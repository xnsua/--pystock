from datetime import datetime

import dateutil.parser


# Time helper

def to_seconds_str(o) -> str:
    return o.strftime('%y-%m-%d %H:%M:%S')


def to_min_str(o) -> str:
    return o.strftime('%y-%m-%d %H:%M')


def to_day_str(o) -> str:
    return o.strftime('%y-%m-%d')


def to_microseconds_str(o, seconds_dight=3) -> str:
    ss = o.strftime('%y-%m-%d %H:%M:%S.%f')
    if seconds_dight == 0:
        ss = ss[:-7]
        return ss
    if seconds_dight == 6:
        return ss
    ss = ss[:seconds_dight - 6]
    return ss


def parse_time(time_string):
    return dateutil.parser.parse(time_string)


# Date helper

def is_today(value):
    if type(value) == datetime:
        return value.date() == datetime.today().date()
    elif type(value) == datetime.date:
        return value == datetime.today().date()
    return False


if __name__ == '__main__':
    a = datetime.now()
    a = a.replace(microsecond=0)
    print(to_seconds_str(a))
