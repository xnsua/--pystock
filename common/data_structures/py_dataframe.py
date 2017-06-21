from contextlib import suppress


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
        self.day_index = dict(zip(self.index, range(len(self.index))))

        self.rise_cnts = None
        self.drop_cnts = None

    def get_open(self, day):
        return self.open[self.day_index[day]]

    def get_close(self, day):
        return self.close[self.day_index[day]]

    def get_close_no_err(self, day):
        return self.close[self.day_index[day]]

    def get_high(self, day):
        return self.high[self.day_index[day]]

    def get_low(self, day):
        return self.low[self.day_index[day]]

    def get_volume(self, day):
        return self.volume[self.day_index[day]]

    def get_drop_cnt(self, day):
        return self.drop_cnts[self.day_index[day]]

    def get_rise_cnt(self, day):
        return self.rise_cnts[self.day_index[day]]
