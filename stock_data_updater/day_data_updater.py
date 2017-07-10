import datetime
import pathlib
import pathlib as pl

import pandas as pd
import tushare as ts

from common.helper import ndays_later_from, ndays_ago_from
from common.scipy_helper import pdDF
from common_stock import stock_trade_over_cache
from common_stock.stock_helper import stock_start_day
from common_stock.trade_day import gtrade_day
from stock_data_updater import day_data_path
from stock_data_updater.classify import sz50_to_name, hs300_to_name, zz500_to_name, index2name, \
    etf_stdcode2name
from stock_data_updater.data_updater_logger import updatelog


class SingleStockUpdater:
    @staticmethod
    def _etf_code_to_csv_filepath(etf_code):
        etf_code = etf_code.replace('SH.', '')
        etf_code = etf_code.replace('SZ.', '')
        path = day_data_path.etf  # type: pathlib.Path
        filename = pl.Path(path) / (etf_code + '.csv')
        return filename

    @staticmethod
    def _index_code_to_csv_filepath(index):
        index = index.replace('SH.', '')
        index = index.replace('SZ.', '')
        path = day_data_path.index
        filename = pl.Path(path) / (index + '.csv')
        return filename

    @staticmethod
    def _stock_code_to_csv_filepath(stock_code):
        stock_code = stock_code.replace('SH.', '')
        stock_code = stock_code.replace('SZ.', '')
        path = day_data_path.stock
        filename = pl.Path(path) / (stock_code + '.csv')
        return filename

    @staticmethod
    @stock_trade_over_cache
    def _update_k_data(stock_code: str, filename, index=False):
        print(f'Updating for {stock_code}')
        try:
            df_read = pd.read_csv(filename, index_col='date')
            last_date = datetime.datetime.strptime(df_read.index.values[-1:][0],
                                                   '%Y-%m-%d').date()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df_read = pdDF()
            last_date = ndays_ago_from(stock_start_day, 1)

        # Skip the non_trade_day
        query_start_date = ndays_later_from(last_date, 1)
        while not gtrade_day.is_trade_day(query_start_date):
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

    @classmethod
    def read_stock_day_data(cls, etf_code):
        filename = cls._stock_code_to_csv_filepath(etf_code)
        try:
            df_read = pd.read_csv(filename, index_col='date', dtype={'code': str})
        except FileNotFoundError:
            df_read = pdDF()
        return df_read

    @classmethod
    def read_index_day_data(cls, etf_code):
        filename = cls._index_code_to_csv_filepath(etf_code)
        try:
            df_read = pd.read_csv(filename, index_col='date', dtype={'code': str})
        except FileNotFoundError:
            df_read = pdDF()
        return df_read


read_etf_day_data = SingleStockUpdater.read_etf_day_data
read_index_day_data = SingleStockUpdater.read_index_day_data
read_stock_day_data = SingleStockUpdater.read_stock_day_data


class DayBarUpdater:
    @classmethod
    def update_800s(cls):
        d50 = sz50_to_name
        d300 = hs300_to_name
        d500 = zz500_to_name
        d_all = {**d50, **d300, **d500}
        failed_code = {}
        for code in d_all:
            try:
                SingleStockUpdater.update_stock_day_data(code)
            except Exception as e:
                updatelog.warn(f'Update stock failed. {code}:{e}')
                failed_code[code] = e
        return failed_code

    @classmethod
    def update_all_etfs(cls):
        fail_codes = {}
        for code in etf_stdcode2name:
            try:
                SingleStockUpdater.update_etf_day_data(code)
            except Exception as e:
                updatelog.warn(f'Update etfs failed. {code}:{e}')
                fail_codes[code] = e
        return fail_codes

    @classmethod
    def update_stock_index(cls):
        fail_codes = {}
        for index in index2name:
            try:
                SingleStockUpdater.update_index_data(index)
            except Exception as e:
                updatelog.warn(f'Update index failed. {index}:{e}')
                fail_codes[index] = e
        return fail_codes

    @classmethod
    def update_all(cls):
        updatelog.notice('Begin update all data')
        stock_code2except = {}
        etf_code2except = {}
        index_code2except = {}
        for i in range(2):
            stock_code2except = cls.update_800s()
            if not stock_code2except:
                break
        for i in range(2):
            etf_code2except = cls.update_all_etfs()
            if not etf_code2except:
                break
        for i in range(2):
            index_code2except = cls.update_stock_index()
            if not index_code2except:
                break
        updatelog.notice(
            f'Update data result {stock_code2except}, {etf_code2except}, {index_code2except}')
        return stock_code2except, etf_code2except, index_code2except

def main():
    DayBarUpdater.update_all()


if __name__ == '__main__':
    main()
