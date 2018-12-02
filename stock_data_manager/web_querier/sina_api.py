import json
import re
from collections import OrderedDict

import pandas as pd

from common.scipy_helper import pdDF
from common.web_helper import firefox_quick_get_url
from common_stock import stock_cache_one_month
from common_stock.stock_helper import CodeTools
from project_config.config_module import STOCK_MARGIN_MARGIN_TRADING_PATH

pd.set_option('precision', 5)

_column_names = ['open', 'yclose', 'price', 'high', 'low', 'name']


def get_realtime_stock_infos(stock_list) -> pdDF:
    #          open  yclose  price   high    low   name
    # 510900  1.141   1.147  1.134  1.143  1.133  H股ETF
    def extract_result(content_list: str):
        find_results = re.finditer(r'var hq_str_(..\d{6})="(.*)";', content_list)
        stock_codes = []
        attrs = []
        for v in find_results:
            stock_codes.append(CodeTools.to_pcode(v[1]))
            content = v[2].split(',')
            content = content[0:6]
            content.append(content.pop(0))
            attrs.append(content)
        df = pdDF(attrs, index=stock_codes, columns=_column_names,
                  dtype=float)
        df['name'] = df['name'].astype(str)
        return df

    list_str = ','.join(map(CodeTools.to_sina_code, stock_list))
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


# @stock_cache_one_sec
@stock_cache_one_month
def get_etf_sina_symbols():
    val = get_etf_info_dict()
    symbol = [item['symbol'] for item in val]
    names = [item['name'] for item in val]
    return OrderedDict(zip(symbol, names))


class NoMarginInfo(Exception): pass


def get_margin_info(code, start_date, end_date):
    code = CodeTools.to_sina_code(code)
    urlpattern = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?" \
                 "symbol={}&bdate={}&edate={}"
    url = urlpattern.format(code, start_date, end_date)
    print(url)
    resp = firefox_quick_get_url(url)
    text = (resp.content.decode('gbk'))
    vals = re.findall(r'<tr class="head">\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n.+\n\n .+</tr>',
                      text)

    ll = []
    for val in vals:
        items = re.findall(r'<td style="background-color:#ffffff">(.+)</td>', val)
        ll.append(items)

    if not ll:
        raise NoMarginInfo()
    df = pd.DataFrame(data=ll)
    df.columns = ['index', 'date', 'zbalance', 'zbuy_amount', 'zreturn_amount',
                  'qremain_amount', 'qremain_vol', 'qsell_vol',
                  'qreturn_vol', 'qbalance']
    df = df.drop(['index'], axis=1)
    df.date = df.date.apply(lambda x: int(x.replace('-', '')))
    return df


def crawl_margin_info(codes, start_date=None, end_date=None):
    import random
    import time
    save_path = STOCK_MARGIN_MARGIN_TRADING_PATH
    if start_date is None:
        start_date = 20100101
    for code in codes:
        code = CodeTools.to_pcode(code)
        try:
            df = get_margin_info(code, start_date, end_date)  # type: pdDF
            filename = save_path / (code + '.csv')
            df.to_csv(filename)
        except:
            pass
        sleep_time = (1 + random.random()) * 1.5
        time.sleep(sleep_time)
    return

def main():
    pass

if __name__ == '__main__':
    main()