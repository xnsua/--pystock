import datetime as dt
import logging
import os
import pathlib as pl

logger = logging.getLogger('py_stock.log')
logger.setLevel(logging.DEBUG)
__ch = logging.StreamHandler()
__log_path = pl.Path(__file__).parent / 'py_stock.log'
__fh = logging.FileHandler(__log_path, 'w', 'utf-8')
__formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s.',
    # '[%(thread)d]%(asctime)s %(levelname)s:%(message)s.',
    "%m-%d %H:%M:%S")
# "%y-%m-%d %H:%M:%S")
__ch.setFormatter(__formatter)
__fh.setFormatter(__formatter)
logger.addHandler(__ch)
logger.addHandler(__fh)
logger.info('-------------------- LOGGING START -----------------------------')


class FatalException(Exception):
    pass


class MyLog:
    def __init__(self):
        self.last_error_str = ''

        self.same_error_time = []
        self.last_log_level = None

    def log_with_level(self, log_level, errstr, outputfilepos=True):
        def find_caller():
            """
            Find the stack frame of the caller so that we can note the source
            file name, line number and function name.
            """
            f = logging.currentframe()
            # On some versions of IronPython, currentframe() returns None if
            # IronPython isn't run with -X:Frames.
            if f is not None:
                f = f.f_back
            rv = "(unknown file)", 0, "(unknown function)"
            while hasattr(f, "f_code"):
                co = f.f_code
                filename = os.path.normcase(co.co_filename)
                # noinspection PyProtectedMember
                if filename == logging._srcfile:
                    f = f.f_back
                    continue
                rv = (co.co_filename, f.f_lineno, co.co_name)
                break
            return rv

        caller = find_caller()
        purefilename = pl.Path(caller[0]).name
        callerstr = str((purefilename, caller[1], caller[2]))
        if outputfilepos:
            errstr = errstr + '.  ' + callerstr

        if self.last_error_str == errstr and self.last_log_level == log_level:
            timestr = dt.datetime.now().strftime('%d %H:%M:%S.%f')[:-4]
            self.same_error_time.append(timestr)
            if len(self.same_error_time) == 1:
                log_level(f'---------- REPEAT BEGIN: {timestr}')
        else:
            if self.same_error_time:
                self.last_log_level(f'---------- REPEAT END. LOG TIME::'
                                    f'{self.same_error_time}')
            self.last_error_str = errstr
            self.last_log_level = log_level
            self.same_error_time = []
            log_level(errstr)

    def info(self, errstr):
        self.log_with_level(logger.info, errstr, outputfilepos=False)

    def debug(self, errstr):
        self.log_with_level(logger.debug, errstr, outputfilepos=True)

    def warn(self, errstr):
        self.log_with_level(logger.warning, errstr, outputfilepos=True)

    def error(self, errstr):
        self.log_with_level(logger.error, errstr, outputfilepos=True)

    def fatal(self, errstr):
        self.log_with_level(logger.fatal, errstr, outputfilepos=True)
        raise FatalException(errstr)


mylog = MyLog()


def jqd(*args):
    errstr = ' '.join(str(v) for v in args)
    mylog.log_with_level(logger.debug, errstr, outputfilepos=True)


import atexit
atexit.register(
    lambda: mylog.info(
        '-------------------- PROGRAM EXIT ------------------------------'))


def main():
    logger.setLevel(logging.INFO)


if __name__ == '__main__':
    main()
