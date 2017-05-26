import datetime as dt
import logging
import os
import pathlib as pl
import threading

_formatter_without_thread_id = logging.Formatter(
    '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s.',
    "%m-%d %H:%M:%S")
_formatter_with_threadid = logging.Formatter(
    '[%(thread)05x]%(asctime)s.%(msecs)03d %(levelname)s:  %(message)s.',
    "%m-%d %H:%M:%S")


class LogFatalException(Exception):
    pass


class MyLog:
    def __init__(self, filename=None, log_to_stdout=True, level=logging.DEBUG,
                 formatter=_formatter_with_threadid, log_begin_end=False):
        self.tls = threading.local()
        self.tls.last_error_str = ''
        self.tls.same_error_time = []
        self.tls.last_log_level = None

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
            atexit.register(lambda: self.info(
                '-------------------- PROGRAM EXIT ------------------------------'))

    def init_thread_local_variable(self):
        if not hasattr(self.tls, 'last_error_str'):
            self.tls.last_error_str = ''
            self.tls.same_error_time = []
            self.tls.last_log_level = None

    def log_with_level(self, level_log, err_str, outputfilepos=True):
        self.init_thread_local_variable()
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
        pure_file_name = pl.Path(caller[0]).name
        call_str = str((pure_file_name, caller[1], caller[2]))
        if outputfilepos:
            err_str = err_str + '.    ' + call_str
        if self.tls.last_error_str == err_str and self.tls.last_log_level == level_log:
            time_str = dt.datetime.now().strftime('%d %H:%M:%S.%f')[:-4]
            self.tls.same_error_time.append(time_str)
            if len(self.tls.same_error_time) == 1:
                level_log(f'------------- REPEAT BEGIN: {time_str}')
        else:
            if self.tls.same_error_time:
                self.tls.last_log_level(f'------------- REPEAT END. LOG TIME::'
                                        f'{self.tls.same_error_time}')
            self.tls.last_error_str = err_str
            self.tls.last_log_level = level_log
            self.tls.same_error_time = []
            level_log(err_str)

    def info(self, err_str):
        self.log_with_level(self.logger.info, err_str, outputfilepos=False)

    def debug(self, err_str):
        self.log_with_level(self.logger.debug, err_str, outputfilepos=True)

    def warn(self, err_str):
        self.log_with_level(self.logger.warning, err_str, outputfilepos=True)

    def error(self, err_str):
        self.log_with_level(self.logger.error, err_str, outputfilepos=True)

    def fatal(self, err_str):
        self.log_with_level(self.logger.fatal, err_str, outputfilepos=True)
        raise LogFatalException(err_str)

    def exception(self, err_str):
        self.log_with_level(self.logger.exception, err_str, outputfilepos=True)

    def info_if(self, condition, err_str):
        if condition:
            self.log_with_level(self.logger.info, err_str, outputfilepos=False)

    def debug_if(self, condition, err_str):
        if condition:
            self.log_with_level(self.logger.debug, err_str, outputfilepos=True)

    def warn_if(self, condition, err_str):
        if condition:
            self.log_with_level(self.logger.warning, err_str, outputfilepos=True)

    def error_if(self, condition, err_str):
        if condition:
            self.log_with_level(self.logger.error, err_str, outputfilepos=True)

    def fatal_if(self, condition, err_str):
        if condition:
            self.log_with_level(self.logger.fatal, err_str, outputfilepos=True)
            raise LogFatalException(err_str)


