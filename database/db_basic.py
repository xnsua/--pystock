import os

import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine


class Database:
    def __init__(self, db_path):
        self.__db_path__ = os.path.abspath(db_path)
        sql_path = 'sqlite:///' + self.__db_path__
        self.__engine__ = sqlalchemy.create_engine(sql_path)
        self.__meta__ = MetaData()

    @property
    def meta(self):
        return self.__meta__

    @property
    def db_path(self):
        return self.__db_path__
    
    @property
    def engine(self):
        return self.__engine__

    def create_all_table(self):
        self.meta.create_all()

