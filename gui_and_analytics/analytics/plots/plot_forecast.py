import matplotlib.pyplot as plt
import analytics.forecast.forecast as fc
import pvlib as pv
import pandas as pd
import numpy as np
import pandas.plotting
import pytz
import mplcursors
from loguru import logger
import datetime
import multiprocessing.pool


def main():
    pandas.plotting.register_matplotlib_converters()

    loc = pv.location.Location(42.2, -72.0)
    dt = datetime.datetime.now()

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.combine(tomorrow, time=datetime.time(hour=6),
                                     tzinfo=pytz.utc)
    logger.debug(f"{time.hour % 3 == 0}")

    n_lat = 24
    n_lon = 24
    min_lat = 41.
    max_lat = 42.
    min_lon = -72.
    max_lon = -71.
    top_right = pv.location.Location(max_lat, max_lon)
    bot_left = pv.location.Location(min_lat, min_lon)

    lats = np.linspace(top_right.latitude, bot_left.latitude, n_lat)
    lons = np.linspace(bot_left.longitude, top_right.longitude, n_lon)

    # mid_clouds  convect_clouds  boundary_clouds  ghi_raw  high_clouds  total_clouds  low_clouds    temp_air  wind_speed_gust  wind_speed_u  wind_speed_v
    locations = [pv.location.Location(lat, lon) for lat in lats for lon in lons]
    results = [500] * len(locations)

    def set_result(index, result):
        results[index] = result
        logger.debug(index)

    # with multiprocessing.pool.Pool() as pool:
    #     for i, loc in enumerate(locations):
    #         def callback(r):
    #             set_result(i, float(r['total_clouds']))
    #
    #         pool.apply_async(fc.get_forecast_on_time, args=(time, loc), callback=callback)
    #
    #     pool.close()
    #     pool.join()

    results = [float(fc.get_forecast_single(time, loc)['total_clouds']) for loc in locations]

    coverage = np.array(results)
    grid = coverage.reshape((n_lat, n_lon))

    print(grid)

    im = plt.imshow(grid, extent=(min_lon, max_lon, min_lat, max_lat),
               interpolation='nearest', cmap="hot", vmin=0, vmax=100)
    ax = plt.gca()
    ax.set_xticks(np.arange(min_lon, max_lon, 0.25))
    ax.set_yticks(np.arange(min_lat, max_lat, 0.25))
    plt.show()

    # result = fc.get_forecast_single(dt, loc)
    #
    # logger.info(result['low_clouds'])
    # logger.info(result['mid_clouds'])
    # logger.info(result['high_clouds'])


def plot_cloud_cover(time: pd.DatetimeIndex, forecast: pd.DataFrame):
    """
    :param time:
    :param forecast: Dataframe with columns "low_clouds", "mid_clouds" and "high_clouds"
    :return:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.plot(time, forecast['low_clouds'], label="low_clouds")

    ax.set_title("GFS 0.25 deg forecast")
    ax.set_ylabel("Cloud cover %")
    ax.set_ylim(0, 100)
    ax.grid()

    mplcursors.cursor()
    plt.show()


if __name__ == "__main__":
    main()
