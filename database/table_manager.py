from common import global_variable
from database.account_table import AccountTable
from database.db_basic import Database
from database.stocks_table import StockTable


class TableManager:
    def __init__(self, testPath=''):
        path = testPath if testPath else global_variable.config.database_path
        self.__db = Database(path)
        self.__account_table = AccountTable(self.__db)
        self.__stock_table = StockTable(self.__db)
        self.__db.meta.bind = self.__db.engine
        self.__db.meta.create_all()

    @property
    def account_table(self):
        return self.__account_table

    @property
    def stock_table(self) -> StockTable:
        return self.__stock_table
