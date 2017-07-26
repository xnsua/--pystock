import math

from common_stock.trade_day import gtrade_day


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
        return abs(self.open-self.close)

    @property
    def is_raise(self):
        return self.close > self.open

    @property
    def total_height(self):
        return self.high - self.low

class DayDataRepr:
    def __init__(self, code, df):
        self.df = df
        self.code = code
        self.days = list(df.index)
        self.open = list(map(float, df.open))
        self.close = list(map(float, df.close))
        self.high = list(map(float, df.high))
        self.low = list(map(float, df.low))
        self.volume = list(map(float, df.volume))
        self.day_to_index = dict(zip(self.days, range(len(self.days))))

    def open_of(self, day):
        return self.open[self.day_to_index[day]]

    def close_of(self, day):
        return self.close[self.day_to_index[day]]

    def high_of(self, day):
        return self.high[self.day_to_index[day]]

    def low_of(self, day):
        return self.low[self.day_to_index[day]]

    def volume_of(self, day):
        return self.volume[self.day_to_index[day]]

    def k_line_of(self, day):
        index = self.day_to_index[day]
        return self.open[index], self.close[index], self.high[index], self.low[index]

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

    def dayk_of(self, day)->DayK:
        index = self.day_to_index[day]
        return DayK(self.open[index], self.close[index], self.high[index], self.low[index])



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
        from stock_data_updater.data_provider import gdp
        self.pv = gdp
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
        return self.pv.close(stock_code, gtrade_day.previous(self.day))


def test_emu_realtime_datarepr():
    rdr = EmuRealTimeDataRepr()
    rdr.day = '2017-06-01'
    val = rdr.open_of('510900')
    assert math.isclose(val, 1.15)
