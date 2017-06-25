import json
import re

import pandas as pd
from common.scipy_helper import pdDF
from common.web_helper import firefox_quick_get_url
from common_stock.common_stock_helper import pure_stock_code_to_sina_symbol, \
    stock_symbol_to_pure_stock_code
from common_stock.stock_config import stock_cache_one_month

pd.set_option('precision', 5)

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


def get_realtime_stock_infos(stock_list) -> pdDF:
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

    list_str = ','.join(map(pure_stock_code_to_sina_symbol, stock_list))
    url = 'http://hq.sinajs.cn/list=' + list_str
    resp = firefox_quick_get_url(url)
    if resp.status_code == 200:
        return extract_result(resp.text)
    raise Exception(
        f'In get_price:: status_code: {resp.status_code}, text: {resp.text[:100]}')


@stock_cache_one_month
def get_etf_info_dict():
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['8mqNVmdg4VG8cx0K']/Market_Center.getHQNodeDataSimple?page=1&num=280&sort=amount&asc=0&node=etf_hq_fund&%5Bobject%20HTMLDivElement%5D=nvdbj"
    resp = firefox_quick_get_url(url)
    # noinspection PyUnresolvedReferences
    text = re.search(']\((.*)\)', resp.text)[1]
    text = text.replace("symbol", '"symbol"')
    text = text.replace("name", '"name"')
    text = text.replace("trade", '"trade"')
    text = text.replace("pricechange", '"pricechange"')
    text = text.replace("changepercent", '"changepercent"')
    text = text.replace("buy", '"buy"')
    text = text.replace("sell", '"sell"')
    text = text.replace("settlement", '"settlement"')
    text = text.replace("open", '"open"')
    text = text.replace("high", '"high"')
    text = text.replace("low", '"low"')
    text = text.replace("volume", '"volume"')
    text = text.replace("amount", '"amount"')
    text = text.replace("code", '"code"')
    text = text.replace("ticktime", '"ticktime"')
    val = json.loads(text)
    # Return value like
    # [{'symbol': 'sh511990', 'name': '华宝添益', 'trade': '100.009', 'pricechange': '0.002',
    # 'changepercent': '0.002', 'buy': '100.009', 'sell': '100.010', 'settlement': '100.007',
    # 'open': '100.011', 'high': '100.014', 'low': '100.007', 'volume': 113663568, 'amount':
    # 11367471830, 'code': '511990', 'ticktime': '15:00:00'}, {
    return val


@stock_cache_one_month
def get_etf_sina_symbols():
    val = get_etf_info_dict()
    rval = [item['symbol'] for item in val]
    return rval




