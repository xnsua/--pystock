import datetime as dt
import time


class SimpleRetry:
    def __init__(self, wait_max_time=3000, wait_base_time=1,
                 wait_exponential=False,
                 max_retry_times=2 ** 32,
                 retry_exception_types=None):
        self.max_retry_times = max_retry_times
        self.max_wait_time = wait_max_time
        self.wait_base_time = wait_base_time
        self.wait_exponential = wait_exponential
        self.retry_exception_type = retry_exception_types \
            if retry_exception_types else [Exception]

    def __call__(self, func):
        start_time = dt.datetime.now()

        def func_wrapper(*args, **kwargs):
            if self.wait_exponential:
                wait_times = (self.wait_base_time * 2 ** v for v in
                              range(0, 1000))
            else:
                wait_times = (self.wait_base_time,) * 1000

            def get_duration():
                td = (dt.datetime.now() - start_time)
                return td.days * 86400000 + td.seconds * 1000 + td.microseconds / 1000

            retry_count = 0
            for wait_time in wait_times:
                retry_count += 1
                if get_duration() + wait_time < self.max_wait_time \
                        and retry_count < self.max_retry_times:
                    try:
                        result = func(*args, **kwargs)
                    except (*self.retry_exception_type,):
                        if get_duration() + wait_time < self.max_wait_time:
                            time.sleep(wait_time / 1000)
                        else:
                            raise
                    else:
                        return result
                else:
                    return func(*args, **kwargs)

        return func_wrapper


def main():
    # class E2(Exception):
    #     pass
    #
    # class E1(Exception):
    #     pass
    #
    # def foo(*args):
    #     print('in foo')
    #     for v in args:
    #         print(type(v))
    #     raise E1('dd')
    #
    # re = SimpleRetry(wait_base_time=10, wait_max_time=1000,
    #                  retry_exception_type=[E1], wait_exponential=True,
    #                  max_retry_times=2)
    #

    pass


if __name__ == '__main__':
    main()
