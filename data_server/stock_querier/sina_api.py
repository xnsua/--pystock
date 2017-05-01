import datetime as dt
import re

import pandas as pd

from common.web_helper import firefox_quick_get_url
from stock_basic.stock_constant import etf_t1

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


def get_price(stocklist):
    stockprices = get_realtime_stock_info(stocklist)
    stockprices = list(stockprices.price)
    return stockprices


def get_realtime_stock_info(stock_list):
    def extract_result(contentlist: str):
        fiter = re.finditer(r'var hq_str_(sh\d{6})="(.*)";', contentlist)
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
    sstime = dt.datetime.now()
    resp = firefox_quick_get_url(url)
    print(dt.datetime.now() - sstime)
    if resp.status_code == 200:
        return extract_result(resp.text)
    raise Exception(
        f'In get_price:: status_code: {resp.status_code}, text: {resp.text[:100]}')


def main():
    sstime = dt.datetime.now()
    # ret = get_price(['sh601003', 'sh601001'])
    ret = get_price('sh' + v[3:] for v in etf_t1)
    print(ret)
    print(dt.datetime.now() - sstime)


if __name__ == '__main__':
    main()
