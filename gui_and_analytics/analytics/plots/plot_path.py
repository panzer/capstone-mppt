import gmplot
import matplotlib.pyplot as plt
import pvlib as pv
import mplcursors
from datetime import datetime, timedelta

from analytics.location.path import Path, LinearPath
from loguru import logger


def main():
    path = LinearPath.create(
        start_loc=pv.location.Location(latitude=42, longitude=-71),
        end_loc=pv.location.Location(latitude=31, longitude=-170),
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(days=1)
    )
    plot_path(path)


def plot_path(path: Path):
    fig, ax = plt.subplots(nrows=1, ncols=1)

    lats, lons = path.lats_lons

    ax.plot(lons, lats)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid()

    mplcursors.cursor()
    plt.show()


def plot_path_gmap(path: Path):
    gmap = gmplot.GoogleMapPlotter(0, 0, 0)

    lats, lons = path.lats_lons

    gmap.plot(lats, lons)

    gmap.draw("output/map.html")


if __name__ == "__main__":
    main()