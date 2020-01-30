import matplotlib.pyplot as plt
import analytics.solar_qualities.position as sp
import pvlib as pv
import pandas as pd
import pandas.plotting
import pytz
import mplcursors
from loguru import logger


def main():
    pandas.plotting.register_matplotlib_converters()

    loc = pv.location.Location(42, -72)
    time = pd.date_range(start='11/28/2019', end='12/1/2019', freq='H', tz=pytz.timezone('America/New_York'))

    result = sp.get_solar_position_time_range(time, loc)

    plot_elevation_azimuth(time, result)


def plot_elevation_azimuth(time: pd.DatetimeIndex, solar_pos: pd.DataFrame):
    """
    Shows two subplots of elevation and azimuth over time
    :param time:
    :param solar_pos: Dataframe with columns "elevation" and "azimuth"
    :return:
    """
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)

    ax[0].plot(time, solar_pos['elevation'], label="elevation")
    ax[0].set_title("Solar Position")
    ax[0].set_ylabel("Elevation (°)")
    ax[0].set_ylim(-180, 180)
    ax[0].grid()

    ax[1].plot(time, solar_pos['azimuth'], label="azimuth")
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Azimuth (°)")
    ax[1].set_ylim(0, 360)
    ax[1].grid()

    mplcursors.cursor()
    plt.show()


if __name__ == "__main__":
    main()
