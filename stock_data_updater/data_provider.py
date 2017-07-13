import datetime
import os
import threading
from typing import Dict

from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy

from common_stock.py_dataframe import DayDataRepr
from stock_data_updater.index_info import gindex_pv
from stock_data_updater.rq_data_proxy import grq_data

dp = DataProxy(BaseDataSource(os.path.expanduser('~/.rqalpha/bundle')))


class DataProvider:
    def __init__(self):
        self.code_to_ddr = {}  # type: Dict[str, DayDataRepr]
        self.code_to_df = {}
        self.lock = threading.Lock()

    def _try_read_data(self, code):
        # with self.lock:
            if not code in self.code_to_ddr:
                self.code_to_ddr[code] = grq_data.ddr_of(code)
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

    def ddr(self, code) -> DayDataRepr:
        ddr = self._try_read_data(code)
        return ddr

    def has_day_data(self, code, day):
        if not isinstance(day, int):

            day = day.year * 10000 + day.month * 100 + day.day
        return self.ddr(code).has_day(day)

    def components_of(self, code):
        return gindex_pv.components_of(code)

    def symbol_to_code(self, symbol):
        return grq_data.symbol_to_code(symbol)

    def name_of(self, symbol, default = None):
        return grq_data.name_of(symbol, default)


gdp = DataProvider()


def main():
    # print(gdata_pv.component_of('000001'))
    # print(gdata_pv.open('sh000001',20170705))
    # for name in main_index:
    #     print(gdata_pv.symbol_to_code(name))
    pass


if __name__ == '__main__':
    main()
