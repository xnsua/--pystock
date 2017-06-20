from contextlib import suppress


class DayDataRepr:
    def __init__(self, df):
        self.df = df
        self.code = df.code[0]
        self.index = list(df.index)
        with suppress(Exception):
            self.open = list(df.open)
            self.close = list(df.close)
            self.high = list(df.high)
            self.low = list(df.low)
            self.volume = list(df.volume)
        self.day_index = None

        self.rise_cnt = None
        self.drop_cnt = None

    def _idx(self, day):
        if not self.day_index:
            self.day_index = dict(zip(self.index, range(len(self.index))))
        return self.day_index[day]

    def get_open(self, day):
        return self.open(self.day_index[day])

    def get_close(self, day):
        return self.close(self.day_index[day])

    def get_high(self, day):
        return self.high(self.day_index[day])

    def get_low(self, day):
        return self.low(self.day_index[day])

    def get_volume(self, day):
        return self.volume(self.day_index[day])
