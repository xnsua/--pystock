import os
import time
import json
import sys
import datetime as dt
import pathlib as pl
import requests
from contextlib import suppress

from common.helper import dttoday, dtnow, dttime
from config_module import myconfig
import tushare as ts
from common.log_helper import jqd
import common.helper as hp


# noinspection PyMethodMayBeStatic
class DateTimeManager:
    def __init__(self):
        self.timerstart = None

    def today(self):
        return dttoday()

    def now(self):
        return dtnow()

    def time(self):
        return dttime()

    def sleep_for_seconds(self, sec):
        time.sleep(sec)

    def set_timer(self):
        self.timerstart = self.now()

    def elapse_seconds(self):
        return (self.now() - self.timerstart).total_seconds()


class MockDateTimeManager(DateTimeManager):
    def __init__(self, start_dt, speed):
        self.start_dt = start_dt
        self.speed = speed

    def now(self):
        vnow = dtnow()
        vtimedelta = vnow - self.start_dt
        sec1 = vtimedelta.total_seconds()
        sec2 = sec1 * self.speed
        vtimedelta2 = dt.timedelta(seconds=sec2)
        now = self.start_dt + vtimedelta2
        return now

    def time(self):
        return self.now().time()

    def sleep(self, seconds):
        time.sleep(seconds / self.speed)


v = MockDateTimeManager(hp.to_datetime(dt.time(10, 1, 1)), 50)

while 1:
    print(v.time())
    v.set_timer()
    v.sleep(10)
    print(v.elapse_seconds())
