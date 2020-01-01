import pvlib as pv
from datetime import datetime
import pandas.plotting
from analytics.location.path import LinearPath
from analytics.solar_qualities.position import get_solar_position_time_range_track
from analytics.plots.plot_solar_position import plot_elevation_azimuth
from analytics.plots.plot_path import plot_path, plot_path_gmap
from loguru import logger
import pytz

def main():
    pandas.plotting.register_matplotlib_converters()

    ny_tz = pytz.timezone("America/New_York")
    # london_tz = pytz.timezone("Europe/London")
    start = datetime(2019, 12, 19, hour=0).astimezone(ny_tz)
    end = datetime(2019, 12, 22, hour=0).astimezone(ny_tz)
    logger.debug(start)
    logger.debug(end)

    path = LinearPath.create(
        start_loc=pv.location.Location(41, -74),
        end_loc=pv.location.Location(41, -134),
        start_time=start,
        end_time=end
    )
    solar_pos = get_solar_position_time_range_track(path.timestamps, path.points)
    plot_elevation_azimuth(path.timestamps, solar_pos)
    plot_path(path)


if __name__ == "__main__":
    main()