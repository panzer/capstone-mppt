import unittest
import pytz
from datetime import datetime, timedelta
import analytics.location.path as ap
import analytics.power.solar as solar

from pvlib.location import Location


class SolarPower(unittest.TestCase):
    def test_integration_nonzero(self):
        # Arrange
        start = datetime.now(tz=pytz.utc)
        end = start + timedelta(days=1)
        path = ap.LinearPath.create(start_loc=Location(42, 71), end_loc=Location(43, 72),
                                    start_time=start, end_time=end)

        # Act
        p = solar.ghi_total_over_path(path)

        # Assert
        self.assertTrue(p > 0)


if __name__ == '__main__':
    unittest.main()
