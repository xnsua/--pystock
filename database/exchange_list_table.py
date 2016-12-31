from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Table

from database.db_basic import Database
from include.basic_structure import ExchangeList


class ExchangeListTable:
    @property
    def id(self):
        return 'id'

    @property
    def time(self):
        return 'time'

    @property
    def code(self):
        return 'code'

    @property
    def name(self):
        return 'name'

    @property
    def price(self):
        return 'price'

    @property
    def tax(self):
        return 'tax'

    @property
    def commission(self):
        return 'commission'

    @property
    def transfer_fee(self):
        return 'transfer_fee'

    @property
    def money_changed(self):
        return 'money_changed'

    @property
    def money_remain(self):
        return 'money_remain'

    @property
    def stock_remain(self):
        return 'stock_remain'

    @property
    def exchange_list(self):
        return 'exchange_list'

    def __init__(self, db: Database):
        self.__db = db
        self.__engine = db.engine
        self.__table = Table(self.exchange_list, db.meta,
                             Column(self.id, String, primary_key=True),
                             Column(self.time, DateTime),
                             Column(self.code, String),
                             Column(self.name, String),
                             Column(self.price, Float),
                             Column(self.tax, Float),
                             Column(self.commission, Float),
                             Column(self.transfer_fee, Float),
                             Column(self.money_changed, Float),
                             Column(self.money_remain, Float),
                             Column(self.stock_remain, Float))

    def read_exchange_list(self) -> List[ExchangeList]:
        sel = self.__table.select()
        res = self.__engine.execute(sel)
        rows = res.fetchall()
        res = list()
        for row in rows:
            res.append(self.row_to_exchange_list(row))
        return res

    def row_to_exchange_list(self, row) -> ExchangeList:
        exchange_list = ExchangeList()
        exchange_list.id = row[self.id]
        exchange_list.time = row[self.time]
        exchange_list.code = row[self.code]
        exchange_list.name = row[self.name]
        exchange_list.price = row[self.price]
        exchange_list.tax = row[self.tax]
        exchange_list.commission = row[self.commission]
        exchange_list.transfer_fee = row[self.transfer_fee]
        exchange_list.money_changed = row[self.money_changed]
        exchange_list.money_remain = row[self.money_remain]
        exchange_list.stock_remain = row[self.stock_remain]
        return exchange_list

    def save_exchange_list(self, exchange_list: ExchangeList):
        ins = self.__table.insert()
        self.__engine.execute(ins, [
            {
                self.id: exchange_list.id,
                self.time: exchange_list.time,
                self.code: exchange_list.code,
                self.name: exchange_list.name,
                self.price: exchange_list.price,
                self.tax: exchange_list.tax,
                self.commission: exchange_list.commission,
                self.transfer_fee: exchange_list.transfer_fee,
                self.money_changed: exchange_list.money_changed,
                self.money_remain: exchange_list.money_remain,
                self.stock_remain: exchange_list.stock_remain,
            }
        ])
