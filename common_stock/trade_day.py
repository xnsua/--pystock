import datetime as dt

import tushare
from common_stock import stock_cache_one_month
from nose.tools import assert_equal


class TradeDay:
    def __init__(self):
        self.df = self._read_df()
        self.day_list = list(self.df.calendarDate)
        self.day_map = self._build_all_date_map()
        # The list is faster than pd.Series here
        self.trade_day_list = list(self.df.calendarDate[self.df.isOpen == 1])
        self.trade_day_map = self._build_trade_day_map()

    @staticmethod
    @stock_cache_one_month
    def _read_df():
        return tushare.trade_cal()

    def _build_trade_day_map(self):
        trade_day_map = {}
        for i, value in enumerate(self.trade_day_list):
            trade_day_map[value] = i
        return trade_day_map

    def _build_all_date_map(self):
        date_map = {}
        for i in range(len(self.df.index)):
            date_map[self.df.iat[i, 0]] = i
        return date_map

    def is_trade_day(self, date_: dt.date):
        return str(date_) in self.trade_day_map

    def next(self, day):
        i_day = self.day_map[day] + 1
        while not self.day_list[i_day] in self.trade_day_map:
            i_day = i_day + 1
        return self.day_list[i_day]

    def previous(self, day):
        i_day = self.day_map[day] - 1
        while not self.day_list[i_day] in self.trade_day_map:
            i_day = i_day - 1
        return self.day_list[i_day]

    def shift(self, date_: dt.date, offset):
        i_trade_day = self.trade_day_map[str(date_)]
        return self.trade_day_list[i_trade_day + offset]

    def range(self, start_date, end_date):
        i_start_date = self.trade_day_map[start_date]
        i_end_date = self.trade_day_map[end_date]
        return (self.trade_day_list[i] for i in range(i_start_date, i_end_date))

    def close_range(self, start_date, end_date):
        return self.range(start_date, self.next(end_date))


trade_day = TradeDay()


def test():
    # 24,25 is Saturday and Sunday
    val = trade_day.next('2017-06-24')
    assert_equal(val, '2017-06-26')
    val = trade_day.next('2017-06-26')
    assert_equal(val, '2017-06-27')

    val = trade_day.previous('2017-06-24')
    assert_equal(val, '2017-06-23')
    val = trade_day.previous('2017-06-27')
    assert_equal(val, '2017-06-26')

    val = trade_day.shift('2017-06-26', 2)
    assert_equal(val, '2017-06-28')
    val = trade_day.shift('2017-06-26', -2)
    assert_equal(val, '2017-06-22')

    range_list = [i for i in trade_day.range('2017-06-23', '2017-06-26')]
    assert_equal(range_list, ['2017-06-23'])
    range_list = [i for i in trade_day.range('2017-06-23', '2017-06-27')]
    assert_equal(range_list, ['2017-06-23', '2017-06-26'])


    range_list = [i for i in trade_day.close_range('2017-06-23', '2017-06-26')]
    assert_equal(range_list, ['2017-06-23', '2017-06-26'])

