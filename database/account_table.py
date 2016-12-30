from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Table

from database.db_basic import Database
from include.basic_structure import Account


class AccountTable:
    # region   Readonly property
    @property
    def account(self):
        return 'account'

    @property
    def initiate(self):
        return 'initiate'

    @property
    def free(self):
        return 'free'

    @property
    def frozen(self):
        return 'frozen'

    @property
    def drawable(self):
        return 'drawable'

    @property
    def total(self):
        return 'total'

    @property
    def profit(self):
        return 'profit'

    @property
    def deposit(self):
        return 'deposit'

    @property
    def withdraw(self):
        return 'withdraw'

    @property
    def table(self):
        return self.__table__

    # endregion

    def __init__(self, db: Database):
        self.__db__ = db
        self.__engine__ = db.engine
        self.__table__ = Table(self.account, db.meta,
                               Column(self.account, Float),
                               Column(self.initiate, Float),
                               Column(self.free, Float),
                               Column(self.frozen, Float),
                               Column(self.drawable, Float),
                               Column(self.total, Float),
                               Column(self.profit, Float),
                               Column(self.deposit, Float),
                               Column(self.withdraw, Float))
    def save_account(self, account: Account):
        ins = self.table.insert()
        self.__engine__.execute(ins, [
            {
                self.total: account.total,
                self.free: account.free,
                self.frozen: account.frozen,
                self.drawable: account.drawable,
                self.deposit: account.deposit,
                self.withdraw: account.withdraw,
            }
        ])

    def read_account(self) -> Account:
        sel = self.__table__.select()
        res = self.__engine__.execute(sel)
        row = res.fetchone()
        account = Account()

        account.total = row[self.total]
        account.free = row[self.free]
        account.frozen = row[self.frozen]
        account.drawable = row[self.drawable]
        account.deposit = row[self.deposit]
        account.withdraw = row[self.withdraw]

        return account
