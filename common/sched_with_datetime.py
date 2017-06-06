import datetime
import sched
import time


class SchedulerWithDt:
    def __init__(self):
        self.sched = sched.scheduler(time.time, time.sleep)

    def enter(self, td, priority, func, args=(), kwargs=None):
        kwargs = kwargs if kwargs else {}
        self.sched.enter(td, priority, func, args, kwargs)

    # def enter_dt(self, td: datetime.timedelta, priority, func, args=(), kwargs={}):
    #     self.sched.enter(td.total_seconds(), priority, func, args, kwargs)

    def enterabs_dt(self, dt: datetime, priority, func, args=(), kwargs=None):
        kwargs = kwargs if kwargs else {}
        self.sched.enterabs(dt.timestamp(), priority, func, args, kwargs)

    def run(self):
        self.sched.run()
