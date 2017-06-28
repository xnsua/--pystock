from abc import ABCMeta
import abc

from common.scipy_helper import pdDF
from trading_emulation.account import Account
from trading_emulation.data_providor import DataProvider


class ModelBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def init(self, dp: DataProvider):
        self.dp = dp

    @abc.abstractmethod
    def on_bid_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    @abc.abstractmethod
    def on_trading(self, day: str, acc: Account, rtdata: pdDF):
        pass

    @abc.abstractmethod
    def on_trade_over(self, day: str, acc: Account, rtdata: pdDF):
        pass
