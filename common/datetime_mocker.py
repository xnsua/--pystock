import datetime


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


datetime.date = NewDate
