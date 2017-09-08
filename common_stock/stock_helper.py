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


def to_stdcode(code):
    if code.endswith('.XSHE'):
        code = 'sz' + code[0:6]
    elif code.endswith('.XSHG'):
        code = 'sh' + code[0:6]
    elif code.startswith('sh') or code.startswith('sz'):
        pass
    else:
        raise Exception(f'Not valid code, {code}')
    return code


def to_stdcodes(codes):
    ncodes = [to_stdcode(code) for code in codes]
    return ncodes


def to_num_code(code):
    import re
    val = re.search('\d+', code)[0]
    return val


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
    text = str(val)[0:5]
    return text


def calc_year_yield_arr(yields):
    yields = numpy.asarray(yields)
    val2 = yields / yields[0]
    val3 = numpy.arange(1, len(yields))
    val3 = 245 / val3
    val2[1:] = val2[1:] ** val3
    return val2

def int_to_date(val):
    a,b = divmod(val, 10000)
    b,c = divmod(b, 100)
    return datetime.date(a,b,c)

