import matplotlib.pyplot as plt
import analytics.forecast.forecast as fc
import analytics.location.path as ap
import analytics.power.solar as solar
import analytics.definitions as adef
import pvlib as pv
import pandas.plotting
import pytz
import datetime
from typing import Optional


def main():
    points = [
        pv.location.Location(36, 141),
        pv.location.Location(42, 162),
        pv.location.Location(44, 168),
        pv.location.Location(44, 175),
        # pv.location.Location(44, -175),
        # pv.location.Location(44, -165),
        # pv.location.Location(43, -155),
        # pv.location.Location(40, -145),
        # pv.location.Location(37, -135),
        # pv.location.Location(35, -128),
        # pv.location.Location(32, -118)
    ]
    start = datetime.datetime.now(tz=pytz.utc)
    end = start + datetime.timedelta(days=5)
    delta = (end - start) / len(points)
    timestamps = [start + (delta * i) for i in range(len(points))]
    path: Optional[ap.SegmentedPath] = None
    for p, t in zip(points, timestamps):
        if path is None:
            path = ap.SegmentedPath.create(p, t)
        else:
            path.append_point(p, t, npoints=6)

    plot_path_power(path)


def plot_path_power(path: ap.Path):
    pandas.plotting.register_matplotlib_converters()

    powers = solar.ghi_over_path(path)

    plt.plot(path.timestamps, powers)
    plt.xlabel("Time")
    plt.ylabel("Wh/m^2")
    plt.show()


if __name__ == "__main__":
    main()
