import time
from unittest import TestCase

from common.datetime_manager import DateTimeManager
from common.helper import dt_now, dt_from_time, datetime


class TestDateTimeManager(TestCase):
    def test_now(self):
        dtm = DateTimeManager(datetime.datetime.now())
        assert (dtm.now() - dt_now()).total_seconds() < 0.1
        start_dt = dt_from_time(9, 0, 0)
        dtm = DateTimeManager(start_dt, 2)
        assert (dtm.now() - start_dt).total_seconds() == 0
        time.sleep(1)
        assert 2.1 >= (dtm.now() - start_dt).total_seconds() >= 2

    def test_sleep(self):
        start_dt = dt_now()
        dtm = DateTimeManager(start_dt, 2)
        dtm.sleep(2)
        assert 1.1 >= (dt_now() - start_dt).total_seconds() >= 1

    def test_do_it_every(self):
        dtm = DateTimeManager(datetime.datetime.now())
        result_list = []
        count = 2

        def func():
            nonlocal count
            count = count - 1
            result_list.append(count)
            return count

        dtm.do_it_every(func, datetime.timedelta(seconds=1))
        assert len(result_list) == 2

    def test_context(self):
        with DateTimeManager(datetime.datetime(2000, 1, 1, 1, 1, 1), 2):
            dt1 = datetime.datetime.now()
        dt2 = datetime.datetime.now()
        assert dt2 - dt1 > datetime.timedelta(days=100)
