import datetime as dt
import time

from common.helper import dtnow


class DateTimeManager:
    def __init__(self, start_dt=dtnow(), speed=1):
        self.start_dt = start_dt
        self.real_start_time = dtnow()

        self.speed = speed
        self.timer_start = self.now()

    def now(self):
        vtimedelta = dtnow() - self.real_start_time
        sec1 = vtimedelta.total_seconds()
        sec2 = sec1 * self.speed
        vtimedelta2 = dt.timedelta(seconds=sec2)
        now = self.start_dt + vtimedelta2
        return now

    def today(self):
        return self.now().date()

    def time(self):
        return self.now().time()

    def sleep(self, sec):
        time.sleep(sec / self.speed)

    def set_timer(self):
        self.timer_start = self.now()

    def elapse_seconds(self):
        return (self.now() - self.timer_start).total_seconds()
