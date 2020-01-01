import pandas as pd
import pvlib as pv
import datetime
import math
import requests.exceptions
from pvlib.forecast import GFS
from cachier import cachier
from loguru import logger
from analytics.location.utils import distance_btwn_loc


def preload_forecast_in_bounds(date: datetime.date, top_right: pv.location.Location, bottom_left: pv.location.Location):
    next_lat = get_next(top_right.latitude)
    next_lon = get_next(top_right.longitude)
    prev_lat = get_prev(bottom_left.latitude)
    prev_lon = get_prev(bottom_left.longitude)

    lats = [prev_lat + (0.25 * n) for n in range(round((next_lat - prev_lat) / 0.25) + 1)]
    lons = [prev_lon + (0.25 * n) for n in range(round((next_lon - prev_lon) / 0.25) + 1)]

    locs = [(lat, lon) for lat in lats for lon in lons]
    logger.info(f"Preloading {len(locs)} forecasts...")

    for loc in locs:
        lat, lon = loc
        logger.debug(f"Starting: {lat} {lon} {date}")
        _get_forecast_gfs_day(lat, lon, date)

    logger.info("Preload complete.")


def get_forecast_single(time: datetime.datetime, location: pv.location.Location) -> pd.DataFrame:
    if time.hour % 3 == 0 and time.minute == 0 and time.second == 0 and time.microsecond == 0:
        # edge case: on 3 hour interval
        return get_forecast_on_time(time, location)

    next_hour = int(get_next(time.hour, ii=1/3))
    prev_hour = int(get_prev(time.hour, ii=1/3))

    next_time = time.replace(hour=next_hour, minute=0, second=0, microsecond=0)
    prev_time = time.replace(hour=prev_hour, minute=0, second=0, microsecond=0)

    forecast_earlier = get_forecast_on_time(prev_time, location)
    forecast_later = get_forecast_on_time(next_time, location)

    w_earlier, w_later = weight_linear_time(time, prev_time, next_time)
    scale_dataframe(forecast_earlier, w_earlier)
    scale_dataframe(forecast_later, w_later)

    if forecast_earlier.size == 0 or forecast_later.size == 0:
        logger.warning(f"Incomplete data {time} {location.latitude}, {location.longitude}")
        return pd.DataFrame(data=[0], index=pd.DatetimeIndex(data=[time]))

    a = forecast_earlier.reindex([time], method='nearest')
    b = forecast_later.reindex([time], method='nearest')

    tot = a + b
    logger.info(tot['total_clouds'])
    return tot


def get_forecast_on_time(time: datetime.datetime, location: pv.location.Location) -> pd.DataFrame:
    # All locations are bounded by a "square" whose edges are the lat and lons that fall on the nearest 0.25 multiples
    # Special case: near the +/-180 degree longitude meridian
    assert time.hour % 3 == 0 and time.minute == 0 and time.second == 0 and time.microsecond == 0, "Hour must be on 3 hour multiple"

    on_latitude_bound = location.latitude % 0.25 == 0
    on_longitude_bound = location.longitude % 0.25 == 0

    if on_latitude_bound and on_longitude_bound:
        # corner case
        return _get_forecast_gfs_on_measurement(location.latitude, location.longitude, time)
    elif on_latitude_bound or on_longitude_bound:
        # edge cases
        if on_latitude_bound:
            next_lon = get_next(location.longitude)
            prev_lon = get_prev(location.longitude)

            start = pv.location.Location(location.latitude, prev_lon)
            end = pv.location.Location(location.latitude, next_lon)
        else:
            next_lat = get_next(location.latitude)
            prev_lat = get_prev(location.latitude)

            start = pv.location.Location(next_lat, location.longitude)
            end = pv.location.Location(prev_lat, location.longitude)

        w_a, w_b = weight_linear(location, start, end)
        forecast_a = _get_forecast_gfs_on_measurement(start.latitude, start.longitude, time)
        forecast_b = _get_forecast_gfs_on_measurement(end.latitude, end.longitude, time)
        scale_dataframe(forecast_a, w_a)
        scale_dataframe(forecast_b, w_b)

        return forecast_a + forecast_b

    next_lat = get_next(location.latitude)
    next_lon = get_next(location.longitude)
    prev_lat = get_prev(location.latitude)
    prev_lon = get_prev(location.longitude)

    forecast_top_right = _get_forecast_gfs_on_measurement(next_lat, next_lon, time)
    forecast_top_left = _get_forecast_gfs_on_measurement(next_lat, prev_lon, time)
    forecast_bot_right = _get_forecast_gfs_on_measurement(prev_lat, next_lon, time)
    forecast_bot_left = _get_forecast_gfs_on_measurement(prev_lat, prev_lon, time)

    tr = pv.location.Location(next_lat, next_lon)
    tl = pv.location.Location(next_lat, prev_lon)
    br = pv.location.Location(prev_lat, next_lon)
    bl = pv.location.Location(prev_lat, prev_lon)
    w_tr, w_tl, w_br, w_bl = weights_for_latlon(location, tr, tl, br, bl)

    scale_dataframe(forecast_top_right, w_tr)
    scale_dataframe(forecast_top_left, w_tl)
    scale_dataframe(forecast_bot_right, w_br)
    scale_dataframe(forecast_bot_left, w_bl)

    return forecast_top_right + forecast_top_left + forecast_bot_right + forecast_bot_left


def scale_dataframe(df: pd.DataFrame, scalar: float):
    for col in list(df):
        df.loc[:, col] *= scalar

def weight_linear_time(target: datetime.datetime, start: datetime.datetime, end: datetime.datetime):
    total = (end - start).total_seconds()
    diff_start = (target - start).total_seconds()
    w_end = diff_start / total
    return 1 - w_end, w_end

def weight_linear(target: pv.location.Location, start: pv.location.Location, end: pv.location.Location):
    """ All three points should form a straight line """
    dist_a = distance_btwn_loc(start, target)
    total_dist = distance_btwn_loc(start, end)
    w_end = dist_a / total_dist
    return 1 - w_end, w_end


def weights_for_latlon(target: pv.location.Location,
                       tr: pv.location.Location,
                       tl: pv.location.Location,
                       br: pv.location.Location,
                       bl: pv.location.Location) -> (float, float, float, float):
    # Assumes tr, tl, br, and bl form a trapezoid
    logger.debug(f"weighting ({tr.latitude}, {tr.longitude}) ({bl.latitude}, {bl.longitude})")
    top = distance_btwn_loc(tr, tl)
    bottom = distance_btwn_loc(br, bl)
    tc = pv.location.Location(tr.latitude, (tr.longitude + tl.longitude) / 2)  # top center
    bc = pv.location.Location(br.latitude, (br.longitude + bl.longitude) / 2)  # bottom center
    height = distance_btwn_loc(tc, bc)

    upper_lat = tr.latitude
    lower_lat = br.latitude
    vertical = normalize(target.latitude, upper_lat, lower_lat)

    right_lon = tr.longitude
    left_lon = tl.longitude

    middle = expand(vertical, hi=top, lo=bottom)

    top_trap_height = height * (1 - vertical)
    bot_trap_height = height * vertical

    top_trap_area = trapezoid_area(top, middle, top_trap_height)
    bot_trap_area = trapezoid_area(middle, bottom, bot_trap_height)
    total_trap_area = top_trap_area + bot_trap_area

    horizontal = normalize(target.longitude, right_lon, left_lon)

    tl_area = top_trap_area * horizontal
    tr_area = top_trap_area * (1 - horizontal)
    bl_area = bot_trap_area * horizontal
    br_area = bot_trap_area * (1 - horizontal)

    w_tl = br_area / total_trap_area
    w_tr = bl_area / total_trap_area
    w_bl = tr_area / total_trap_area
    w_br = tl_area / total_trap_area

    return w_tr, w_tl, w_br, w_bl


def normalize(v: float, hi: float, lo: float):
    return (v - lo) / (hi - lo)

def expand(v: float, hi: float, lo: float):
    """ Expects v within [0, 1] """
    return (v * (hi - lo)) + lo

def get_next(x: float, ii: float = 4):
    """
    x: value
    ii: inverse increment, ie 1/increment. Default increment of 0.25 => 4
    """
    result = math.ceil(x * ii) / ii
    if math.isclose(x, result, rel_tol=0, abs_tol=1e-5):
        return x + 1/ii
    return result


def get_prev(x: float, ii: float = 4):
    """
    x: value
    ii: inverse increment, ie 1/increment. Default increment of 0.25 => 4
    """
    result = math.floor(x * ii) / ii
    if math.isclose(x, result, rel_tol=0, abs_tol=1e-5):
        return x - 1/ii
    return result


def trapezoid_area(base1: float, base2: float, height: float) -> float:
    return (base1 + base2) * height / 2

def get_forecast_time_range(start_time: datetime.datetime, end_time: datetime.datetime, location: pv.location.Location):
    pass


@cachier(stale_after=datetime.timedelta(hours=6))
def _get_forecast_gfs_on_measurement(lat: float, lon: float, dt: datetime.datetime) -> pd.DataFrame:
    logger.debug(f"GFS on measurement {lat} {lon} {dt}")
    assert dt.hour % 3 == 0 and dt.minute == 0 and dt.second == 0 and dt.microsecond == 0, "Hour must be on 3 hour multiple"

    date_data = _get_forecast_gfs_day(lat, lon, dt.date())

    result = date_data.truncate(before=dt, after=dt)

    return result


@cachier(stale_after=datetime.timedelta(hours=6))
def _get_forecast_gfs_day(lat: float, lon: float, date: datetime.date) -> pd.DataFrame:
    """
    Suspected that multithreading this does not work, because of
    some internal logic within pvlib.forecast.ForecastModel.get_data
    """
    logger.debug(f"GFS day {lat} {lon} {date}")
    today = datetime.datetime.today()
    date_after = date + datetime.timedelta(days=1)
    one_week_from_today = today + datetime.timedelta(weeks=1)
    assert lat % 0.25 == 0, "Latitude must be multiple of 0.25"
    assert lon % 0.25 == 0, "Longitude must be multiple of 0.25"
    assert one_week_from_today.date() - date >= datetime.timedelta(), "Cannot be more than 1 week in the future"

    model = GFS(resolution="quarter")
    start = datetime.datetime.combine(date, datetime.time())
    end = datetime.datetime.combine(date_after, datetime.time())

    try:
        data: pd.DataFrame = model.get_data(lat, lon, start, end)
    except requests.exceptions.ConnectionError:
        raise ConnectionAbortedError("Connection Error while fetching forecast data. Check network connection.")

    return model.rename(data)
