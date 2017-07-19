import abc

from common_stock.py_dataframe import RealtimeDataRepr
from trading.abstract_context import AbstractContext


class AbstractModel(metaclass=abc.ABCMeta):
    def __init__(self):
        self.codes = None

    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def init_model(self, ctx: AbstractContext):
        pass

    @abc.abstractmethod
    def on_bid_over(self, context: AbstractContext, rdr: RealtimeDataRepr):
        pass

    @abc.abstractmethod
    def handle_bar(self, context: AbstractContext, rdr: RealtimeDataRepr):
        pass

    @abc.abstractmethod
    def on_trade_over(self, context: AbstractContext, rdr: RealtimeDataRepr):
        pass


