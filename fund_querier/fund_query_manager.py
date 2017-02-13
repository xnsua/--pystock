import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas

from common.helper import save_string_to_file, rmdir_ifexist, is_file_outdated
from common.log_helper import logger
from fund_querier.easy_money_querier import easy_money_querier
from fund_querier.hexun_querier import hexun_querier
from utilities.config import config


class FundQuerier:
    @classmethod
    def query_or_update_all(cls):
        is_fund_codes_outdated = is_file_outdated(cls._get_fund_code_list_path(), span=timedelta(days=30))
        if is_fund_codes_outdated:
            fcodes = easy_money_querier.query_all_stockfund_code()
        else:
            df = pandas.read_csv(cls._get_fund_code_list_path(), dtype=str, index_col=0)
            fcodes = df.iloc[:, 0].tolist()
        for fcode in fcodes:
            # call_after_first(lambda: sleep(random.randint(1, 3)))
            logger.info('Query fund code : %s', fcode)
            try:
                if is_file_outdated(cls.get_fund_info_pathname(fcode), timedelta(days=30)):
                    cls.query_and_save_fund_info(fcode)
                else:
                    pass  # logger.info('%s fund info is up to date')
            except Exception as e:
                logger.warn('Query Fund info %s failed, Msg : %s', fcode, str(e))
            try:
                if is_file_outdated(cls.get_fund_value_pathname(fcode), timedelta(days=30)):
                    cls.query_and_save_fund_value(fcode)
                else:
                    # logger.info('%s fund value is up to date')
                    pass
            except Exception as e:
                logger.warn('Query Fund value %s failed, Msg: %s', fcode, str(e))

    @classmethod
    def _save_stockfund_codes(cls, fcodes):
        save_path = cls._get_fund_code_list_path()
        fcodes = easy_money_querier.query_all_stockfund_code()
        df = pandas.DataFrame(fcodes)
        df.to_csv(save_path)

    @classmethod
    def get_fund_info_pathname(cls, fund_code: str):
        path = cls._get_fund_info_save_path(fund_code)
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, fund_code + '.json')
        return filepath

    @classmethod
    def query_and_save_fund_info(cls, fund_code: str):
        filecontent = cls._get_fund_info_json_str(fund_code)
        pathname = cls.get_fund_info_pathname(fund_code)
        rmdir_ifexist(pathname)
        save_string_to_file(filecontent, pathname)

    @classmethod
    def get_fund_value_pathname(cls, fund_code: str):
        path = cls._get_fund_info_save_path(fund_code)
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join(path, fund_code + '.csv')
        return filepath

    @classmethod
    def query_and_save_fund_value(cls, fund_code):
        df = hexun_querier.get_fund_history(fund_code)
        pathname = cls.get_fund_value_pathname(fund_code)
        rmdir_ifexist(pathname)
        df.to_csv(pathname)

    @staticmethod
    def _get_fund_info_save_path(fund_code: str):
        path = Path(config.get_fund_data_path())
        save_path = path / fund_code
        return str(save_path)

    @staticmethod
    def _get_fund_code_list_path():
        return str(Path(config.get_fund_data_path()) / 'fund_codes.csv')

    @staticmethod
    def _get_fund_info_json_str(fund_code):
        fundinfo = easy_money_querier.query_fund_info(fund_code)
        fundinfo.query_date = datetime.now()
        ss = fundinfo.to_json()
        return ss


fund_querier = FundQuerier()
if __name__ == '__main__':
    fund_querier.query_or_update_all()
    # print(os.getcwd())
