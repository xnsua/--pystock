import datetime

import numpy

from common.helper import f_repr
from project_config.config_module import STOCK_ANALYSE_RESULT

stock_start_day = datetime.date(1990, 12, 19)
stock_start_datetime = datetime.datetime(1990, 12, 19)

trade_bid_start_time = datetime.time(9, 15, 0)
trade_bid_end_time = datetime.time(9, 25, 0)
trade1_begin_time = datetime.time(9, 30, 0)
trade1_end_time = datetime.time(11, 30, 0)
trade2_begin_time = datetime.time(13, 0, 0)
trade2_end_time = datetime.time(15, 0, 0)


class CodeTools:
    sh_stock = '6'
    sh_fund = '5'
    sz_stock = '0'
    sz_fund = '1'
    sz_gem = '3'
    sh_all = ['6', '5']
    sz_all = ['0', '1', '3']

    @staticmethod
    def to_pcode(code):
        import re
        val = re.search('\d+', code)[0]
        return val

    @staticmethod
    def is_sh_code(code):
        pcode = CodeTools.to_pcode(code)
        if pcode.startswith('6') or pcode.startswith('5'):
            return True
        elif pcode.startswith('0') or pcode.startswith('1') or pcode.startswith('3'):
            return False
        else:
            assert False, f'Not supported code {pcode}'

    @staticmethod
    def to_rqcode(code):
        pcode = CodeTools.to_pcode(code)
        if CodeTools.is_sh_code(pcode):
            return pcode + '.SHG'
        else:
            return pcode + '.SHE'

    @staticmethod
    def to_sina_code(code):
        pcode = CodeTools.to_pcode(code)
        if CodeTools.is_sh_code(pcode):
            return 'sh' + pcode
        else:
            return 'sz' + pcode


def dict_with_float_repr(dict_):
    items = ['{']
    for key, val in dict_.items():
        items.append(key)
        items.append(':')
        if isinstance(val, float):
            # noinspection PyTypeChecker
            items.append(f_repr(val))
        else:
            items.append(str(val))
        items.append(', ')
    items.append('}')
    result = ''.join(items)
    return result


def calc_year_yield_arr(yields):
    yields = numpy.asarray(yields)
    val2 = yields / yields[0]
    val3 = numpy.arange(1, len(yields))
    val3 = 245 / val3
    val2[1:] = val2[1:] ** val3
    return val2


def date_to_intday(date_):
    return (date_.year * 10000 + date_.month * 100) + date_.day


def date_str_to_intday(date_str):
    y, m, d = map(int, date_str.split('-'))
    return y * 10000 + m * 100 + d


def plot_values(values):
    from matplotlib import pyplot
    pyplot.plot(values)
    pyplot.show()


def plot_histogram(values):
    from matplotlib import pyplot
    import numpy as np
    x = values
    hist, bins = np.histogram(x, bins=50)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    pyplot.bar(center, hist, align='center', width=width)
    pyplot.show()


def stock_result_saver(fpath):
    import pickle
    fpath = STOCK_ANALYSE_RESULT / fpath
    fpath.parent.mkdir(exist_ok=True, parents=True)

    def wrapper(func):

        def worker(*args, **kwargs):
            import ntpath
            import inspect
            import hashlib
            filename = ntpath.basename(func.__code__.co_filename)
            md5id = inspect.getsource(func)
            md5id = hashlib.md5(md5id.encode('utf-8')).hexdigest()
            key_text = '.'.join(
                map(str, [filename, func.__name__, *args, *kwargs.items(), md5id]))
            if fpath.exists():
                with open(fpath, 'rb') as file:
                    val = pickle.load(file)
                    if val[0] == key_text:
                        return val[1]
            val = func(*args)
            with open(fpath, 'wb') as file:
                pickle.dump((key_text, val), file)
            return val

        return worker

    return wrapper


def main():
    pass


if __name__ == '__main__':
    main()
