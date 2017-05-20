import datetime
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later, ndays_ago
from common.my_old.cache_database import cache_db
from common.scipy_helper import pdDF
from common.simple_retry import SimpleRetry
from config_module import myconfig
from data_manager.stock_querier import w163_api
from stock_utility.stock_data_constants import stock_start_day
from stock_utility.trade_day import is_trade_day


class DayBar:
    @staticmethod
    def _etf_code_to_csv_filepath(etf_code):
        etf_code = etf_code.replace('SH.', '')
        etf_code = etf_code.replace('SZ.', '')
        path = myconfig.etf_day_data_dir
        filename = pl.Path(path) / (etf_code + '.csv')
        return filename

    @staticmethod
    def _stock_code_to_csv_filepath(stock_code):
        stock_code = stock_code.replace('SH.', '')
        stock_code = stock_code.replace('SZ.', '')
        path = myconfig.stock_day_data__dir
        filename = pl.Path(path) / (stock_code + '.csv')
        return filename

    @staticmethod
    def _update_k_data(stock_code: str, filename):
        try:
            df_read = pd.read_csv(filename, index_col='date')
            last_date = datetime.datetime.strptime(df_read.index.values[-1:][0],
                                             '%Y-%m-%d').date()
        except FileNotFoundError:
            df_read = pdDF()
            last_date = ndays_ago(1, stock_start_day)

        # Skip the non_trade_day
        query_start_date = ndays_later(1, last_date)
        while not is_trade_day(query_start_date):
            query_start_date = ndays_later(1, query_start_date)

        now = datetime.datetime.now()
        if now.date() < query_start_date:
            return df_read
        if now.date() == query_start_date and now.hour < 16:
            return df_read
        df_update = ts.get_k_data(stock_code, start=str(query_start_date))
        df_update.set_index('date', inplace=True)
        df_concat = pd.concat([df_read, df_update],
                              ignore_index=False)  # type: pdDF
        df_concat.to_csv(filename)
        return df_concat

    @classmethod
    def update_etf_day_data(cls, stock_code):
        filename = cls._etf_code_to_csv_filepath(stock_code)
        return cls._update_k_data(stock_code, filename)

    @classmethod
    def update_stock_day_data(cls, stock_code):
        filename = cls._stock_code_to_csv_filepath(stock_code)
        return cls._update_k_data(stock_code, filename)

    @classmethod
    def read_etf_day_data(cls, etf_code):
        filename = cls._etf_code_to_csv_filepath(etf_code)
        try:
            df_read = pd.read_csv(filename, index_col='date')
        except FileNotFoundError:
            df_read = pdDF()
        return df_read


def query_etf_info(etf_code):
    key = 'key_etf_' + etf_code
    val = cache_db.query_dict(key, ndays_ago(7))
    if val: return val

    retrier = SimpleRetry(max_retry_times=2, wait_base_time=3)
    info = retrier(w163_api.wget_etf_info)(etf_code)
    cache_db.update(key, str(info))
    return info

# </editor-fold>
