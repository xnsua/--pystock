import datetime as dt
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later, ndays_ago
from config_module import myconfig
from stock_basic import stock_helper
from stock_basic.stock_helper import stock_start_day, is_trade_day


def update_k_data(stock_code: str, path):
    stock_code = stock_code.replace('SH.', '')
    stock_code = stock_code.replace('SZ.', '')
    filename = pl.Path(path) / (stock_code + '.csv')
    try:
        df_read = pd.read_csv(filename, index_col='date')
        last_date = dt.datetime.strptime(df_read.index.values[-1:][0],
                                         '%Y-%m-%d').date()
    except FileNotFoundError:
        df_read = pd.DataFrame()
        last_date = ndays_ago(1, stock_start_day)

    # Skip the non_trade_day
    query_start_date = ndays_later(1, last_date)
    while not is_trade_day(query_start_date):
        query_start_date = ndays_later(1, query_start_date)

    now = dt.datetime.now()
    if now.date() < query_start_date:
        return df_read
    if now.date() == query_start_date and now.hour < 16:
        return df_read

    df_update = ts.get_k_data(stock_code, start=str(query_start_date))
    df_update.set_index('date', inplace=True)
    df_concat = pd.concat([df_read, df_update],
                          ignore_index=False)  # type: pd.DataFrame
    df_concat.to_csv(filename)
    return df_concat


# <editor-fold desc="Etf">
def read_etf_history(stock_code):
    stock_code = stock_code.replace('SH.', '')
    stock_code = stock_code.replace('SZ.', '')
    path = myconfig.stock_day_data_etf_path
    filename = pl.Path(path) / (stock_code + '.csv')
    try:
        df_read = pd.read_csv(filename, index_col='date')
    except FileNotFoundError:
        df_read = pd.DataFrame()
    return df_read


def update_etf_histories():
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


def read_etf_histories():
    rval = {}
    for val in stock_helper.etf_t1:
        val = val[2:]
        rval[val] = read_etf_history(val)
    for val in stock_helper.etf_t0:
        val = val[2:]
        rval[val] = read_etf_history(val)
    return rval


def read_etf_infos():
    pass

# </editor-fold>
