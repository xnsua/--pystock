import datetime


class MockDateTime(datetime.datetime):
    start_dt = None  # type: datetime.datetime
    speed = None  # type: int

    def


def mock_datetime(start_dt, speed):
    MockDateTime.start_dt = start_dt
    MockDateTime.speed = speed
    datetime.datetime = MockDateTime

class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


datetime.date = NewDate
