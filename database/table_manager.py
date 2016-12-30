import database
from common import global_variable
from database.account_table import AccountTable
from database.db_basic import Database


class TableManager:
    def __init__(self):
        self.__db__ = Database(global_variable.config.database_path)
        self.__account_table__ = AccountTable(self.__db__)
        self.__db__.meta.bind = self.__db__.engine
        self.__db__.meta.create_all()

    @property
    def account_table(self):
        return self.__account_table__


