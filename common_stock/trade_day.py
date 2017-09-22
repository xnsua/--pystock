import datetime
import datetime as dt
import os
import pickle
from copyreg import pickle

from common_stock import stock_cache_one_month


# ------- Print run time --------------


class TradeDay:
    def __init__(self):
        self.df = self._read_df()
        self.day_list = list(self.df.calendarDate)
        print(self.day_list)
        self.day_map = self._build_all_date_map()
        # The list is faster than pd.Series here
        self.trade_day_list = list(self.df.calendarDate[self.df.isOpen == 1])
        self.trade_day_map = self._build_trade_day_map()

        self._date_to_str = {}
        self._date_to_int = {}
        self._int_to_str = {}
        self._int_to_date = {}
        self._str_to_date = {}
        self._str_to_int = {}
        self.init_converter()

    def init_converter(self):
        daylist = list(self.df.calendarDate)
        for day_str in daylist:
            a, b, c = map(int, day_str.split('-'))
            date = dt.date(a, b, c)
            day_int = a * 10000 + b * 100 + c
            self._date_to_str[date] = day_str
            self._date_to_int[date] = day_int
            self._int_to_str[day_int] = day_str
            self._int_to_date[day_int] = date
            self._str_to_int[day_str] = day_int
            self._str_to_date[day_str] = date

    def date_to_str(self, date):
        return self._date_to_str[date]

    def date_to_int(self, date):
        return self._date_to_int[date]

    def int_to_str(self, day_int):
        return self._int_to_str[day_int]

    def int_to_date(self, day_int):
        return self._int_to_date[day_int]

    def str_to_int(self, day_str):
        return self._str_to_int[day_str]

    def str_to_date(self, day_str):
        return self._str_to_date[day_str]

    @staticmethod
    @stock_cache_one_month
    def _read_df():
        import tushare
        return tushare.trade_cal()

    def span_of(self, day1, day2):
        i1 = self.trade_day_map[day1]
        i2 = self.trade_day_map[day2]
        return i2 - i1

    def _build_trade_day_map(self):
        trade_day_map = {}
        for i, day in enumerate(self.trade_day_list):
            a, b, c = map(int, day.split('-'))
            day = a * 10000 + b * 100 + c
            self.trade_day_list[i] = day
            trade_day_map[day] = i
            trade_day_map[datetime.date(a, b, c)] = i

        return trade_day_map

    def _build_all_date_map(self):
        date_map = {}
        for i, day in enumerate(self.day_list):
            a, b, c = map(int, day.split('-'))
            day = a * 10000 + b * 100 + c
            self.day_list[i] = day
            date_map[day] = i
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

    def shift(self, date_, offset):
        if isinstance(date_, datetime.date):
            date_ = date_.year * 10000 + date_.month * 100 + date_.day
        i_trade_day = self.trade_day_map[date_]
        return self.trade_day_list[i_trade_day + offset]

    def range_list(self, start_date, end_date):
        if start_date not in self.trade_day_map:
            start_date = self.next(start_date)
        i_start_date = self.trade_day_map[start_date]
        if end_date not in self.trade_day_map:
            end_date = self.next(end_date)
        i_end_date = self.trade_day_map[end_date]
        return [self.trade_day_list[i] for i in range(i_start_date, i_end_date)]

    def close_range_list(self, start_date, end_date):
        return self.range_list(start_date, self.next(end_date))

    def range_len(self, start_date, end_date):
        i = self.day_map[start_date]
        j = self.day_map[end_date]
        return j - i


def get_gtrade_day():
    trade_day = None
    file_name = 'd:/gtr'
    if os.path.isfile(file_name):
        print('hhd')
        with open(file_name, 'rb') as file:
            # ------- Print run time --------------
            import datetime
            s_time = datetime.datetime.now()
            trade_day = pickle.load(file)
            print(datetime.datetime.now() - s_time)

    else:
        trade_day = TradeDay()
        print('hh')
        with open('d:/gtr', 'wb') as file:
            pickle.dump(trade_day, file)
    return trade_day


s_time = datetime.datetime.now()
# ------- Print run time --------------
import datetime

s_time = datetime.datetime.now()
gtrade_day = get_gtrade_day()
print(datetime.datetime.now() - s_time)




# def test():
#     # 24,25 is Saturday and Sunday
#     val = gtrade_day.next(20170624)
#     assert_equal(val, 20170626)
#     val = gtrade_day.next(20170626)
#     assert_equal(val, 20170627)
#
#     val = gtrade_day.previous(20170624)
#     assert_equal(val, 20170623)
#     val = gtrade_day.previous(20170627)
#     assert_equal(val, 20170626)
#
#     val = gtrade_day.shift(20170626, 2)
#     assert_equal(val, 20170628)
#     val = gtrade_day.shift(20170626, -2)
#     assert_equal(val, 20170622)
#
#     range_list = [i for i in gtrade_day.range_list(20170623, 20170626)]
#     assert_equal(range_list, [20170623])
#     range_list = [i for i in gtrade_day.range_list(20170623, 20170627)]
#     assert_equal(range_list, [20170623, 20170626])
#
#     range_list = [i for i in gtrade_day.close_range_list(20170623, 20170626)]
#     # 20170623 is Friday, 20170626 is Monday
#     assert_equal(range_list, [20170623, 20170626])
#
#     assert_equal(gtrade_day.span_of(20170623, 20170626), 1)
#     assert_equal(gtrade_day.span_of(20170623, 20170627), 2)
#
