import datetime
import re

# noinspection PyProtectedMember

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
    # noinspection PyUnresolvedReferences
    val = re.search('\d+', code)[0]
    return val
