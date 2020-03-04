import numpy as np
import scipy.integrate
from datetime import datetime

import analytics.forecast.forecast as fc
import analytics.location.path as ap
import analytics.definitions as adef


def ghi_total_over_path(path: ap.Path) -> float:
    """ Returned value is Watt hours per meter squared """
    return sum(ghi_over_path(path))


def ghi_over_path(path: ap.Path, limit=1e6) -> np.ndarray:
    """ Returns 1D numpy array of Watt hours per meter squared """
    df = fc.get_forecast_path(path)
    timestamp = datetime.now().isoformat()
    timestamp = timestamp[:-7].replace(":", "-")
    with open(adef.get_output_path(f"forecast-{timestamp}.csv"), mode="w") as f:
        df.to_csv(path_or_buf=f)
    column = "ghi"

    sel_df = df[column].fillna(value=0)
    sel_df.clip(upper=limit, inplace=True)
    integral = scipy.integrate.cumtrapz(sel_df, x=df.index, axis=0, initial=0)
    hours = integral.astype('timedelta64[h]')
    return hours.astype('float')


def power_over_path(path: ap.Path, panel_area, efficiency, limit=1e6):
    """ Returns Watt hours per time interval """
    df = fc.get_forecast_path(path)
    timestamp = datetime.now().isoformat()
    timestamp = timestamp[:-7].replace(":", "-")
    with open(adef.get_output_path(f"forecast-{timestamp}.csv"), mode="w") as f:
        df.to_csv(path_or_buf=f)
    column = "ghi"

    sel_df = df[column].fillna(value=0)  # Watts / meters^2
    sel_df *= efficiency * panel_area    # Becomes Watts
    sel_df.clip(upper=limit, inplace=True)

    integral_cumulative = scipy.integrate.cumtrapz(sel_df, x=df.index, axis=0, initial=0)
    np.diff
