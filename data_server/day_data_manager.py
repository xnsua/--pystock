import datetime as dt
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later, ndays_ago
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
    # toch
    # Return if there is no new data
    now = dt.datetime.now()
    if now.date() == query_start_date and now.hour < 17:
        return dfread

    dfupdate = ts.get_k_data(stockcode, start=str(query_start_date))
    dfupdate = dfupdate.set_index('date')

    dfconcat = pd.concat([dfread, dfupdate],
                         ignore_index=False)  # type: pd.DataFrame
    dfconcat.to_csv(filename)
    return dfconcat
