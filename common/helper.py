import datetime as dt
import os
from datetime import datetime
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


def save_string_to_file(filecontent: str, filename: str):
    Path(filename).write_text(filecontent, 'utf-8')


def read_string_from_file(filename):
    return Path(filename).read_text(encoding='utf-8')


def call_after_first(func):
    if call_after_first.first_time:
        call_after_first.first_time = False
        return
    func()


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


def ndays_ago(n):
    today = dt.date.today()
    return today - dt.timedelta(days=n)
