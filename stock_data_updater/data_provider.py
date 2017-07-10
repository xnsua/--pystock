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
        self.code2ddr = {}  # type: Dict[str, DayDataRepr]
        self.code2df = {}
        self.lock = threading.Lock()

    def _try_read_data(self, code):
        with self.lock:
            if not code in self.code2ddr:
                self.code2ddr[code] = grq_data.ddr_of(code)
            return self.code2ddr[code]

            # if code in self.code2ddr:
            #     return self.code2ddr[code]
            # # use 'i000001' to indicate index
            # if len(code) == 7:
            #     df = read_index_day_data(code[1:])
            # elif code in etf_code2name:
            #     df = read_etf_day_data(code)
            # else:
            #     df = read_stock_day_data(code)
            #
            # self.code2df[code] = df
            # self.code2ddr[code] = DayDataRepr(df)
            # return self.code2ddr[code]

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

    def has_data(self, code, day):
        return self.ddr(code).has_day(day)

    def component_of(self, code):
        return gindex_pv.components_of(code)

    def symbol2code(self, symbol):
        return grq_data.symbol2code(symbol)


gdata_pv = DataProvider()


def main():
    # print(gdata_pv.component_of('000001'))
    print(gdata_pv)
    pass


if __name__ == '__main__':
    main()
