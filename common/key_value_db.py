import os
import pathlib
import pickle
import sqlite3
from contextlib import suppress


class KeyValueDb:
    def __init__(self, db_path):
        pathlib.Path(pathlib.Path(db_path).parent).mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.db_conn = sqlite3.connect(str(db_path))
        self.db_conn.execute('''
              CREATE TABLE IF NOT EXISTS key_value(
                  key      TEXT     PRIMARY KEY,
                  value          BLOB
              );
          ''')

    def __getitem__(self, item):
        assert item, f'key "{item}" is not string'
        text = self.query(item)
        return pickle.loads(text)

    def __setitem__(self, key, value):
        assert isinstance(key, str), f'key "{key}" is not string'
        b_value = pickle.dumps(value)
        return self.update(key, b_value)

    def get(self, key, value):
        try:
            return self[key]
        except:
            return value

    def clear(self):
        self.db_conn.execute('delete from key_value')
        self.db_conn.commit()

    def items(self):
        exec_str = f"select * from key_value"
        cursor = self.db_conn.execute(exec_str)

        class key_value_iter:
            def __init__(self):
                self.cursor = cursor

            def __iter__(self):
                return self

            def __next__(self):
                row = self.cursor.fetchone()
                if not row:
                    raise StopIteration
                return row[0], pickle.loads(row[1])

        return key_value_iter()

    def query(self, key):
        # key = key.replace("'","''")
        exec_str = f"select * from key_value where key == (?)"
        row = self.db_conn.execute(exec_str, (key,)).fetchone()
        # exec_str = f"select * from key_value where key == '{key}'"
        # row = self.db_conn.execute(exec_str).fetchone()
        return row[1]

    def update(self, key, b_value):
        execute_str = f"INSERT OR REPLACE into key_value values (?,?)"

        self.db_conn.execute(execute_str, (key, memoryview(b_value)))
        self.db_conn.commit()

    def close(self):
        self.db_conn.close()


def test():
    path = 'test_cache_db.db'
    with suppress(FileNotFoundError):
        os.remove(path)
    db = KeyValueDb(path)
    value1 = [1, '2"', (3,), {4: '5\''}]

    db['val\'ue'] = value1
    assert db['val\'ue'] == value1

    for k, v in db.items():
        assert v == value1

    db.clear()
    assert db.get('val\'ue', None) is None

    db.close()
    with suppress(FileNotFoundError):
        os.remove(path)
