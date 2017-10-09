from unittest import TestCase

import numpy as np

from common.scipy_helper import pdDF
from data_mining.train_features import KlineFeatures


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
        df = pdDF(data={'open':[1,2,0], 'close':[2,1,0]})
        val = KlineFeatures.is_up_inday(df)
        np.array_equal(val, [True,False,False])
