import os.path
import numpy as np
from datetime import datetime
from netCDF4 import MFDataset, Variable

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


def read_file():
    path = f"{data_dir}/gfs.0p25*.nc"
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


class Times:
    def __init__(self, netcdf_times: Variable):
        # Convert netcdf Variable to np.ndarray of time strings
        # produces something like:
        # array(['12/25/2018 (06:00)', '12/25/2018 (12:00)', ...], dtype='<U18')
        self.times = np.array([e.tobytes().decode('UTF-8') for e in netcdf_times[:]])

    def index_for_datetime(self, dt: datetime) -> int:
        formatted_str = dt.strftime("%m/%d/%Y (%H:%M)")
        indexes = np.argwhere(self.times == formatted_str)
        print(indexes)
