import datetime
import pathlib
import sys

from project_helper.logbook_logger import mylog

try:
    import logbook
except:
    import log_helper
# noinspection PyUnresolvedReferences
from logbook.base import LogRecord
from logbook.handlers import StreamHandler

logbook.set_datetime_format("local")

# noinspection PyProtectedMember
logbook.base._level_names[logbook.base.WARNING] = 'WARN'
# noinspection PyProtectedMember
logbook.base._level_names[logbook.base.CRITICAL] = 'FATAL'


class MyLogger(logbook.Logger):
    def process_record(self, record: LogRecord):
        logbook.Logger.process_record(self, record)


# noinspection PyUnusedLocal
def stdout_formatter(record: LogRecord, handler):
    dt = record.time.strftime('%H:%M:%S.%f')[:-3]
    filename = pathlib.Path(record.filename).stem
    log = "{dt} {level:5.5} {module:12.12}: {msg}".format(
        dt=dt,
        level=record.level_name,
        msg=record.message,
        module=filename
    )
    except_str = record.formatted_exception
    if except_str:
        return log + '\n' + except_str
    return log


# noinspection PyUnusedLocal
def file_formatter(record, handler):
    dt = record.time.strftime('%y-%m-%d %H:%M:%S.%f')
    filename = pathlib.Path(record.filename).stem
    log = "[{threadid:5x}] {dt} {level:5.5} {module:15.15}: {msg}".format(
        dt=dt,
        level=record.level_name,
        msg=record.message,
        module=filename,
        threadid=record.thread
    )
    except_str = record.formatted_exception
    if except_str:
        return log + '\n' + except_str
    return log


stdout_handler = StreamHandler(sys.stdout, bubble=False, level=logbook.INFO)
stdout_handler.formatter = stdout_formatter

_file_path = pathlib.Path(__file__).parent / 'updater.log'
_file_handler = logbook.FileHandler(_file_path, bubble=True, level=logbook.NOTICE)

# file_handler = logbook.RotatingFileHandler(_file_path, bubble=True, max_size=5 * 1024 * 1024,
#                                            backup_count=10)
_file_handler.formatter = file_formatter

updatelog = logbook.Logger("update_log")
updatelog.handlers.append(_file_handler)
updatelog.handlers.append(stdout_handler)

s_time = datetime.datetime.now()


def main():
    updatelog.info('Hello6')
    mylog.warn('war7')


if __name__ == '__main__':
    main()
