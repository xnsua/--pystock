from typing import Dict

from common.data_structures.py_dataframe import DayDataRepr
from stock_data_updater.classify import all_etf_code_list
from stock_data_updater.day_data_updater import DayBarUpdater, read_etf_day_data, \
    read_stock_day_data


class DataProvider:
    def __init__(self):
        self.code2ddr = {}  # type: Dict[str, DayDataRepr]
        self.code2df = {}

        pass

    def _try_read_data(self, code):
        if code in self.code2df:
            return
        if code in all_etf_code_list:
            df = read_etf_day_data(code)
        else:
            df = read_stock_day_data(code)
        self.code2df[code] = df
        self.code2ddr[code] = DayDataRepr(df)

    def get_open(self, code, day):
        self._try_read_data(code)
        return self.code2ddr[code].get_open(day)

    def get_close(self, code, day):
        self._try_read_data(code)
        return self.code2ddr[code].get_close(day)

    def get_high(self, code, day):
        self._try_read_data(code)
        return self.code2ddr[code].get_high(day)

    def get_low(self, code, day):
        self._try_read_data(code)
        return self.code2ddr[code].get_low(day)
