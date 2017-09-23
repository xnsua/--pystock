import threading
from typing import Dict

from common_stock.py_dataframe import DayDataRepr
# from stock_data_updater.index_info import gindex_pv
# from stock_data_updater.rq_data_proxy import grq_data
#
# dp = DataProxy(BaseDataSource(os.path.expanduser('~/.rqalpha/bundle')))
from common_stock.stock_helper import to_pcode
from stock_data_updater.rq_data_fetcher import rq_history_bars


class DataProvider:
    def __init__(self):
        self.code_to_ddr = {}  # type: Dict[str, DayDataRepr]
        self.code_to_df = {}
        self.lock = threading.Lock()

    def _try_read_data(self, code):
        # with self.lock:
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

    def has_day_data(self, code, day):
        if not isinstance(day, int):

            day = day.year * 10000 + day.month * 100 + day.day
        return self.ddr_of(code).has_day(day)

    def symbol_to_code(self, symbol):
        return r

    def name_of(self, pcode, default = None):
        pcode = to_pcode(symbol)
        return (symbol, default)

    def is_etf(self, stdcode):
        return grq_data.is_etf(stdcode)


gdp = DataProvider()


def main():
    gdp.ddr_of('sh000001')
    pass


if __name__ == '__main__':
    main()
