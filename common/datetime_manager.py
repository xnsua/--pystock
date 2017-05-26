import datetime
import datetime as dt
import sys
import time

_std_datetime = datetime.datetime
_std_date = datetime.date


class MockDateTime(_std_datetime):
    datetime_manager = None  # type: DateTimeManager

    @classmethod
    def now(cls):
        return cls.datetime_manager.now()


class MockDate(_std_date):
    datetime_manager = None  # type: DateTimeManager

    @classmethod
    def today(cls):
        return cls.datetime_manager.today()


class DateTimeManager:
    def __init__(self, start_dt, speed=1):
        self.std_date = datetime.date
        self.std_datetime = datetime.datetime

        assert not (start_dt is None and speed != 1)
        self.start_dt = start_dt
        self.real_start_time = self.std_datetime.now()

        self.speed = speed

    def __enter__(self):
        MockDateTime.datetime_manager = self
        MockDate.datetime_manager = self

        self.std_datetime = datetime.datetime
        datetime.datetime = MockDateTime

        self.std_date = datetime.date
        datetime.date = MockDate
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        datetime.datetime = self.std_datetime
        datetime.date = self.std_date

    def now(self):
        timedelta1 = self.std_datetime.now() - self.real_start_time
        sec1 = timedelta1.total_seconds()
        sec2 = sec1 * self.speed
        timedelta2 = dt.timedelta(seconds=sec2)
        now = self.start_dt + timedelta2
        return datetime_to_mock_datetime(now)

    def today(self):
        # noinspection PyUnresolvedReferences
        return date_to_mock_date(self.now().date())

    def time(self):
        # noinspection PyUnresolvedReferences
        return self.now().time()

    def sleep(self, sec):
        time.sleep(sec / self.speed)

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def do_it_every(self, func, timedelta_):
        start = self.now()
        for i in range(1, sys.maxsize):
            if not func():
                break
            sleep_time = timedelta_ * i - (self.now() - start)
            if sleep_time.total_seconds() > 0:
                self.sleep(sleep_time.total_seconds())


def datetime_to_mock_datetime(dt_):
    return MockDateTime(dt_.year,
                        dt_.month,
                        dt_.day,
                        dt_.hour,
                        dt_.minute,
                        dt_.second,
                        dt_.microsecond)


def date_to_mock_date(date_):
    return MockDate(date_.year,
                    date_.month,
                    date_.day)
