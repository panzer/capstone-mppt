import analytics.solar_qualities.position as sp
import pvlib as pv
import pandas as pd
import pytz
from loguru import logger


def test_solar_pos():
    # Arrange
    loc = pv.location.Location(42, -72)
    time = pd.date_range(start='11/28/2019', end='12/1/2019', freq='H', tz=pytz.timezone('America/New_York'))

    # Act
    result = sp.get_solar_position_time_range(time, loc)

    # Assert
    logger.info(result.columns)
