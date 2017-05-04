import datetime as dt
import logging
import os
import pathlib as pl

_formatter_without_threadid = logging.Formatter(
    '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s.',
    "%m-%d %H:%M:%S")
_formatter_with_threadid = logging.Formatter(
    '[%(thread)d]%(asctime)s.%(msecs)03d %(levelname)s:%(message)s.',
    "%m-%d %H:%M:%S")


class FatalException(Exception):
    pass


class MyLog:
    def __init__(self, filename=None, log_to_stdout=True, level=logging.DEBUG,
                 formatter=_formatter_with_threadid, log_begin_end=False):
        self.last_error_str = ''
        self.same_error_time = []
        self.last_log_level = None

        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level)

        self.file_handle = logging.FileHandler(
            pl.Path(__file__).parent.parent / 'log' / filename, 'a', 'utf-8')
        self.file_handle.setFormatter(formatter)
        self.logger.addHandler(self.file_handle)

        if log_to_stdout:
            stdoutstream = logging.StreamHandler()
            stdoutstream.setFormatter(formatter)
            self.logger.addHandler(stdoutstream)
        if log_begin_end:
            self.logger.info(
                '-------------------- LOGGING START -----------------------------')

            import atexit
            atexit.register(lambda: self.logger.info(
                '-------------------- PROGRAM EXIT ------------------------------'))

    def log_with_level(self, log_with_level, errstr, outputfilepos=True):
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

        if self.last_error_str == errstr and self.last_log_level == log_with_level:
            timestr = dt.datetime.now().strftime('%d %H:%M:%S.%f')[:-4]
            self.same_error_time.append(timestr)
            if len(self.same_error_time) == 1:
                log_with_level(f'---------- REPEAT BEGIN: {timestr}')
        else:
            if self.same_error_time:
                self.last_log_level(f'---------- REPEAT END. LOG TIME::'
                                    f'{self.same_error_time}')
            self.last_error_str = errstr
            self.last_log_level = log_with_level
            self.same_error_time = []
            log_with_level(errstr)

    def info(self, errstr):
        self.log_with_level(self.logger.info, errstr, outputfilepos=False)

    def debug(self, errstr):
        self.log_with_level(self.logger.debug, errstr, outputfilepos=True)

    def warn(self, errstr):
        self.log_with_level(self.logger.warning, errstr, outputfilepos=True)

    def error(self, errstr):
        self.log_with_level(self.logger.error, errstr, outputfilepos=True)

    def fatal(self, errstr):
        self.log_with_level(self.logger.fatal, errstr, outputfilepos=True)
        raise FatalException(errstr)

    def info_if(self, condition, errstr):
        if condition:
            self.log_with_level(self.logger.info, errstr, outputfilepos=False)

    def debug_if(self, condition, errstr):
        if condition:
            self.log_with_level(self.logger.debug, errstr, outputfilepos=True)

    def warn_if(self, condition, errstr):
        if condition:
            self.log_with_level(self.logger.warning, errstr, outputfilepos=True)

    def error_if(self, condition, errstr):
        if condition:
            self.log_with_level(self.logger.error, errstr, outputfilepos=True)

    def fatal_if(self, condition, errstr):
        if condition:
            self.log_with_level(self.logger.fatal, errstr, outputfilepos=True)
        raise FatalException(errstr)


mylog = MyLog(filename='py_stock.log')


def jqd(*args):
    errstr = ' '.join(str(v) for v in args)
    mylog.log_with_level(mylog.debug, errstr, outputfilepos=True)


def main():
    # mylog = MyLog(filename='pystock2.log')
    # mylog.debug_if(1<0, 'aaa')
    # sleep_ms(100000)
    pass


if __name__ == '__main__':
    main()
