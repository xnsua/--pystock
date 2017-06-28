from typing import Dict

from gevent import threading

from common.data_structures.py_dataframe import DayDataRepr
from stock_data_updater.classify import all_etf_code_list
from stock_data_updater.day_data_updater import DayBarUpdater, read_etf_day_data, \
    read_stock_day_data


class DataProvider:
    def __init__(self):
        self.code2ddr = {}  # type: Dict[str, DayDataRepr]
        self.code2df = {}
        self.lock = threading.Lock()

    def _try_read_data(self, code):
        with self.lock:
            if code in self.code2ddr:
                return self.code2ddr[code]

            if code in all_etf_code_list:
                df = read_etf_day_data(code)
            else:
                df = read_stock_day_data(code)

            self.code2df[code] = df
            self.code2ddr[code] = DayDataRepr(df)
            return self.code2ddr[code]

    def open(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.open(day)

    def close(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.close(day)

    def high(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.high(day)

    def low(self, code, day):
        ddr = self._try_read_data(code)
        return ddr.low(day)

    def ddr(self, code) -> DayDataRepr:
        ddr = self._try_read_data(code)
        return ddr

gdata_provider = DataProvider()