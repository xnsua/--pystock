from unittest import TestCase

import numpy as np

from common.scipy_helper import pdDF
from data_mining.kline_features import KlineFeatures


class TestKlineFeatures(TestCase):
    def test_up_day_count_of_previous_days(self):
        val = KlineFeatures.up_count_of_previous_days(np.asarray([0, 1, 2, 1, 0, 1, 0]))
        np.array_equal(val, [0, 0, 1, 2, 0, 0, 1])

    def test_down_day_count_of_previous_day(self):
        val = KlineFeatures.down_count_of_previous_days(-1 * np.asarray([0, 1, 2, 1, 0, 1, 0]))
        np.array_equal(val, [0, 0, 1, 2, 0, 0, 1])

    def test_even_count_of_previous_days(self):
        val = KlineFeatures.down_count_of_previous_days(-1 * np.asarray([1, 1, 1, 0, 1, 1, 0]))
        np.array_equal(val, [0, 0, 1, 2, 0, 0, 1])

    def test_is_up_inday(self):
        df = pdDF(data={'open': [1, 2, 0], 'close': [2, 1, 0]})
        val = KlineFeatures.is_up_inday(df)
        np.array_equal(val, [True, False, False])

    def test_ochl_features(self):
        df = pdDF(data={'open': [1., 2., 3., 4.], 'close': [1.1, 2.1, 3.1, 4.1],
                        'high': [1.2, 2.2, 3.3, 4.4], 'low': [0.1, 0.2, 0.3, 0.4]})
        o, c, h, l = KlineFeatures.ochl_features(df)
        assert o[0] == 1.
        assert c[0] == 1.1
        assert h[0] == 1.2
        assert l[0] == 0.1

    def test_jump_value(self):
        df = pdDF(data={'high': [2, 4, 1.3, 1.4],
                        'low': [0.1, 2.2, 0.3, 0.4]})
        jump_values = KlineFeatures.jump_value(df)
        assert np.allclose(jump_values, [0.1, 0.2, -0.9, 0.])

    def test_day_compare_features(self):
        df = pdDF(data={'open': [1., 2., 3., 4.], 'close': [1.1, 2.1, 3.1, 4.1],
                        'high': [1., 2.1, 3.2, 4.3], 'low': [0.1, 0.2, 0.3, 0.4]})
        fs = KlineFeatures.day_compare_features(df)
        result = np.asarray([*fs])
        test_result = np.asarray([[1., 0.95, 0.93333333, 0.925, ],
                                  [1.1, 1., 0.96666667, 0.95, ],
                                  [0., 0.45, 0.6, 0.675],
                                  [0., 0.5, 0.63333333, 0.7, ],
                                  [1., 1., 1., 1.],
                                  [0.1, 0.05, 0.03333333, 0.025, ],
                                  [0., 0.45, 0.63333333, 0.725, ],
                                  [0., 0., 0., 0.]])

        assert np.all(result - test_result < 0.0001)

    def test_is_close_up(self):
        df = pdDF(data={'open': [1., 2., 3., 4.], 'close': [1.1, 2.1, 0.1, 4.1]})
        val = KlineFeatures.is_close_up(df)
        assert np.allclose(val, [True, True, False, True])
