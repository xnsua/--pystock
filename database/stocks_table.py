from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table

import database as db


class StocksTable:
    @property
    def stocks(self):
        return 'stocks'

    @property
    def code(self):
        return 'code'

    @property
    def name(self):
        return 'name'

    @property
    def amount(self):
        return 'amount'

    def __init__(self, db: db.Database):
        self.__db__ = db
        self.__table__ = Table(self.stocks, db.meta,
                               Column(self.code, String),
                               Column(self.name, String),
                               Column(self.amount, String));

    def read_stocks(self):
        #sel = self.__table__.select([sel.])
        pass
