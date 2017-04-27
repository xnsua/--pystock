import datetime as dt
import io

import pandas as pd
import requests

import common.helper
from common.web_helper import firefox_get_url
from utilities import stock_helper


# The 163 website add 0 to the stockcode to imply SH stock
# Add the 1 to the stockcode to imply the SZ stock
def download_stock_history(stockcode, savepath,
                           startdate=stock_helper.stock_startday,
                           enddate=dt.date.today()):
    # noinspection PyTypeChecker
    df = wget_stock_history(stockcode, startdate, enddate)
    df.to_csv(savepath, encoding='gbk')


def wget_stock_history(stockcode, startdate=dt.datetime(1990, 1, 1),
                       enddate=dt.datetime(2050, 1, 1)) -> pd.DataFrame:
    fmt163 = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

    url = fmt163.format(stockcode, startdate.strftime('%Y%m%d'),
                        enddate.strftime('%Y%m%d'))
    res = firefox_get_url(requests.Session(), url)
    content = res.content.decode(encoding='GBK')
    df = pd.read_csv(io.StringIO(content))
    return df


def main():
    download_stock_history('utfile0000001', 'jqtt1.csv',
                           startdate=common.helper.ndays_ago(5))


if __name__ == '__main__':
    main()
