from contextlib import suppress


class DayDataRepr:
    def __init__(self, df):
        self.df = df
        self.code = df.code[0]
        assert isinstance(self.code, str) and len(self.code) == 6
        self.day = list(df.index)
        with suppress(Exception):
            self.open = list(df.open)
            self.close = list(df.close)
            self.high = list(df.high)
            self.low = list(df.low)
            self.volume = list(df.volume)
        self.day2index = dict(zip(self.day, range(len(self.day))))

    def open_of(self, day):
        return self.open_of[self.day2index[day]]

    def close_of(self, day):
        return self.close_of[self.day2index[day]]

    def high_of(self, day):
        return self.high_of[self.day2index[day]]

    def low_of(self, day):
        return self.low_of[self.day2index[day]]

    def volume_of(self, day):
        return self.volume_of[self.day2index[day]]

    def first_day(self):
        return self.day[0]

    def last_day(self):
        return self.day[-1]
