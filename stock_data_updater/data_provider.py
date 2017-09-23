from typing import Dict

from common_stock.py_dataframe import DayDataRepr
from stock_data_updater.rq_data_fetcher import rq_history_bars


class DataProvider:
    def __init__(self):
        self.code_to_ddr = {}  # type: Dict[str, DayDataRepr]
        self.code_to_df = {}

    def _try_read_data(self, code):
        if not code in self.code_to_ddr:
            self.code_to_ddr[code] = DayDataRepr(code, rq_history_bars(code))
        return self.code_to_ddr[code]


    def open(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.open_of(day)

    def close(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.close_of(day)

    def high(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.high_of(day)

    def low(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.low_of(day)

    def ddr_of(self, code) -> DayDataRepr:
        ddr = self._try_read_data(code)
        return ddr

    def has_day_data(self, code, date_or_intday):
        if not isinstance(date_or_intday, int):
            date_or_intday = date_or_intday.year * 10000 + date_or_intday.month * 100 + date_or_intday.day
        return self.ddr_of(code).has_day(date_or_intday)

data_provider = DataProvider()


def main():
    val = data_provider.ddr_of('000001.XSHE')
    print(val.df)
    pass


if __name__ == '__main__':
    main()
