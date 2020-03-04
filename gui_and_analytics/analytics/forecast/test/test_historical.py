import unittest
import os.path
import analytics.forecast.historical as hist
from datetime import datetime


class HistoricalDataTest(unittest.TestCase):
    def test_something(self):
        hist.read_multifile()

    def test_filename_parse(self):
        # Arrange
        fullpath = os.path.join(hist.data_dir, "gfs.0p25.2019011012.f153-2019011500.f057.grib2.panzer408979.nc.tar")
        now = datetime(year=2019, month=1, day=11)
        fc_time = datetime(year=2019, month=1, day=16, hour=3)

        # Act
        tf = hist.NetCDFRangeTarfile(fullpath)
        contained = tf.contains(now, fc_time)

        # Assert
        self.assertTrue(contained)

    def test_get_dataset(self):
        now = datetime(year=2019, month=1, day=11)
        fc_time = datetime(year=2019, month=1, day=16, hour=3)
        hist.get_dataset(now, fc_time)


if __name__ == '__main__':
    unittest.main()
