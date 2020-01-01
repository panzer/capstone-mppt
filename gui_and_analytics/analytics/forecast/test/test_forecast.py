import datetime
import pandas as pd
import pvlib as pv
import analytics.forecast.forecast as forecast
from loguru import logger


def test_get_forecast_single_on_hour_future():
    # Arrange
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.combine(tomorrow, time=datetime.time(hour=3))

    loc = pv.location.Location(34.25, -72.75)

    # Act
    result = forecast._get_forecast_gfs_on_measurement(loc.latitude, loc.longitude, time, overwrite_cache=True)

    # Assert
    print(result.to_string())


def test_weights():
    # Arrange
    tr = pv.location.Location(40, -70)
    tl = pv.location.Location(40, -80)
    br = pv.location.Location(30, -70)
    bl = pv.location.Location(30, -80)

    target = pv.location.Location(35, -71)

    # Act
    weights = forecast.weights_for_latlon(target, tr, tl, br, bl)
    w_tr, w_tl, w_br, w_bl = weights

    # Assert
    print(weights)


def test_scale_df():
    # Arrange
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [6, 5, 4],
    })

    # Act
    forecast.scale_dataframe(df, 2)

    # Assert
    assert df.equals(pd.DataFrame({
        'a': [2, 4, 6],
        'b': [12, 10, 8],
    }))


def test_get_forecast_on_time():
    # Arrange
    loc = pv.location.Location(40.15, -70.1)
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    time = datetime.datetime.combine(tomorrow, time=datetime.time(hour=3))

    # Act
    df = forecast.get_forecast_on_time(time, loc)

    # Assert
    print(df['low_clouds'])