from abc import ABCMeta
import abc

from common.scipy_helper import pdDF
from common_stock.trade_day import gtrade_day
from trading_emulation.account import Account
from trading_emulation.data_provider import DataProvider, gdata_provider


class ModelBase(metaclass=ABCMeta):
    def __init__(self, code, date_range, params):
        self.codes = code
        self.date_range = date_range if date_range \
            else self._calc_date_range(self.codes, gdata_provider)
        self.params = params

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def init(self, dp: DataProvider):
        pass

    @abc.abstractmethod
    def on_bid_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    @abc.abstractmethod
    def on_trading(self, day: str, acc: Account, rtdata: pdDF):
        pass

    @abc.abstractmethod
    def on_trade_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    @staticmethod
    def _calc_date_range(codes, dp):
        first_day = min(dp.ddr(code).first_day() for code in codes)
        last_day = min(dp.ddr(code).last_day() for code in codes)
        return gtrade_day.close_range(first_day, last_day)
