import datetime as dt

import tushare as ts

from common.helper import remove_ifexist
from config_module import myconfig
from stock_basic.stock_constant import str_stock_startday


def get_k_data(stockcode):
    today_date = dt.date.today()
    df = ts.get_k_data(stockcode, start=str_stock_startday, end=str(today_date))
    df2 = df.set_index('date')
    filename = myconfig.stock_day_data_etf_path / (stockcode + '.csv')
    remove_ifexist(filename)
    df2.to_csv(filename)


def func(vv, **kwargs):
    print(vv)
    print(kwargs)
    pass


def main():
    func({'vv': 'aa', 'cc': 'dd'})

    # get_k_data('000001')
    # print(str(stock_startday))


if __name__ == '__main__':
    main()
