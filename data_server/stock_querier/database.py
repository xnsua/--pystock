import datetime as dt
import sqlite3

from config_module import myconfig


class CacheDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_conn = sqlite3.connect(str(db_path))
        self.db_conn.execute('''
            CREATE TABLE cache_table (
                cache_key      TEXT     PRIMARY KEY,
                value          TEXT,
                store_datetime DATETIME
            );
        ''')

    def query(self, key, start_date_time=None):
        if start_date_time is None:
            exec_str = "select * from cache_table where cache_key == 'testkey'"
        if type(start_date_time) == dt.date:
            pass


cache_db = CacheDatabase(myconfig.project_root / 'cache.db')
