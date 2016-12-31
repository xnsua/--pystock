from typing import List

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table

from database.db_basic import Database
from include.basic_structure import Entrustment


class EntrustmentTable:
    @property
    def datetime(self):
        return 'datetime'

    @property
    def id(self):
        return 'id'

    @property
    def code(self):
        return 'code'

    @property
    def name(self):
        return 'name'

    @property
    def operation(self):
        return 'operation'

    @property
    def exchange(self):
        return 'exchange'

    @property
    def price(self):
        return 'price'

    @property
    def type(self):
        return 'type'

    @property
    def withdraw(self):
        return 'withdraw'

    @property
    def entrustment(self):
        return 'entrustment'

    def __init__(self, db: Database):
        self.__db = db
        self.__engine = db.engine
        self.__table = Table(self.entrustment, db.meta,
                             Column(self.datetime, DateTime),
                             Column(self.id, String),
                             Column(self.code, String),
                             Column(self.name, String),
                             Column(self.operation, String),
                             Column(self.exchange, float),
                             Column(self.type, String),
                             Column(self.withdraw, float))

    def read_entrustment(self) -> List[Entrustment]:
        sel = self.__table.select()
        res = self.__engine.execute(sel)
        rows = res.fetchall()
        res = list()
        for row in rows:
            res.append(self.row_to_entrustment(row))
        return res

    def row_to_entrustment(self, row) -> Entrustment:
        entrustment = Entrustment()
        entrustment.datetime = row[self.datetime]
        entrustment.id = row[self.id]
        entrustment.code = row[self.code]
        entrustment.name = row[self.name]
        entrustment.operation = row[self.operation]
        entrustment.exchange = row[self.exchange]
        entrustment.type = row[self.type]
        entrustment.withdraw = row[self.withdraw]
        return entrustment

    def save_entrustment(self, entrustment: Entrustment):
        ins = self.__table.insert()
        self.__engine.execute(ins, [
            {
                self.datetime: entrustment.datetime,
                self.id: entrustment.id,
                self.code: entrustment.code,
                self.name: entrustment.name,
                self.operation: entrustment.operation,
                self.exchange: entrustment.exchange,
                self.type: entrustment.type,
                self.withdraw: entrustment.withdraw
            }
        ])
