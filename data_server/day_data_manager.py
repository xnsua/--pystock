import datetime as dt
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later, ndays_ago
from config_module import myconfig
from stock_basic import stock_helper
from stock_basic.stock_helper import stock_startday


def update_k_data(stockcode: str, path):
    stockcode = stockcode.replace('SH.', '')
    stockcode = stockcode.replace('SZ.', '')
    filename = pl.Path(path) / (stockcode + '.csv')
    try:
        dfread = pd.read_csv(filename, index_col='date')
        lastdate = dt.datetime.strptime(dfread.index.values[-1:][0],
                                        '%Y-%m-%d').date()
    except FileNotFoundError:
        dfread = pd.DataFrame()
        lastdate = ndays_ago(1, stock_startday)

    query_start_date = ndays_later(1, lastdate)
    now = dt.datetime.now()
    if now.date() == query_start_date and now.hour < 16:
        return dfread

    dfupdate = ts.get_k_data(stockcode, start=str(query_start_date))
    dfupdate.set_index('date', inplace=True)

    dfconcat = pd.concat([dfread, dfupdate],
                         ignore_index=False)  # type: pd.DataFrame
    dfconcat.to_csv(filename)
    return dfconcat


def update_etf():
    """ Return updated etf """
    etf_path = myconfig.stock_day_data_etf_path
    rval = {}
    for val in stock_helper.etf_t1:
        val = val[2:]
        rval[val] = update_k_data(val, etf_path)
    for val in stock_helper.etf_t0:
        val = val[2:]
        rval[val] = update_k_data(val, etf_path)
    return rval
