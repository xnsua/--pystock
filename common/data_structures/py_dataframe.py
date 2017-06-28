from contextlib import suppress

from common_stock.trade_day import TradeDay


class DayDataRepr:
    def __init__(self, df):
        self.df = df
        self.code = df.code[0]
        assert isinstance(self.code, str) and len(self.code) == 6
        self.index = list(df.index)
        with suppress(Exception):
            self.open = list(df.open)
            self.close = list(df.close)
            self.high = list(df.high)
            self.low = list(df.low)
            self.volume = list(df.volume)
        self.day2index = dict(zip(self.index, range(len(self.index))))

    def get_open(self, day):
        return self.open[self.day2index[day]]

    def get_close(self, day):
        return self.close[self.day2index[day]]

    def get_close_no_err(self, day):
        return self.close[self.day2index[day]]

    def get_high(self, day):
        return self.high[self.day2index[day]]

    def get_low(self, day):
        return self.low[self.day2index[day]]

    def get_volume(self, day):
        return self.volume[self.day2index[day]]

    def get_drop_cnt(self, day):
        return self.drop_cnts[self.day2index[day]]

    def get_rise_cnt(self, day):
        return self.rise_cnts[self.day2index[day]]

    def get_date_range(self, code):
        return range(self.index[0], TradeDay.get_nearby_trade_day(self.index[-1], 1,))

