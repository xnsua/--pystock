import datetime

from utilities.equality_base import EqualityBase


class Account(EqualityBase):
    def __init__(self):
        self.datetime = datetime.datetime.fromtimestamp(0)
        self.total = {}
        self.free = 0
        self.frozen = 0
        self.drawable = 0

        self.deposit = 0
        self.withdraw = 0

    def __str__(self):
        fm = 'datetime:{} total:{} free:{} frozen:{} drawable:{} deposit:{} withdraw:{}'
        s = fm.format(self.datetime,
                      self.total,
                      self.free,
                      self.frozen,
                      self.drawable,
                      self.deposit,
                      self.withdraw)
        return s

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
        self.datetime = datetime.datetime.fromtimestamp(0)

    def __str__(self):
        return 'Name: {}, Code: {}, Amount: {}, T : {}' \
            .format(self.name, self.code, self.amount, self.datetime.date())

    def __hash__(self):
        return hash((self.name, self.code, self.amount, self.datetime))


class Entrustment(EqualityBase):
    def __init__(self):
        self.id = None
        self.datetime = datetime.datetime.fromtimestamp(0)
        self.code = None
        self.name = None
        self.operation = None
        self.exchange = None
        self.price = None
        self.type = None
        self.withdraw = None

    def __str__(self):
        fm = "id:{} datetime:{} code:{} name:{} operation:{} exchange:{} price:{} type:{} withdraw:{}"
        s = fm.format(self.id, self.datetime, self.code, self.name, self.operation, self.exchange, self.price,
                      self.type, self.withdraw)
        return s

    def __hash__(self):
        return hash((self.id, self.datetime, self.code, self.name, self.operation, self.exchange, self.price,
                     self.type, self.withdraw))


class ExchangeList(EqualityBase):
    def __init__(self):
        self.time = None
        self.id = None
        self.code = None
        self.name = None
        self.price = None
        self.money_changed = None
        self.money_remain = None
        self.stock_remain = None
        self.commission = None
        self.transfer_fee = None
        self.tax = None

    def __str__(self):
        fm = 'time:{} id:{} code:{} name:{} price:{} ' \
             'mchange:{} mremain:{} stockremain:{} ' \
             'commission:{} transferfee:{} tax:{} '
        s = fm.format(self.time, self.id, self.code, self.name, self.price, self.money_changed, self.money_remain,
                      self.stock_remain,
                      self.commission, self.transfer_fee, self.tax)
        return s

    def __hash__(self):
        return hash((self.time, self.id, self.code, self.name, self.price, self.money_changed, self.money_remain,
                     self.stock_remain, self.commission, self.transfer_fee, self.tax))
