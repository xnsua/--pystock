from unittest import TestCase

from common.datetime_manager import DateTimeManager
from common.helper import dtnow, dt_from_time, sleep_for_seconds, dttimedelta


class TestDateTimeManager(TestCase):
    def test_now(self):
        dtm = DateTimeManager()
        assert (dtm.now() - dtnow()).total_seconds() < 0.1
        start_dt = dt_from_time(9, 0, 0)
        dtm = DateTimeManager(start_dt, 2)
        assert (dtm.now() - start_dt).total_seconds() == 0
        sleep_for_seconds(1)
        assert 2.1 >= (dtm.now() - start_dt).total_seconds() >= 2

    def test_sleep(self):
        start_dt = dtnow()
        dtm = DateTimeManager(start_dt, 2)
        dtm.sleep(2)
        assert 1.1 >= (dtnow() - start_dt).total_seconds() >= 1

    def test_elapse_seconds(self):
        start_dt = dtnow()
        dtm = DateTimeManager(start_dt, 2)
        dtm.sleep(2)
        assert 2.1 > dtm.elapse_seconds() > 2

    def test_do_it_every(self):
        dtm = DateTimeManager()
        result_list = []
        quit_variable = []
        count = 2

        def func():
            nonlocal count
            count = count - 1
            if count == 0:
                nonlocal quit_variable
                quit_variable.append(1)
            result_list.append(1)

        dtm.do_it_every(func, dttimedelta(seconds=1), quit_variable)
        assert len(result_list) == 2
