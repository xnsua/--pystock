import datetime as dt
import io

import pandas as pd
import pyquery
import requests

# The 163 website add 0 to the stock_code to imply SH stock_utility
# Add the 1 to the stock_code to imply the SZ stock_utility
from common.scipy_helper import pdDF
from common.web_helper import firefox_get_url
from stock_utility import stock_data_constants
from trading.base_structure.trade_constants import StockTermConstant


def download_stock_history(stock_code, save_path,
                           start_date=stock_data_constants.stock_start_day,
                           end_date=dt.date.today()):
    # noinspection PyTypeChecker
    df = wget_stock_history(stock_code, start_date, end_date)
    df.to_csv(save_path, encoding='gbk')


def wget_stock_history(stock_code, start_date=dt.datetime(1990, 1, 1),
                       end_date=dt.datetime(2050, 1, 1)) -> pdDF:
    fmt163 = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

    url = fmt163.format(stock_code, start_date.strftime('%Y%m%d'),
                        end_date.strftime('%Y%m%d'))
    print(url)
    res = firefox_get_url(requests.Session(), url)
    content = res.content.decode(encoding='GBK')
    df = pd.read_csv(io.StringIO(content))
    return df


def wget_etf_info(etf_code):
    # http://quotes.money.163.com/fund/159917.html
    url = f'http://quotes.money.163.com/fund/{etf_code}.html'
    resp = firefox_get_url(requests.session(), url)
    dom = pyquery.PyQuery(resp.text)
    text = (dom('body > div > div.fn_data_title').text())
    parts = text.split(' ')
    net_assert = parts[(parts.index('总净资产:')) + 1]
    net_assert = net_assert.replace(',', '')
    if net_assert.find('万') != -1:
        net_assert = float(net_assert.replace('万', '')) * 10000
    elif net_assert.find('亿') != -1:
        net_assert = float(net_assert.replace('亿', '')) * 10000 * 10000
    else:
        raise Exception(f'Query etf info for {etf_code} failed, text is {text}')
    return {StockTermConstant.scale: net_assert}


def main():
    wget_etf_info('510900')
    # get_etf_info('510900')
    pass


if __name__ == '__main__':
    main()
