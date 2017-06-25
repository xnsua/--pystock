import datetime as dt

import pandas
import tushare
from common_stock.stock_config import stock_cache_one_month
from nose.tools import assert_equal


class TradeDay:
    def __init__(self):
        self.df = self.read_df()
        self.day_list = list(self.df.calendarDate)
        self.day_map = self.build_all_date_map()
        # The list is faster than pd.Series here
        self.trade_day_list = list(self.df.calendarDate[self.df.isOpen == 1])
        self.trade_day_map = self.build_trade_day_map()

    @staticmethod
    @stock_cache_one_month
    def read_df():
        # path = pathlib.Path(__file__).parent / 'trade_day.csv'
        # return pd.read_csv(str(path), index_col='index')
        return tushare.trade_cal()

    def build_trade_day_map(self):
        trade_day_map = {}
        for i, value in enumerate(self.trade_day_list):
            trade_day_map[value] = i
        return trade_day_map

    def build_all_date_map(self):
        date_map = {}
        for i in range(len(self.df.index)):
            date_map[self.df.iat[i, 0]] = i
        return date_map

    def is_trade_day(self, date_: dt.date):
        return str(date_) in self.trade_day_map

    def offset_trade_day(self, date_: dt.date, offset):
        i_trade_day = self.trade_day_map[str(date_)]
        return self.trade_day_list[i_trade_day + offset]

    def get_date_range(self, start_date, end_date):
        i_start_date = self.trade_day_map[start_date]
        i_end_date = self.trade_day_map[end_date]
        return self.trade_day_list[i_start_date:i_end_date]

    def get_close_trade_day_range(self, start_date, end_date):
        i_start_date = self.trade_day_map[start_date]
        i_end_date = self.trade_day_map[end_date]
        return self.trade_day_list[i_start_date:i_end_date + 1]

    def get_nearby_trade_day(self, day, is_before):
        i_day = self.day_map[day]
        if is_before:
            while not self.day_list[i_day] in self.trade_day_map:
                i_day = i_day - 1
            return self.day_list[i_day]
        else:
            while not self.day_list[i_day] in self.trade_day_map:
                i_day = i_day + 1
            return self.day_list[i_day]

    def get_n_trade_days(self, day, ndays):
        if day not in self.trade_day_map:
            day = self.get_nearby_trade_day(day, ndays < 0)
        i_day = self.trade_day_map[str(day)]
        if ndays > 0:
            return self.trade_day_list[i_day: i_day + ndays]
        else:
            return self.trade_day_list[i_day + ndays + 1: i_day + 1]


pandas.options.display.max_rows = 10

_trade_day = TradeDay()
is_trade_day = _trade_day.is_trade_day
get_close_trade_date_range = _trade_day.get_close_trade_day_range
get_n_trade_days = _trade_day.get_n_trade_days
get_nearby_trade_day = _trade_day.get_nearby_trade_day


def test():
    val = _trade_day.get_n_trade_days('2017-06-18', -1)
    assert_equal(val[0], '2017-06-16')
