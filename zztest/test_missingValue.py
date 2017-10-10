from unittest import TestCase

import numpy

from data_mining.data_preprocess import MissingValue


class TestMissingValue(TestCase):
    def test_handle_df_missing_values(self):
        from pandas import DataFrame
        arr = numpy.arange(700000)
        arr1 = numpy.roll(arr, -1)
        arr2 = numpy.roll(arr, -2)
        arr3 = numpy.roll(arr, -3)
        arr4 = numpy.roll(arr, -4)
        arr5 = numpy.roll(arr, -5)
        df = DataFrame(data={'open': arr1, 'close': arr2, 'high': arr3, 'low': arr4, 'volume': arr5})
        val = MissingValue.fill_with_previous(df)
        print(val.head(10))



