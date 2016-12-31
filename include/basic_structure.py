import datetime as dt

from utilities.equality_base import EqualityBase


class Account(EqualityBase):
    def __init__(self):
        self.datetime = dt.datetime.fromtimestamp(0)
        self.total = {}
        self.free = 0
        self.frozen = 0
        self.drawable = 0

        self.deposit = 0
        self.withdraw = 0

    def __hash__(self):
        return hash((self.datetime,
                     self.total,
                     self.free,
                     self.frozen,
                     self.drawable,
                     self.deposit,
                     self.withdraw))


class Stock(EqualityBase):
    def __init__(self):
        self.name = None
        self.code = None
        self.amount = 0
        self.datetime = dt.datetime.fromtimestamp(0)

    def __str__(self):
        return 'Name: {}, Code: {}, Amount: {}, T : {}' \
            .format(self.name, self.code, self.amount, self.datetime.date())

    def __hash__(self):
        return hash((self.name, self.code, self.amount, self.datetime))


class Entrustment(EqualityBase):
    def __init__(self):
        self.id = None
        self.datetime = None
        self.code = None
        self.name = None
        self.operation = None
        self.exchange = None
        self.price = None
        self.type = None
        self.withdraw = None


class ExchangeList:
    def __init__(self):
        self.id = None
        self.time = None
        self.code = None
        self.name = None
        self.price = None
        self.tax = None
        self.commission = None
        self.transfer_fee = None
        self.money_changed = None
        self.money_remain = None
        self.stock_remain = None
