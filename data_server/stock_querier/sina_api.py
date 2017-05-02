import datetime as dt
import re

from common.web_helper import firefox_quick_get_url
from stock_basic.stock_helper import etf_t1

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


# def get_real_time_price(stocklist):
#     stockprices = get_realtime_stock_info(stocklist)
#     stockprices = list(stockprices.price)
#     return stockprices


def get_realtime_stock_info(stock_list):
    def extract_result(contentlist: str):
        fiter = re.finditer(r'var hq_str_(..\d{6})="(.*)";', contentlist)
        # print(contentlistist)
        # fiter = re.finditer(r'var', contentlist)
        stockcodes = []
        attrs = []
        for v in fiter:
            stockcodes.append(v[1])
            content = v[2].split(',')
            content = content[0:6]
            content.append(content.pop(0))
            attrs.append(content)
        df = pd.DataFrame(attrs, index=stockcodes, columns=_column_names,
                          dtype=float)
        df['name'] = df['name'].astype(str)
        return df

    liststr = ','.join(stock_list)
    url = 'http://hq.sinajs.cn/list=' + liststr
    resp = firefox_quick_get_url(url)
    if resp.status_code == 200:
        return extract_result(resp.text)
    raise Exception(
        f'In get_price:: status_code: {resp.status_code}, text: {resp.text[:100]}')


import pandas as pd

pd.set_option('precision', 5)


def main():
    while 1:
        sstime = dt.datetime.now()
        ret = get_realtime_stock_info('sh' + v for v in etf_t1)
        print(dt.datetime.now() - sstime)


if __name__ == '__main__':
    main()
