import datetime as dt
import sys
import time

from common.helper import dt_now


class DateTimeManager:
    def __init__(self, start_dt=None, speed=1):
        assert not (start_dt is None and speed != 1)
        self.start_dt = start_dt
        self.real_start_time = dt_now()

        self.speed = speed
        self.timer_start = self.now()

    def now(self):
        if not self.start_dt:
            return dt_now()
        timedelta1 = dt_now() - self.real_start_time
        sec1 = timedelta1.total_seconds()
        sec2 = sec1 * self.speed
        timedelta2 = dt.timedelta(seconds=sec2)
        now = self.start_dt + timedelta2
        return now

    def today(self):
        # noinspection PyUnresolvedReferences
        return self.now().date()

    def time(self):
        # noinspection PyUnresolvedReferences
        return self.now().time()

    def sleep(self, sec):
        time.sleep(sec / self.speed)

    def set_timer(self):
        self.timer_start = self.now()

    def elapse_seconds(self):
        return (self.now() - self.timer_start).total_seconds()

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def do_it_every(self, func, timedelta_):
        start = self.now()
        for i in range(1, sys.maxsize):
            if not func():
                break
            sleep_time = timedelta_ * i - (self.now() - start)
            if sleep_time.total_seconds() > 0:
                self.sleep(sleep_time.total_seconds())
