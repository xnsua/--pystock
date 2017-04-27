import datetime as dt
import os
import re
from datetime import datetime, date
from pathlib import Path


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


def get_list_from_file(filename):
    fcontent = (Path(filename)).read_text()
    listcontent = fcontent.split('\n')
    listcontent = filter(bool, listcontent)
    return listcontent

call_after_first.first_time = True


def is_file_outdated(path, span):
    if not os.path.exists(path):
        return True
    file_dt = os.path.getmtime(path)
    file_dt = datetime.fromtimestamp(file_dt)
    now = datetime.now()
    curspan = now - file_dt
    if curspan > span:
        return True
    return False


def get_file_modify_time(path):
    file_dt = os.path.getmtime(path)
    return datetime.fromtimestamp(file_dt)


def get_file_create_time(path):
    filedt = os.path.getctime(path)
    return datetime.fromtimestamp(filedt)


def time_exec(func):
    start = datetime.now()
    func()
    print(datetime.now() - start)


def ndays_later(n, olddate=None):
    if not olddate:
        olddate = dt.date.today()
    return olddate + dt.timedelta(days=n)


def ndays_ago(n, olddate=None):
    if not olddate:
        olddate = dt.date.today()
    return olddate - dt.timedelta(days=n)


def to_datetime(olddate: dt.date):
    return dt.datetime(olddate.year, olddate.month, olddate.day)


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
    if type(value) == datetime:
        return value.date() == datetime.today().date()
    elif type(value) == date:
        return value == datetime.today().date()
    return False


def find_date_substr(source: str):
    return search_substr_by_regex('\d{4}-\d{1,2}-\d{1,2}', source)


def search_substr_by_regex(regex: str, source: str):
    reg = re.compile(regex)
    match = reg.search(source)
    return match.group()
