import datetime
import pathlib as pl

import pandas as pd
import requests
import tushare
import tushare as ts

from common.helper import ndays_later_from, ndays_ago_from, dt_day_delta
from common.scipy_helper import pdDF
from common.timing import time_this
from common_stock.common_stock_helper import stock_start_day
from common_stock.stock_config import stock_cache
from common_stock.stock_data import etf_with_amount
from common_stock.trade_day import is_trade_day
from project_helper.config_module import myconfig
from project_helper.logbook_logger import mylog


class DayBar:
    @staticmethod
    def _etf_code_to_csv_filepath(etf_code):
        etf_code = etf_code.replace('SH.', '')
        etf_code = etf_code.replace('SZ.', '')
        path = myconfig.etf_day_data_dir
        filename = pl.Path(path) / (etf_code + '.csv')
        return filename

    @staticmethod
    def _index_code_to_csv_filepath(index):
        index = index.replace('SH.', '')
        index = index.replace('SZ.', '')
        path = myconfig.index_day_data_dir
        filename = pl.Path(path) / (index + '.csv')
        return filename

    @staticmethod
    def _stock_code_to_csv_filepath(stock_code):
        stock_code = stock_code.replace('SH.', '')
        stock_code = stock_code.replace('SZ.', '')
        path = myconfig.stock_day_data__dir
        filename = pl.Path(path) / (stock_code + '.csv')
        return filename

    @staticmethod
    def _update_k_data(stock_code: str, filename, index=False):
        try:
            df_read = pd.read_csv(filename, index_col='date')
            last_date = datetime.datetime.strptime(df_read.index.values[-1:][0],
                                                   '%Y-%m-%d').date()
        except FileNotFoundError:
            df_read = pdDF()
            last_date = ndays_ago_from(stock_start_day, 1)

        # Skip the non_trade_day
        query_start_date = ndays_later_from(last_date, 1)
        while not is_trade_day(query_start_date):
            query_start_date = ndays_later_from(query_start_date, 1)

        now = datetime.datetime.now()
        if now.date() < query_start_date:
            return df_read
        if now.date() == query_start_date and now.hour < 16:
            return df_read
        print(f'Updating using web for {stock_code}')
        df_update = ts.get_k_data(stock_code, start=str(query_start_date), index=index)
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
    def update_index_data(cls, index):
        filename = cls._etf_code_to_csv_filepath(index)
        return cls._update_k_data(index, filename, index=True)

    @classmethod
    @time_this
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


class DayBarUpdater:
    @classmethod
    @stock_cache(day_boundary=datetime.time(17, 0, 0), cache_days=1)
    def update_etfs_with_amount(cls):
        try:
            for code in etf_with_amount:
                DayBar.update_etf_day_data(code)
        except requests.exceptions.RequestException as e:
            mylog.info(e)

    @classmethod
    @stock_cache(cache_timedelta=dt_day_delta(100))
    def update_sz50_component(cls):
        df1 = tushare.get_sz50s()
        code_dict = dict(zip(df1.code, df1.name))
        return code_dict

    @classmethod
    @stock_cache(cache_timedelta=dt_day_delta(100))
    def update_hs300_component(cls):
        df2 = tushare.get_hs300s()
        code_dict = dict(zip(df2.code, df2.name))
        return code_dict

    @classmethod
    @stock_cache(cache_timedelta=dt_day_delta(100))
    def update_zz500_component(cls):
        df3 = tushare.get_zz500s()
        code_dict = dict(zip(df3.code, df3.name))
        return code_dict

    @classmethod
    @stock_cache(day_boundary=datetime.time(17, 0, 0), cache_days=1)
    def update_800(cls):
        d50 = cls.update_sz50_component()
        d300 = cls.update_hs300_component()
        d500 = cls.update_zz500_component()
        d50.update(d300)
        d50.update(d500)
        for code in d50:
            DayBar.update_stock_day_data(code)

    @classmethod
    @stock_cache(day_boundary=datetime.time(17, 0, 0), cache_days=1)
    def update_all(cls):
        cls.update_800()
        cls.update_etfs_with_amount()

# PersistentCache.clear_cache()
# PersistentCache.print_cache_data()
# toch run this
# val = DayBarUpdater.update_all()
# DayBarUpdater.update_etfs_with_amount()
