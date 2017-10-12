import cmath
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


def float_default_zero(text):
    if text:
        return float(text)
    return 0


def int_default_zero(text):
    if text:
        return int(text)
    return 0


def geo_mean_overflow(iterable):
    for val in iterable:
        assert val > 0
    a = [cmath.log(val) for val in iterable]
    return cmath.exp(sum(a) / len(a)).real


def print_line_item(*args):
    print(*args, sep='\n')


def iterable_extend(func):
    def func_inner(*args):
        try:
            if isinstance(args[0], str):
                return func(*args)
            else:
                iter(args[0])
        except:
            return func(*args)
        else:
            ll = []
            first, remain = args[0], args[1:]
            for i in first:
                ll.append(func(i, *remain))
            return ll

    return func_inner

def is_iterable(val):
    if isinstance(val, str):
        return False
    try:
        iter(val)
    except:
        return False
    return True

def full_file_name_under_folder(path):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return [join(path,item) for item in onlyfiles]

# def reduce_along_column(func, first, *remains):
#     try:
#         ll = []
#         for val in first:
#             ll.append(func(val, *remains))
#         return ll
#     except:
#         return func(first, *remains)
#
#
# def reduce_along_row(func, first, *remains):
#     try:
#         vals = zip(*first)
#         ll = []
#         for val in vals:
#             ll.append(func(val, *remains))
#         return ll
#     except:
#         return func(first, *remains)


def main():
    pass


if __name__ == '__main__':
    main()
