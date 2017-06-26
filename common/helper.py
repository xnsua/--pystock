import datetime as datetime
import os


class hfile:
    @staticmethod
    def modify_time(path):
        file_dt = os.path.getmtime(path)
        return datetime.datetime.fromtimestamp(file_dt)

    @staticmethod
    def create_time(path):
        file_dt = os.path.getctime(path)
        return file_dt.datetime.fromtimestamp(file_dt)


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


def dt_from_time(a, b, c):
    return datetime.datetime.combine(dt_today(), datetime.time(a, b, c))


def dt_date_from_str(text):
    return datetime.date(*map(int, text.split('-')))


def dt_date_to_dt(date):
    return datetime.datetime(date.year, date.month, date.day)


def dt_combine(date, time):
    return datetime.datetime.combine(date, time)


def n_days(n):
    return datetime.timedelta(days=n)


def n_seconds(n):
    return datetime.timedelta(seconds=n)

# def to_seconds_str(o) -> str:
#     return o.strftime('%y-%m-%d %H:%M:%S')


# def to_datetime_str(o, second_digits=3) -> str:
#     ss = o.strftime('%Y-%m-%d %H:%M:%S.%f')
#     if second_digits == 0:
#         ss = ss[:-7]
#         return ss
#     if second_digits == 6:
#         return ss
#     ss = ss[:second_digits - 6]
#     return ss


# def find_date_substr(source: str):
#     return re.search(r'\d{4}-\d{1,2}-\d{1,2}', source).group()


# def loop_for_seconds(func, seconds):
#     start_dt = dt_now()
#     while (dt_now() - start_dt).total_seconds() < seconds:
#         func()


# </editor-fold>

# <editor-fold desc="Basic">
# def type_info(val):
#     if type(val) == list:
#         info = 'typeinfo:: list['
#         for i in range(min(len(val), 3)):
#             info += str(type(val[i])) + ','
#         info += ']'
#         return info
#     if type(val) == dict:
#         info = 'typeinfo:: dict{'
#         for i, key in enumerate(val):
#             if i < 3:
#                 info += str(type(key)) + ':' + str(type(val[key])) + ','
#         info += '}'
#         return info
#     if type(val) == set:
#         info = 'typeinfo:: set{'
#         for i, item in enumerate(val):
#             if i < 3:
#                 info += str(type(item)) + ','
#         info += '}'
#         return info

# </editor-fold>
