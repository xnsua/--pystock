import os

import sqlalchemy
from sqlalchemy import MetaData


class Database:
    def __init__(self, db_path):
        self.__db_path = os.path.abspath(db_path)
        sql_path = 'sqlite:///' + self.__db_path
        self.__engine = sqlalchemy.create_engine(sql_path)
        self.__meta = MetaData()

    @property
    def meta(self):
        return self.__meta

    @property
    def db_path(self):
        return self.__db_path
    
    @property
    def engine(self):
        return self.__engine

    def create_all_table(self):
        self.meta.create_all()

