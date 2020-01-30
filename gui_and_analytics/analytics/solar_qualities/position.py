from typing import List, Union

import pandas as pd
import pvlib as pv

import analytics.location.path as alp


def get_solar_position_time_range(times: pd.DatetimeIndex, location: pv.location.Location) -> pd.DataFrame:
    """

    :param time:
    :param location:
    :return:
    """
    return pv.solarposition.get_solarposition(times, location.latitude, location.longitude)


def get_solar_position_single(time: pd.Timestamp, location: pv.location.Location) -> pd.DataFrame:
    """

    :param time:
    :param location:
    :return:
    """
    return pv.solarposition.get_solarposition(time=pd.DatetimeIndex(data=[time]),
                                              latitude=location.latitude,
                                              longitude=location.longitude)


def get_solar_position_time_range_track(times: pd.DatetimeIndex, locations: List[pv.location.Location]) -> pd.DataFrame:
    result = pd.DataFrame()

    for time, location in zip(times, locations):
        solar = get_solar_position_single(time, location)
        result = result.append(solar)

    return result