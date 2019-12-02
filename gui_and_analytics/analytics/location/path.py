from __future__ import annotations
from typing import List
from datetime import datetime
import pvlib as pv
import pandas as pd
import dataclasses
import numpy as np
import abc


@dataclasses.dataclass()
class Path:
    points: List[pv.location.Location]
    timestamps: List[pd.Timestamp]

    @classmethod
    @abc.abstractmethod
    def create(cls, *args, **kwargs) -> LinearPath:
        pass

    @property
    def lats_lons(self) -> (List[float], List[float]):
        lats = [point.latitude for point in self.points]
        lons = [point.longitude for point in self.points]

        return lats, lons

class LinearPath(Path):
    @classmethod
    def create(cls, start_loc: pv.location.Location, end_loc: pv.location.Location,
               start_time: datetime, end_time: datetime,
               npoints=None) -> LinearPath:
        """

        :param start_loc:
        :param end_loc:
        :param start_time:
        :param end_time:
        :param npoints: Number of points on the path. Defaults to None, for auto.
        :return:
        """

        time_range = end_time - start_time

        if npoints is None:  # automatically determine appropriate number of points
            npoints = 100

        lats = np.linspace(start_loc.latitude, end_loc.latitude, npoints)

        lons = np.linspace(start_loc.longitude, end_loc.longitude, npoints)

        points = [pv.location.Location(lat, lon) for lat, lon in zip(lats, lons)]

        delta = time_range / npoints
        times = [start_time + (delta * n) for n in range(npoints)]

        return Path(points=points, timestamps=times)
