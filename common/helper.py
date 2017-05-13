import datetime as dt
import os
import queue
import re
import traceback
from pathlib import Path


# <editor-fold desc="FileAndDir">


def rmdir_ifexist(path):
    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass


def remove_ifexist(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def mkdir_ifnotexist(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def save_bin_to_file(filename: str, b: bytes):
    with open(filename, 'wb') as file:
        file.write(b)
    return


def save_string_to_file(filecontent, filename):
    Path(filename).write_text(filecontent, 'utf-8')


def read_string_from_file(filename):
    return Path(filename).read_text(encoding='utf-8')


def call_after_first(func):
    if call_after_first.first_time:
        call_after_first.first_time = False
        return
    func()


call_after_first.first_time = True


def get_list_from_file(filename):
    fcontent = (Path(filename)).read_text()
    listcontent = fcontent.split('\n')
    listcontent = filter(bool, listcontent)
    return listcontent


def is_file_outdated(path, span):
    if not os.path.exists(path):
        return True
    file_dt = os.path.getmtime(path)
    file_dt = dt.datetime.fromtimestamp(file_dt)
    now = dt.datetime.now()
    curspan = now - file_dt
    if curspan > span:
        return True
    return False


def get_file_modify_time(path):
    file_dt = os.path.getmtime(path)
    return dt.datetime.fromtimestamp(file_dt)


def get_file_create_time(path):
    filedt = os.path.getctime(path)
    return dt.datetime.fromtimestamp(filedt)


# </editor-fold>


# <editor-fold desc="Time">
def time_exec(func):
    start = dt.datetime.now()
    func()
    print(dt.datetime.now() - start)


def ndays_later(n, olddate=None):
    if not olddate:
        olddate = dt.date.today()
    return olddate + dt.timedelta(days=n)


def ndays_ago(n, olddate=None):
    if not olddate:
        olddate = dt.date.today()
    return olddate - dt.timedelta(days=n)


dtdate = dt.date
dtdatetime = dt.datetime
dttimedelta = dt.timedelta


def dttoday():
    return dt.date.today()


def dtnow():
    return dt.datetime.now()


def dtnowtime():
    return dt.datetime.now().time()


def seconds_of(val):
    if type(val) == dt.time:
        return val.hour * 3600 + val.minute * 60 + val.second + val.microsecond / 1000_000
    raise Exception(f'Unsupported type {type(val)}')


def to_datetime(dateortime):
    if type(dateortime) == dt.date:
        return dt.datetime(dateortime.year, dateortime.month, dateortime.day)
    elif type(dateortime) == dt.time:
        return dt.datetime.combine(dttoday(), dateortime)
    raise LogicException(f'{dateortime} has wrong type')


def dt_from_time(a, b, c):
    return dt.datetime.combine(dttoday(), dt.time(a, b, c))


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


def is_today(value):
    if type(value) == dt.datetime:
        return value.date() == dt.date.today()
    elif type(value) == dt.date:
        return value == dt.date.today()
    return False


def find_date_substr(source: str):
    return re.search(r'\d{4}-\d{1,2}-\d{1,2}', source).group()


def sleep_for_milliseconds(millisecond):
    import time
    time.sleep(millisecond / 1000)


def sleep_for_seconds(seconds):
    import time
    time.sleep(seconds)


def seconds_from_epoch():
    import time
    return time.time()


def milliseconds_from_epoch():
    import time
    return time.time() * 1000


def loop_for_seconds(func, seconds):
    start_dt = dtnow()
    while (dtnow() - start_dt).total_seconds() < seconds:
        func()


# </editor-fold>

# noinspection PyUnusedLocal
# Used in lambda
def assign(dest, src):
    dest = src
    return dest


# <editor-fold desc="Exception">
class LogicException(Exception):
    pass


def retry_on_claim_exception(exception):
    return isinstance(exception, ClaimException)


# <editor-fold desc="ClaimException">
class ClaimException(Exception):
    pass


def claim_msg(msg=''):
    raise ClaimException(f'Failed :: {msg}')


def claim_true(val, msg=''):
    if not val:
        raise ClaimException(f'Failed:: {val} :: {msg}')


def claim_false(val, msg=''):
    if val:
        raise ClaimException(f'Failed:: Not {val} :: {msg}')


def claim_len(val1, val2, msg=''):
    if not len(val1) == val2:
        raise ClaimException(f'Failed:: Length of {val1} == {val2} :: {msg}')


def claim_eq(val1, val2, msg=''):
    if not val1 == val2:
        raise ClaimException(f'Failed:: {val1} == {val2} :: {msg}')


def claim_noteq(val1, val2, msg=''):
    if val1 == val2:
        raise ClaimException(f'Failed:: {val1} != {val2} :: {msg}')


def claim_gt(val1, val2, msg=''):
    if not val1 > val2:
        raise ClaimException(f'Failed:: {val1} > {val2} :: {msg}')


def claim_lt(val1, val2, msg=''):
    if not val1 < val2:
        raise ClaimException(f'Failed:: {val1} < {val2} :: {msg}')


def claim_ge(val1, val2, msg=''):
    if not val1 >= val2:
        raise ClaimException(f'Failed:: {val1} >= {val2} :: {msg}')


def claim_le(val1, val2, msg=''):
    if not val1 <= val2:
        raise ClaimException(f'Failed:: {val1} <= {val2} :: {msg}')


def claim_contain(collection, val, msg=''):
    if val not in collection:
        raise ClaimException(
            f'Failed:: {collection} contains {val} :: {msg}')


# </editor-fold>

def to_logstr(e):
    if isinstance(e, Exception):
        tbstr = ''.join(traceback.format_tb(e.__traceback__))
        tbstr = tbstr + str(e)
        return f'Exception encountered: \n{tbstr}'
    raise Exception(f'Unsupport type {type(e)} value:{e}')


# </editor-fold>

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
