import abc


class AbstractModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def init_model(self):
        pass

    @abc.abstractmethod
    def on_bid_over(self):
        pass

    @abc.abstractmethod
    def handle_bar(self):
        pass


