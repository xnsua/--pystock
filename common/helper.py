import datetime as dt


def is_today(value):
    if type(value) == dt.datetime:
        return value.date() == dt.datetime.today().date()
    elif type(value) == dt.date:
        return value == dt.datetime.today().date()
    return False
