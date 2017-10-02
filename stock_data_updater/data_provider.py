from typing import Dict

from common_stock.py_dataframe import DayDataRepr
from common_stock.stock_helper import handle_df_missing_values
from stock_data_updater.rq_data_fetcher import rq_history_bars


class DataProvider:
    def __init__(self):
        self.code_to_ddr = {}  # type: Dict[str, DayDataRepr]
        self.code_to_df = {}

    def _try_read_data(self, code):
        if not code in self.code_to_ddr:
            self.code_to_ddr[code] =  DayDataRepr(code,
                                                  handle_df_missing_values(rq_history_bars(code)))
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

    def ddr_of(self, code, len=None) -> DayDataRepr:
        ddr = self._try_read_data(code)
        if len:
            ddr = ddr.tail(len)
        return ddr

    def has_day_data(self, code, date_or_intday):
        if not isinstance(date_or_intday, int):
            date_or_intday = date_or_intday.year * 10000 + date_or_intday.month * 100 + date_or_intday.day
        return self.ddr_of(code).has_day(date_or_intday)


ddr_pv = DataProvider()


def main():
    val = ddr_pv.ddr_of('000001.XSHE')
    print(val.df)
    pass


if __name__ == '__main__':
    main()
