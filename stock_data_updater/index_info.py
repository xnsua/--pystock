import os
import threading
from typing import List

import pandas
from openpyxl import load_workbook

from common_stock.stock_helper import to_num_code


def read_xls_data(path) -> List[List]:
    import xlrd
    book = xlrd.open_workbook(path)
    sh = book.sheet_by_index(0)
    lo = []
    for rx in range(sh.nrows):
        li = []
        for x in sh.row(rx):
            li.append(x.value)
        lo.append(li)
    return lo


class IndexInfoProvider:
    def __init__(self, path):
        self.path = path
        self.code2component = {}
        self.lock = threading.Lock()

    def components_of(self, code):
        ncode = to_num_code(code)
        with self.lock:
            if code not in self.code2component:
                self.code2component[code] = self._data_of(ncode)
            return self.code2component[code]

    def path_of(self, index_code):
        return self.path + index_code + 'cons.xls'

    def _data_of(self, index_code):
        path = self.path_of(index_code)
        data = read_xls_data(path)
        column_data = list(zip(*data))

        comp_codes = None
        for column in column_data:
            if column[0].startswith('成分券代码'):
                comp_codes = list(column[1:])
            elif column[0].startswith('交易所'):
                market = column[1:]
        for i, value in enumerate(market):
            if value == 'Shanghai':
                comp_codes[i] = 'sh' + comp_codes[i]
            elif value == 'Shenzhen':
                comp_codes[i] = 'sz' + comp_codes[i]
        return comp_codes


gindex_pv = IndexInfoProvider(os.path.expanduser('~/StockData/index_data/'))


def main():
    val = gindex_pv.components_of('000001')
    print(val)


if __name__ == '__main__':
    main()
