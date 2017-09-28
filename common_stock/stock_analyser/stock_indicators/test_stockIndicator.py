from unittest import TestCase

import numpy

from common.scipy_helper import nparr
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
        arr1 = nparr([1, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4], dtype=numpy.float64)
        val2 = StockIndicator.trend_len_and_slope(arr1, window_len=5)
        assert numpy.array_equal(val2[0], [0, 1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 3])
        assert numpy.allclose(val2[1], [0., 1., 0., -0.33333333, 1., 1., 1., -1., -1., 1., 1., 1.])
