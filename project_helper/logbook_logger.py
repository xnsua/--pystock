# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import atexit
import datetime
import pathlib
import sys

import logbook
# noinspection PyUnresolvedReferences
from logbook.base import LogRecord
from logbook.handlers import StreamHandler

from project_helper.config_module import myconfig

logbook.set_datetime_format("local")

# noinspection PyProtectedMember
logbook.base._level_names[logbook.base.WARNING] = 'WARN'
# noinspection PyProtectedMember
logbook.base._level_names[logbook.base.CRITICAL] = 'FATAL'


class MyLogger(logbook.Logger):
    def process_record(self, record: LogRecord):
        logbook.Logger.process_record(self, record)


# noinspection PyUnusedLocal
def stdout_formatter(record, handler):
    dt = record.time.strftime('%H:%M:%S.%f')[:-3]
    filename = pathlib.Path(record.filename).stem
    log = "{dt} {level:5.5} {module:12.12}: {msg}".format(
        dt=dt,
        level=record.level_name,
        msg=record.message,
        module=filename
    )
    return log


def file_formatter(record, handler):
    dt = record.time.strftime('%y%m%d %H:%M:%S.%f')
    filename = pathlib.Path(record.filename).stem
    log = "[{threadid:5x}] {dt} {level:5.5} {module:15.15}: {msg}".format(
        dt=dt,
        level=record.level_name,
        msg=record.message,
        module=filename,
        threadid=record.thread
    )
    return log


stdout_handler = StreamHandler(sys.stdout, bubble=True, level=logbook.INFO)
stdout_handler.formatter = stdout_formatter

_file_path = myconfig.project_root / 'log/py_stock.log'
_file_handler = logbook.FileHandler(_file_path, bubble=False, level=logbook.INFO)

_file_path_with_debug = myconfig.project_root / 'log/py_stock_debug.log'
_file_handler_with_debug = logbook.FileHandler(_file_path_with_debug, bubble=False,
                                               level=logbook.DEBUG)
# file_handler = logbook.RotatingFileHandler(_file_path, bubble=True, max_size=5 * 1024 * 1024,
#                                            backup_count=10)
_file_handler.formatter = file_formatter
_file_handler_with_debug.formatter = file_formatter

mylog = logbook.Logger("std_log")
_file_handler_with_debug.push_application()
_file_handler.push_application()
stdout_handler.push_application()


def jqd(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "")

    message = sep.join(map(str, args)) + end

    mylog.info(message)


s_time = datetime.datetime.now()
print(datetime.datetime.now() - s_time)

atexit.register(lambda: _file_handler_with_debug.pop_application())
atexit.register(lambda: _file_handler.pop_application())
atexit.register(lambda: stdout_handler.pop_application())
