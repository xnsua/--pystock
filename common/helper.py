import datetime as dt
import os
import queue
import re
import traceback


# <editor-fold desc="FileAndDir">

def is_file_outdated(path, span):
    if not os.path.exists(path):
        return True
    file_dt = os.path.getmtime(path)
    file_dt = dt.datetime.fromtimestamp(file_dt)
    now = dt.datetime.now()
    cur_span = now - file_dt
    if cur_span > span:
        return True
    return False


def get_file_modify_time(path):
    file_dt = os.path.getmtime(path)
    return dt.datetime.fromtimestamp(file_dt)


def get_file_create_time(path):
    file_dt = os.path.getctime(path)
    return file_dt.datetime.fromtimestamp(file_dt)


# </editor-fold>


# <editor-fold desc="Time">
def time_exec(func):
    start = dt.datetime.now()
    func()
    print(dt.datetime.now() - start)


def ndays_later(n, old_date=None):
    if not old_date:
        old_date = dt.date.today()
    return old_date + dt.timedelta(days=n)


def ndays_ago(n, old_date=None):
    if not old_date:
        old_date = dt.date.today()
    return old_date - dt.timedelta(days=n)


def dt_date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


def dt_today():
    return dt.date.today()


def dt_now():
    return dt.datetime.now()


def dt_now_time():
    return dt.datetime.now().time()


def dt_from_time(a, b, c):
    return dt.datetime.combine(dt_today(), dt.time(a, b, c))


def to_seconds_str(o) -> str:
    return o.strftime('%y-%m-%d %H:%M:%S')


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
def to_log_str(e):
    if isinstance(e, Exception):
        log_str = ''.join(traceback.format_tb(e.__traceback__))
        log_str = log_str + str(e)
        return f'Exception encountered: \n{log_str}'
    raise Exception(f'Unsupported type {type(e)} value:{e}')


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

# <editor-fold desc="Data Structure">
class ObjectCabinet:
    def __init__(self, generator, clear_func):
        self.queue = queue.Queue()
        self.generator = generator
        self.clear_func = clear_func

    def fetch_one(self):
        try:
            fetch_result = self.queue.get(block=False)
            return fetch_result
        except queue.Empty:
            return self.generator()

    def put_one(self, obj):
        if self.clear_func:
            self.clear_func(obj)
        self.queue.put(obj)

    def use_one(self):
        class Context:
            def __init__(self, cabinet):
                self.cabinet = cabinet
                self.current_obj = None

            def __enter__(self):
                self.current_obj = self.cabinet.fetch_one()
                return self.current_obj

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.cabinet.put_one(self.current_obj)

        return Context(self)

# </editor-fold>
