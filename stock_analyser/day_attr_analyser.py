from itertools import islice

from nose.tools import assert_equal

from common.algorithm import group_consecutive_count
from common.data_structures.py_dataframe import DayDataRepr
from common.scipy_helper import pdDF
from common_stock.trade_day import gtrade_day
from stock_data_updater.day_data_updater import read_etf_day_data
from trading_emulation.data_provider import gdata_provider


# noinspection PyTypeChecker
class DropRiseCount:
    def __init__(self, ddr: DayDataRepr):
        self.ddr = ddr
        self.rise_count = None
        self.drop_count = None
        self.calc_fill_day_attr(ddr)

    def rise_count_of(self, day):
        return self.rise_cnts[self.ddr.day2index[day]]

    def drop_count_of(self, day):
        return self.drop_cnts[self.ddr.day2index[day]]

    def calc_fill_day_attr(self, ddr: DayDataRepr):
        rise = list((ddr.df.close - ddr.df.open) > 0)
        self.rise_count = group_consecutive_count(rise, True)
        self.drop_count = group_consecutive_count(rise, False)
        self.rise_count = [0, *self.rise_count[0: -1]]
        self.drop_count = [0, *self.drop_count[0: -1]]


def test_day_attr_analyser():
    df = pdDF(data=[[1, 2, 1, 1, '111111'],
                    [1, 2, 1, 1, 1],
                    [2, 1, 1, 1, 1],
                    [1, 2, 1, 1, 1],
                    [1, 3, 1, 1, 1]],
              index=['2015-01-01', '2015-01-02', '2015-01-03', '2015-01-04', '2015-01-05'],
              columns=['open', 'close', 'high', 'low', 'code'])
    # ddr = gdata_provider.ddr('bb0900')
    # drc = DropRiseCount(ddr)
    ddr = DayDataRepr(df)
    rdc = DropRiseCount(ddr)
    assert_equal(rdc.rise_count, [0, 1, 2, 0, 1])
    assert_equal(rdc.drop_count, [0, 0, 0, 1, 0])
