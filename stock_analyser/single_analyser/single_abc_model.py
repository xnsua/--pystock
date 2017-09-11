import abc


class SingleAbcModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def skip_len(self): pass

    @abc.abstractmethod
    def buy_sell_price(self, index): pass