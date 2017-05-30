import abc

from common.scipy_helper import pdDF


class AbstractModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def init_model(self):
        pass

    @abc.abstractmethod
    def on_bid_over(self, df: pdDF):
        pass

    @abc.abstractmethod
    def handle_bar(self, df: pdDF):
        pass

