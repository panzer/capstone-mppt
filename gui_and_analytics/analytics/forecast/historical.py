from typing import List, Iterable, Optional
import os.path
import glob
import re
import tempfile
import tarfile
import zipfile
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import Dataset, MFDataset, Variable

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


def read_multifile(root: str = data_dir):
    path = f"{root}/gfs.0p25*.nc"
    print(path)
    f = MFDataset(path)
    print(f.data_model)
    print(f.dimensions)
    print(f.ncattrs())
    # for n, variable in f.variables.items():  # type: (str, Variable)
    #     print(n)
    #     print(variable[:])
    ghi_raw: Variable = f.variables["DSWRF_P8_L1_GLL0_avg3h"]
    print(ghi_raw.dimensions)
    ghi_raw.getncattr("initial_time0_hours")
    # print(ghi_raw.ncattrs())
    print(ghi_raw[0][0][:])


def index_of(search_this: Iterable, find_this) -> Optional[int]:
    for i, item in enumerate(search_this):
        if item == find_this:
            return i


def get(now: datetime, forecast_for: datetime, lat: float, lon: float):
    pass


def _get_historical_gfs_on_measurement(lat: float, lon: float, now: datetime, dt: datetime):
    """
    Longitude is from 0 to 360 (limited by available data)
    """
    dataset = get_dataset(now=now, forecast_for=dt)
    ghi_raw = dataset.variables["DSWRF_P8_L1_GLL0_avg3h"]
    lat_0 = dataset.variables["lat_0"]
    lon_0 = dataset.variables["lon_0"]
    lat_idx = index_of(lat_0, lat)
    lon_idx = index_of(lon_0, lon)
    return ghi_raw[0][lat_idx][lon_idx]


def get_dataset(now: datetime, forecast_for: datetime) -> Dataset:
    with tempfile.TemporaryDirectory() as temp_dir:
        tarpath = get_top_level_zip_path(now, forecast_for)

        # unzip tarfile
        with tarfile.open(tarpath) as tf:
            tf.extractall(temp_dir)
            pattern = os.path.join(temp_dir, "*")
            inner = get_inner_zip_path(glob.glob(pattern), now, forecast_for)

        # unzip netCDF file
        with zipfile.ZipFile(inner, 'r') as z:
            z.extractall(path=temp_dir)
            return MFDataset(f"{temp_dir}/gfs.0p25*.nc")


def get_top_level_zip_path(now: datetime, forecast_for: datetime) -> str:
    pattern = os.path.join(data_dir, "gfs.0p25.*.nc.tar")
    paths = glob.glob(pattern)
    for path in paths:
        print(path)
        if NetCDFRangeTarfile(path).contains(now, forecast_for):
            return path
    # No valid paths found
    raise ValueError(f"No archives found which are forecasts for {forecast_for} made at {now}")


def get_inner_zip_path(path_options: List[str], now: datetime, forecast_for: datetime) -> str:
    for path in path_options:
        if NetCDFSingleZipFile(path).matches(now, forecast_for):
            return path
    # No valid forecast found
    raise ValueError(f"No archives found which are forecasts for {forecast_for} made at {now}")


class NetCDFSingleZipFile:
    re_pattern = re.compile(r".*?(\d{10})\.f(\d{3})")

    def __init__(self, fullpath: str):
        self.fullpath = fullpath
        self.basename = os.path.basename(self.fullpath)
        self.now, self.fc_time = self.parse(self.basename)

    @classmethod
    def parse(cls, basename: str) -> (datetime, datetime):
        match = cls.re_pattern.match(basename)
        now_str, fc_str = match.group(1, 2)

        now = datetime.strptime(now_str, "%Y%m%d%H")
        fc_time = now + timedelta(hours=int(fc_str))

        return now, fc_time

    def matches(self, now: datetime, forecast_time: datetime) -> bool:
        # if self.now == now:
        #     print(f"{self.fc_time}={forecast_time}")
        return self.now == now and self.fc_time == forecast_time


class NetCDFRangeTarfile:
    re_pattern = re.compile(r".*?(\d{10})\.f(\d{3})")
    maximum_forecast_future = timedelta(hours=165)

    def __init__(self, fullpath: str):
        self.fullpath = fullpath
        self.basename = os.path.basename(self.fullpath)

        start, end = self.parse_date_offsets(self.basename)

        self.now_start, self.start_fc = start
        self.now_end, self.end_fc = end

    @classmethod
    def parse_date_offsets(cls, basename: str) -> ((datetime , datetime), (datetime, datetime)):
        # Returns tuple of (start, end) where start and end are tuples of:
        # (now_time, forecast_time)
        matches: List = cls.re_pattern.findall(basename)
        start, end = matches[0], matches[1]
        now_start_str, fc_start_str = start
        now_end_str, fc_end_str = end

        now_start = datetime.strptime(now_start_str, "%Y%m%d%H")
        fc_start = now_start + timedelta(hours=int(fc_start_str))
        now_end = datetime.strptime(now_end_str, "%Y%m%d%H")
        fc_end = now_end + timedelta(hours=int(fc_end_str))

        return (now_start, fc_start), (now_end, fc_end)

    def contains(self, now: datetime, forecast_time: datetime):

        latest_possible_forecast = now + self.maximum_forecast_future
        if now == self.now_start:
            # time that forecast was made is on the start boundary
            return self.start_fc <= forecast_time <= latest_possible_forecast
        elif now == self.now_end:
            # time that forecast was made is on the end boundary
            return forecast_time <= self.end_fc
        elif self.now_start < now < self.now_end:
            # time that forecast was made is in between boundaries
            return forecast_time <= latest_possible_forecast
        else:
            return False


class Times:
    def __init__(self, netcdf_times: Variable):
        # Convert netcdf Variable to np.ndarray of time strings
        # produces something like:
        # array(['12/25/2018 (06:00)', '12/25/2018 (12:00)', ...], dtype='<U18')
        self.times = np.array([e.tobytes().decode('UTF-8') for e in netcdf_times[:]])

    def index_for_datetime(self, dt: datetime) -> int:
        formatted_str = dt.strftime("%m/%d/%Y (%H:%M)")
        indexes = np.argwhere(self.times == formatted_str)
        return indexes[0]
