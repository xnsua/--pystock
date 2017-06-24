import datetime as datetime
import os
import re


# <editor-fold desc="FileAndDir">


def is_file_outdated(path, span):
    if not os.path.exists(path):
        return True
    file_dt = os.path.getmtime(path)
    file_dt = datetime.datetime.fromtimestamp(file_dt)
    now = datetime.datetime.now()
    cur_span = now - file_dt
    if cur_span > span:
        return True
    return False


def get_file_modify_time(path):
    file_dt = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(file_dt)


def get_file_create_time(path):
    file_dt = os.path.getctime(path)
    return file_dt.datetime.fromtimestamp(file_dt)


# </editor-fold>


# <editor-fold desc="Time">

def ndays_later(n):
    return datetime.date.today() + datetime.timedelta(days=n)


def ndays_ago(n):
    return datetime.date.today() - datetime.timedelta(days=n)


def ndays_later_from(old_date, n):
    if not old_date:
        old_date = datetime.date.today()
    return old_date + datetime.timedelta(days=n)


def ndays_ago_from(old_date, n):
    if not old_date:
        old_date = datetime.date.today()
    return old_date - datetime.timedelta(days=n)


def dt_date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def dt_today():
    return datetime.date.today()


def dt_now():
    return datetime.datetime.now()


def dt_now_time():
    return datetime.datetime.now().time()


def dt_from_time(a, b, c):
    return datetime.datetime.combine(dt_today(), datetime.time(a, b, c))


def dt_combine(date, time):
    return datetime.datetime.combine(date, time)


def dt_day_delta(n):
    return datetime.timedelta(days=n)


def dt_seconds_delta(n):
    return datetime.timedelta(seconds=n)


def to_seconds_str(o) -> str:
    return o.strftime('%y-%m-%d %H:%M:%S')


def dt_from_date_str(text):
    return datetime.date(*map(int, text.split('-')))


def to_datetime_str(o, second_digits=3) -> str:
    ss = o.strftime('%Y-%m-%d %H:%M:%S.%f')
    if second_digits == 0:
        ss = ss[:-7]
        return ss
    if second_digits == 6:
        return ss
    ss = ss[:second_digits - 6]
    return ss


def find_date_substr(source: str):
    return re.search(r'\d{4}-\d{1,2}-\d{1,2}', source).group()


def loop_for_seconds(func, seconds):
    start_dt = dt_now()
    while (dt_now() - start_dt).total_seconds() < seconds:
        func()


# </editor-fold>

# <editor-fold desc="Basic">
def type_info(val):
    if type(val) == list:
        info = 'typeinfo:: list['
        for i in range(min(len(val), 3)):
            info += str(type(val[i])) + ','
        info += ']'
        return info
    if type(val) == dict:
        info = 'typeinfo:: dict{'
        for i, key in enumerate(val):
            if i < 3:
                info += str(type(key)) + ':' + str(type(val[key])) + ','
        info += '}'
        return info
    if type(val) == set:
        info = 'typeinfo:: set{'
        for i, item in enumerate(val):
            if i < 3:
                info += str(type(item)) + ','
        info += '}'
        return info

# </editor-fold>
