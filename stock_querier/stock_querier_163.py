import io

import pandas as pd

import common.helper
from utilities import stock_helper
from utilities.import_basic import *


# The 163 website add 0 to the stockcode to imply SH stock
# Add the 1 to the stockcode to imply the SZ stock
def download_stock_history(stockcode, savepath, startdate=stock_helper.stock_startday, enddate=dt.date.today()):
    df = wget_stock_history(stockcode, startdate, enddate)
    df.to_csv(savepath, encoding='gbk')


def wget_stock_history(stockcode, startdate=dt.datetime(1990, 1, 1), enddate=dt.datetime(2050, 1, 1)) -> pd.DataFrame:
    fmt163 = 'http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'

    url = fmt163.format(stockcode, startdate.strftime('%Y%m%d'), enddate.strftime('Y%m%d'))
    res = hp.firefox_get_url(url)
    content = res.content.decode(encoding='GBK')
    df = pd.read_csv(io.StringIO(content))
    return df


def main():
    download_stock_history('0000001', 'jqtt1.csv', startdate=common.helper.ndays_ago(5))


if __name__ == '__main__':
    main()
