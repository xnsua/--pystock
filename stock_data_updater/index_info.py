import os
from typing import List

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
    main_index_symbol = ['上证指数', '上证180', '上证50', '上证380', '沪深300', '深证成指', '深证100R', '中小板指', '红利指数', '中证红利',
                          '中证500']
    def __init__(self, path):
        self.path = path
        self.code_to_component = {}

    def components_of(self, code):
        ncode = to_num_code(code)
        if code not in self.code_to_component:
            self.code_to_component[code] = self._data_of(ncode)
        return self.code_to_component[code]

    def _path_of(self, index_code):
        return self.path + index_code + 'cons.xls'

    def _data_of(self, index_code):
        path = self._path_of(index_code)
        data = read_xls_data(path)
        column_data = list(zip(*data))

        comp_codes = None
        for column in column_data:
            if column[0].startswith('成分券代码'):
                comp_codes = list(column[1:])
            elif column[0].startswith('交易所'):
                market = column[1:]
        # noinspection PyUnboundLocalVariable
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
