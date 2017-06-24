import datetime
import pathlib
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later_from, ndays_ago_from
from common.scipy_helper import pdDF
from common_stock.common_stock_helper import stock_start_day
from common_stock.stock_config import stock_trade_over_cache
from common_stock.trade_day import is_trade_day
from project_helper.config_module import myconfig
from project_helper.logbook_logger import mylog
from stock_data.classify import sz50s, hs300s, zz500s, all_stock_index_list, all_etf_code_list


class StockUpdater:
    @staticmethod
    def _etf_code_to_csv_filepath(etf_code):
        etf_code = etf_code.replace('SH.', '')
        etf_code = etf_code.replace('SZ.', '')
        path = myconfig.etf_day_data_dir  # type: pathlib.Path
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
        df_concat.to_csv(str(filename))
        return df_concat

    @classmethod
    def update_etf_day_data(cls, stock_code):
        filename = cls._etf_code_to_csv_filepath(stock_code)
        return cls._update_k_data(stock_code, filename)

    @classmethod
    def update_index_data(cls, index):
        filename = cls._index_code_to_csv_filepath(index)
        return cls._update_k_data(index, filename, index=True)

    @classmethod
    def update_stock_day_data(cls, stock_code):
        filename = cls._stock_code_to_csv_filepath(stock_code)
        return cls._update_k_data(stock_code, filename)

    @classmethod
    def read_etf_day_data(cls, etf_code):
        filename = cls._etf_code_to_csv_filepath(etf_code)
        try:
            df_read = pd.read_csv(filename, index_col='date', dtype={'code': str})
        except FileNotFoundError:
            df_read = pdDF()
        return df_read


class DayBarUpdater:
    @classmethod
    @stock_trade_over_cache
    def update_800s(cls):
        d50 = sz50s
        d300 = hs300s
        d500 = zz500s
        d50.update(d300)
        d50.update(d500)
        for code in d50:
            StockUpdater.update_stock_day_data(code)

    @classmethod
    @stock_trade_over_cache
    def update_all_etfs(cls):
        for code in all_etf_code_list:
            try:
                StockUpdater.update_etf_day_data(code)
            except Exception as e:
                mylog.info(f'Update etf {code} failed: {e}')

    @classmethod
    @stock_trade_over_cache
    def update_stock_index(cls):
        for index in all_stock_index_list:
            try:
                StockUpdater.update_index_data(index)
            except Exception as e:
                mylog.info(f'Update index {index} failed: {e}')

    @classmethod
    @stock_trade_over_cache
    def update_all(cls):
        cls.update_800s()
        cls.update_all_etfs()
        cls.update_stock_index()


def test():
    DayBarUpdater.update_all_etfs()
