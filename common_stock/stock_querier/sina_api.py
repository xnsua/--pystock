import datetime
import re

from common.scipy_helper import pdDF
from common.web_helper import firefox_quick_get_url
from common_stock.common_stock_helper import pure_stock_code_to_sina_symbol_code, \
    stock_symbol_to_pure_stock_code
from common_stock.stock_config import stock_cache_one_month

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


def get_realtime_stock_info(stock_list) -> pdDF:
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
    resp = firefox_quick_get_url(url)
    if resp.status_code == 200:
        return extract_result(resp.text)
    raise Exception(
        f'In get_price:: status_code: {resp.status_code}, text: {resp.text[:100]}')


@stock_cache_one_month
def get_etf_scode_list():
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['8mqNVmdg4VG8cx0K']/Market_Center.getHQNodeDataSimple?page=1&num=280&sort=amount&asc=0&node=etf_hq_fund&%5Bobject%20HTMLDivElement%5D=nvdbj"
    resp = firefox_quick_get_url(url)
    codes = re.finditer('symbol:"(..\d{6})', resp.text)
    codes = [val[1] for val in codes]
    return codes


import pandas as pd

pd.set_option('precision', 5)


def main():
    s_time = datetime.datetime.now()
    get_etf_scode_list()
    print(datetime.datetime.now() - s_time)
    # ret = get_realtime_stock_info('sh' + v for v in ['510900'])
    # print(dt_now())
    # print(ret.dtypes)
    # print(ret.ix[0, 'price'])


if __name__ == '__main__':
    main()
