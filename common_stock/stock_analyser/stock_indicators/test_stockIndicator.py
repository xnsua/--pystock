from unittest import TestCase

import numpy

from common_stock.stock_analyser.stock_indicators.stock_indicator import StockIndicator


class TestStockIndicator(TestCase):
    def test_min_poses(self):
        arr = numpy.arange(4)
        arr[0] = 10
        arr = numpy.concatenate((arr, arr[::-1]))
        max_arr = StockIndicator.max_poses(arr, 5)
        assert numpy.all(max_arr == [False, False, False, True, True, False, False, False])

    def test_max_poses(self):
        arr = numpy.arange(4)
        arr[0] = -1
        arr = numpy.concatenate((arr[::-1], arr))
        max_arr = StockIndicator.min_poses(arr, 5)
        assert numpy.all(max_arr == [False, False, False, True, True, False, False, False])

    def test_len_and_slope(self):
        arr = numpy.arange(4)
        arr = numpy.concatenate((arr[::-1], arr, arr[::-1]))
        arr[0] = -1
        StockIndicator.trend_len_and_slope(arr, 5)
