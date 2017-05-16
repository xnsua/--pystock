import time
from unittest import TestCase

from common.datetime_manager import DateTimeManager
from common.helper import dt_now, dt_from_time, dt


class TestDateTimeManager(TestCase):
    def test_now(self):
        dtm = DateTimeManager()
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

    def test_elapse_seconds(self):
        start_dt = dt_now()
        dtm = DateTimeManager(start_dt, 2)
        dtm.sleep(2)
        assert 2.1 > dtm.elapse_seconds() > 2

    def test_do_it_every(self):
        dtm = DateTimeManager()
        result_list = []
        count = 2

        def func():
            nonlocal count
            count = count - 1
            result_list.append(count)
            return count

        dtm.do_it_every(func, dt.timedelta(seconds=1))
        assert len(result_list) == 2
