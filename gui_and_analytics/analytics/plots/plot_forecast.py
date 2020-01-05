import matplotlib.pyplot as plt
import analytics.forecast.forecast as fc
import analytics.location.path as ap
import pvlib as pv
import pandas as pd
import numpy as np
import pandas.plotting
import pytz
import mplcursors
from loguru import logger
from tqdm import tqdm
import datetime


def main():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.combine(tomorrow, time=datetime.time(hour=16),
                                     tzinfo=pytz.utc)
    # plot_forecast_area(top_right=pv.location.Location(42, -140),
    #                    bottom_left=pv.location.Location(41, -141),
    #                    time=time, metric="high_clouds")
    path = ap.LinearPath.create(start_loc=pv.location.Location(42, -140),
                                end_loc=pv.location.Location(41, -141),
                                start_time=time, end_time=time+datetime.timedelta(hours=3))
    plot_forecast_path(path, "ghi_raw")


def plot_forecast_path(path: ap.Path, metric: str):
    pandas.plotting.register_matplotlib_converters()
    df = fc.get_forecast_path(path)
    print(df.to_string())
    plt.plot(df[metric])
    plt.show()


def plot_forecast_area(top_right: pv.location.Location, bottom_left: pv.location.Location,
                       time: datetime, metric: str,
                       imshow_kwargs: dict = None, resolution: int = 16, use_tqdm=True):
    """
    :param top_right: Location with the greatest latitude and longitude
    :param bottom_left: Location with the least latitude and longitude
    :param time: Time of forecast
    :param metric: The metric to forecast; any of pvlib's forecast metrics
    :param imshow_kwargs: kwargs to pass to imshow
    :param resolution: number of discrete points to break up each degree into
    :param use_tqdm: boolean, whether to show tqdm loading bar or not
    :return: None
    Valid metrics:
    mid_clouds, convect_clouds, boundary_clouds, ghi_raw, high_clouds, total_clouds
    low_clouds, temp_air, wind_speed_gust, wind_speed_u, wind_speed_v
    """
    pandas.plotting.register_matplotlib_converters()

    # Default key-word arguments (kwargs)
    if imshow_kwargs is None:
        imshow_kwargs = dict()  # use empty dictionary

    min_lat = bottom_left.latitude
    max_lat = top_right.latitude
    min_lon = bottom_left.longitude
    max_lon = top_right.longitude
    n_lat = int((max_lat - min_lat) * resolution)
    n_lon = int((max_lon - min_lon) * resolution)

    lats = np.linspace(min_lat, max_lat, n_lat)
    lons = np.linspace(min_lon, max_lon, n_lon)

    locations = [pv.location.Location(lat, lon) for lat in lats for lon in lons]
    results = []

    it = tqdm if use_tqdm else iter

    for loc in it(locations):
        forecast = fc.get_forecast_single(time, loc)
        res = float(forecast[metric])
        results.append(res)

    coverage = np.array(results)
    grid = coverage.reshape((n_lat, n_lon))

    use_imshow_kwargs = dict(extent=(min_lon, max_lon, min_lat, max_lat),
                             origin="lower",  # plot starting at the lower left corner
                             interpolation='nearest', cmap="Blues_r", vmin=0, vmax=100)
    use_imshow_kwargs.update(imshow_kwargs)
    im = plt.imshow(grid, **use_imshow_kwargs)
    ax = plt.gca()
    fig = plt.gcf()
    cbar = fig.colorbar(im, ax=ax)
    cbar.minorticks_on()
    ax.set_xticks(np.arange(min_lon, max_lon, 0.25))
    ax.set_yticks(np.arange(min_lat, max_lat, 0.25))
    ax.set_title(f"{metric} {time}")
    plt.show()


if __name__ == "__main__":
    main()
