import datetime

import numpy

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
    sh_func = '5'
    sz_stock = '0'
    sz_func = '1'
    sz_gem = '3'
    sh_all = ['6', '5']
    sz_all = ['0', '1', '3']

    @staticmethod
    def to_pcode(code):
        import re
        val = re.search('\d+', code)[0]
        return val

    @staticmethod
    def to_rqcode(pcode):
        if pcode.startswith('6') or pcode.startswith('5'):
            return pcode + '.SHG'
        elif pcode.startswith('0') or pcode.startswith('1') or pcode.startswith('3'):
            return pcode + '.SHE'
        else:
            assert False, f'Not supported code {pcode}'


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


def p_repr(val):
    # Percentage represenstation of value
    assert isinstance(val, float), f'{type(val)}'
    text = str(val * 100)[0:4]
    return text + '%'


def f_repr(val):
    # Float representation of value
    text = str(val)[0:6]
    return text


def calc_year_yield_arr(yields):
    yields = numpy.asarray(yields)
    val2 = yields / yields[0]
    val3 = numpy.arange(1, len(yields))
    val3 = 245 / val3
    val2[1:] = val2[1:] ** val3
    return val2


def intday_to_date(val):
    a, b = divmod(val, 10000)
    b, c = divmod(b, 100)
    return datetime.date(a, b, c)


def dtdate_to_intday(date_):
    return (date_.year * 10000 + date_.month * 100) + date_.day


def date_str_to_intday(date_str):
    y, m, d = map(int, date_str.split('-'))
    return y * 10000 + m * 100 + d
