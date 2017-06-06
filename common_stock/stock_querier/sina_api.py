import re
import time

from common.helper import dt_now
from common.scipy_helper import pdDF
from common.web_helper import firefox_quick_get_url
from common_stock.stock_codes_format import pure_stock_code_to_sina_symbol_code, \
    stock_symbol_to_pure_stock_code
from project_helper.logbook_logger import jqd

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


def get_realtime_stock_info(stock_list):
    def extract_result(content_list: str):
        find_results = re.finditer(r'var hq_str_(..\d{6})="(.*)";', content_list)
        stock_codes = []
        attrs = []
        for v in find_results:
            stock_codes.append(stock_symbol_to_pure_stock_code(v[1]))
            content = v[2].split(',')
            content = content[0:6]
            content.append(content.pop(0))
            attrs.append(content)
        df = pdDF(attrs, index=stock_codes, columns=_column_names,
                  dtype=float)
        df['name'] = df['name'].astype(str)
        return df

    list_str = ','.join(map(pure_stock_code_to_sina_symbol_code, stock_list))
    url = 'http://hq.sinajs.cn/list=' + list_str
    jqd(url)
    resp = firefox_quick_get_url(url)
    if resp.status_code == 200:
        return extract_result(resp.text)
    raise Exception(
        f'In get_price:: status_code: {resp.status_code}, text: {resp.text[:100]}')


import pandas as pd

pd.set_option('precision', 5)


def main():
    while 1:
        ret = get_realtime_stock_info('sh' + v for v in ['510900'])
        time.sleep(1000)
        print(dt_now())
        print(ret.ix[0, 'price'])


if __name__ == '__main__':
    main()
