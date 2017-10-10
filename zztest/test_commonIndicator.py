from unittest import TestCase

import numpy

from common.scipy_helper import nparr
from common_stock.common_indicator import ArrayIndicator


class TestStockIndicator(TestCase):
    def test_min_poses(self):
        arr = numpy.arange(4)
        arr[0] = 10
        arr = numpy.concatenate((arr, arr[::-1]))
        max_arr = ArrayIndicator.max_poses(arr, 5)
        assert numpy.all(max_arr == [False, False, False, True, True, False, False, False])

    def test_max_poses(self):
        arr = numpy.arange(4)
        arr[0] = -1
        arr = numpy.concatenate((arr[::-1], arr))
        max_arr = ArrayIndicator.min_poses(arr, 5)
        assert numpy.all(max_arr == [False, False, False, True, True, False, False, False])

    def test_len_and_slope(self):
        arr1 = nparr([1, 2, 1, 0, 1, 2, 3, 2, 1, 2, 3, 4], dtype=numpy.float64)
        val2 = ArrayIndicator.trend_len_and_slope(arr1, window_len=5)
        assert numpy.array_equal(val2[0], [0, 1, 2, 3, 1, 2, 3, 1, 2, 1, 2, 3])
        assert numpy.allclose(val2[1], [0., 1., 0., -0.33333333, 1., 1., 1., -1., -1., 1., 1., 1.])

    def test_mdd_poses(self):
        arr1 = nparr([1, 2, 1, 1.5, 0, 1, 2])
        poses = ArrayIndicator.mdd_poses(arr1)
        assert poses == (1, 4)

    def test_continuous_count(self):
        arr1 = nparr([False, True, True, False, True, False])
        assert numpy.array_equal(ArrayIndicator.consecutive_count_of_True(arr1),
                                 [0, 1, 2, 0, 1, 0])
        arr1 = nparr([True, True, True, False, True, True])
        assert numpy.array_equal(ArrayIndicator.consecutive_count_of_True(arr1),
                                 [1, 2, 3, 0, 1, 2])

    def test_rise_count(self):
        val = ArrayIndicator.rise_count(numpy.asarray([1, 2, 3, 0, 1]))
        numpy.array_equal(val, [0, 1, 2, 0, 1])

    def test_drop_count(self):
        val = ArrayIndicator.rise_count(numpy.asarray([3, 2, 1, 2, 1]))
        numpy.array_equal(val, [0, 1, 2, 0, 1])

    def test_even_count(self):
        val = ArrayIndicator.even_count(numpy.asarray([1, 1, 1, 0, 0]))
        numpy.array_equal(val, [0, 1, 2, 0, 1])
