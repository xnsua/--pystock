import atexit
import datetime
import os
import pathlib
import time
from unittest.case import TestCase

from common.datetime_manager import DateTimeManager
from common.helper import dt_now, dt_from_time, dt_combine
from common.key_value_db import KeyValueDb


class _PersistentCacheBase:
    _db_path = None
    _db = None

    @classmethod
    def init_db(cls, file_path):
        assert not cls._db, f'Already initiate with {file_path}'
        cls._db_path = file_path
        pathlib.Path(pathlib.Path(file_path).parent).mkdir(parents=True, exist_ok=True)

        # cls._db = shelve.open(file_path)
        cls._db = KeyValueDb(file_path)
        atexit.register(lambda: cls._db.close())

    def __init__(self, cache_timedelta=None, day_boundary: datetime.time = None, cache_days=None):
        assert cache_timedelta is None or (day_boundary is None and cache_days is None)
        self.is_day_boundary_type = day_boundary is not None

        self.cache_timedelta = cache_timedelta

        self.day_boundary = day_boundary
        self.cache_days = cache_days

    @classmethod
    def print_cache_data(cls):
        for k, v in cls._db.items():
            print(k, v)

    @classmethod
    def clear_cache(cls):
        cls._db.clear()

    def _in_cache_time_span(self, cache_dt: datetime.datetime):
        if self.is_day_boundary_type:
            base_time = dt_combine(dt_now().date(), self.day_boundary)
            delta1 = cache_dt - base_time
            delta2 = dt_now() - base_time
            return delta1.days + self.cache_days > delta2.days
        else:
            return dt_now() - cache_dt < self.cache_timedelta

    def __call__(self, func):
        def function_wrapper(*args, **kwargs):
            import ntpath
            filename = ntpath.basename(func.__code__.co_filename)
            key_text = '.'.join(
                map(str, [filename, func.__name__, *args, *kwargs.items()]))
            val = self._db.get(key_text, None)
            if val and self._in_cache_time_span(val[0]):
                return val[1]
            else:
                result = func(*args, **kwargs)
                self._db[key_text] = dt_now(), result
                return result

        return function_wrapper


def create_persistent_cache(file_path):
    class PersistentCache(_PersistentCacheBase):
        pass

    PersistentCache.init_db(file_path)
    return PersistentCache


class TestFileCache(TestCase):
    p_cache = None

    @classmethod
    def setUpClass(cls):
        for path in pathlib.Path().glob('__test_cache__*'):
            os.remove(path)
        TestFileCache.p_cache = create_persistent_cache('__test_cache__')

    @classmethod
    def tearDownClass(cls):
        TestFileCache.p_cache._db.close()
        for path in pathlib.Path().glob('__test_cache__*'):
            os.remove(path)
        pass

    def test_file_cache1(self):
        @TestFileCache.p_cache(cache_timedelta=datetime.timedelta(seconds=1))
        def foo1():
            return dt_now()

        val = foo1()
        time.sleep(0.5)
        assert val == foo1()
        time.sleep(1.5)
        assert val != foo1()

    def test_file_cache2(self):
        @TestFileCache.p_cache(day_boundary=datetime.time(11, 11, 11), cache_days=1)
        def foo2():
            print(dt_now())
            return dt_now()

        with DateTimeManager(dt_from_time(11, 11, 10)):
            val = foo2()
            time.sleep(0.5)
            assert val == foo2()
            time.sleep(1.5)
            assert val != foo2()

    def test_file_cache3(self):
        @TestFileCache.p_cache(day_boundary=datetime.time(11, 11, 11), cache_days=2)
        def foo3():
            print(dt_now())
            return dt_now()

        with DateTimeManager(dt_from_time(11, 11, 10)):
            val = foo3()
            time.sleep(0.5)
            assert val == foo3()
            time.sleep(1.5)
            assert val == foo3()
