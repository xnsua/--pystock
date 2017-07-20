import abc
from abc import abstractmethod

from ip.st import EntrustType, EntrustWay


class AbstractAccount(metaclass=abc.ABCMeta):
    @abstractmethod
    def buy_stock(self, code, price, amount, entrust_type: EntrustType):
        pass

    @abstractmethod
    def sell_stock(self, code, price, amount, entrust_type: EntrustType):
        pass

    @abstractmethod
    def buy_at_most(self, code, price, entrust_type: EntrustType):
        pass

    @abstractmethod
    def sell_at_most(self, code, price, entrust_type: EntrustType):
        pass

    @abstractmethod
    def cancel_order(self, enetrust_id, code, way: EntrustWay):
        pass

    @property
    @abstractmethod
    def available(self):
        pass

    @property
    @abstractmethod
    def entrust_items(self):
        pass


    @property
    @abstractmethod
    def share_items(self):
        pass

    def try_buy_all(self, code, param):
        pass

    def try_sell_all(self, code, param):
        pass

