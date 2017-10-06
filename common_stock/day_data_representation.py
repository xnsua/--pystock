import math

import numpy

from common.scipy_helper import pdDF


class DayK:
    def __init__(self, open_, close, high, low):
        self.open = open_
        self.close = close
        self.high = high
        self.low = low
        self.max_open_close = max(open_, close)
        self.min_open_close = min(open_, close)

    @property
    def low_shadow(self):
        return self.min_open_close - self.low

    @property
    def high_shadow(self):
        return self.high - self.max_open_close

    @property
    def body_height(self):
        return abs(self.open - self.close)

    @property
    def is_raise(self):
        return self.close > self.open

    @property
    def total_height(self):
        return self.high - self.low


class DayDataRepr:
    def __init__(self, code, df: pdDF):
        self.df = df
        self.code = code

        self.days = list(df.index.values.astype(numpy.int64))
        self.opens = list(map(float, df.open))
        self.closes = list(map(float, df.close))
        self.highs = list(map(float, df.high))
        self.lows = list(map(float, df.low))
        self.volumes = list(map(float, df.volume))

        self.day_to_index = dict(zip(self.days, range(len(self.days))))

        self.open_nparr = df.open.values
        self.close_nparr = df.close.values
        self.high_nparr = df.high.values
        self.low_nparr = df.low.values

    def __len__(self):
        return len(self.df)

    def index_of(self, day):
        return self.day_to_index[day]

    def open_of(self, day):
        return self.opens[self.day_to_index[day]]

    def close_of(self, day):
        return self.closes[self.day_to_index[day]]

    def high_of(self, day):
        return self.highs[self.day_to_index[day]]

    def low_of(self, day):
        return self.lows[self.day_to_index[day]]

    def volume_of(self, day):
        return self.volumes[self.day_to_index[day]]

    def k_line_of(self, day):
        index = self.day_to_index[day]
        return self.opens[index], self.closes[index], self.highs[index], self.lows[index]

    def first_day(self):
        return self.days[0]

    def last_day(self):
        return self.days[-1]

    def has_day(self, day):
        return day in self.day_to_index

    def clip(self, begin_day, end_day):
        ddr = DayDataRepr(self.code, self.df.loc[begin_day:end_day, :])
        return ddr

    def head(self, num):
        ddr = DayDataRepr(self.code, self.df.head(num))
        return ddr

    def tail(self, num):
        ddr = DayDataRepr(self.code, self.df.tail(num))
        return ddr

    def head(self, num):
        ddr = DayDataRepr(self.code, self.df.head(num))
        return ddr

    def section(self, date_begin, date_end):
        df = self.df.loc[date_begin:date_end, :]
        ddr = DayDataRepr(self.code, df)
        return ddr

    def dayk_of(self, day) -> DayK:
        index = self.day_to_index[day]
        return DayK(self.opens[index], self.closes[index], self.highs[index], self.lows[index])

    def ochl(self, index):
        return self.opens[index], self.closes[index], self.highs[index], self.lows[index]


class RealtimeDataRepr:
    def __init__(self, df):
        self.df = df
        #          open  yclose  price   high    low   name
        # 510900  1.141   1.147  1.134  1.143  1.133  H股ETF

    def price_of(self, stock_code):
        return self.df.price[stock_code]

    def open_of(self, stock_code):
        return self.df.open[stock_code]

    def yclose_of(self, stock_code):
        return self.df.yclose[stock_code]

    def high_of(self, stock_code):
        return self.df.high[stock_code]

    def low_of(self, stock_code):
        return self.df.low[stock_code]


class EmuRealTimeDataRepr(RealtimeDataRepr):
    def __init__(self):
        super().__init__(None)
        from stock_data_manager.data_provider import ddr_pv
        self.pv = ddr_pv
        self.day = None

    def open_of(self, stock_code):
        return self.pv.open(stock_code, self.day)

    def price_of(self, stock_code):
        return self.pv.open(stock_code, self.day)

    def close_of(self, stock_code):
        return self.pv.close(stock_code, self.day)

    def high_of(self, stock_code):
        return self.pv.high(stock_code, self.day)

    def low_of(self, stock_code):
        return self.pv.low(stock_code, self.day)

    def yclose_of(self, stock_code):
        from common_stock.__old.trade_day import gtrade_day
        return self.pv.close(stock_code, gtrade_day.previous(self.day))


def test_emu_realtime_datarepr():
    rdr = EmuRealTimeDataRepr()
    rdr.day = '2017-06-01'
    val = rdr.open_of('510900')
    assert math.isclose(val, 1.15)
