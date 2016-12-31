from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table

from database.db_basic import Database
from include.basic_structure import Stock


class StockTable:
    @property
    def stock(self):
        return 'stock'

    @property
    def buy_time(self):
        return 'datetime'

    @property
    def code(self):
        return 'code'

    @property
    def name(self):
        return 'name'

    @property
    def amount(self):
        return 'amount'

    def __init__(self, db: Database):
        self.__db = db
        self.__engine = db.engine
        self.__table = Table(self.stock, db.meta,
                             Column(self.buy_time, DateTime),
                             Column(self.code, String),
                             Column(self.name, String),
                             Column(self.amount, String))

    def read_stocks(self) -> List[Stock]:
        sel = self.__table.select()
        res = self.__engine.execute(sel)
        rows = res.fetchall()
        res = list()
        for row in rows:
            res.append(self.row_to_stock(row))
        return res

    def row_to_stock(self, row) -> Stock:
        stock = Stock()
        stock.datetime = row[self.buy_time]
        stock.name = row[self.name]
        stock.code = row[self.code]
        stock.amount = row[self.amount]
        return stock

    def save_stock(self, stock: Stock):
        ins = self.__table.insert()
        self.__engine.execute(ins, [
            {
                self.buy_time: stock.datetime,
                self.name: stock.name,
                self.code: stock.code,
                self.amount: stock.amount
            }
        ])
