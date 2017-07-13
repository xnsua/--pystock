import abc
import datetime
from trading.abstract_account import AbstractAccount


class AbstractContext(metaclass=abc.ABCMeta):
    def __init__(self, account=None):
        self.account = account  # type: AbstractAccount
        self.datetime = None  # type: datetime.datetime

