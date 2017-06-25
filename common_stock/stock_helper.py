import datetime
import re

# noinspection PyProtectedMember
from tushare.stock.cons import _code_to_symbol

stock_start_day = datetime.date(1990, 12, 19)
stock_start_datetime = datetime.datetime(1990, 12, 19)

trade_bid_start_time = datetime.time(9, 15, 0)
trade_bid_end_time = datetime.time(9, 25, 0)
trade1_begin_time = datetime.time(9, 30, 0)
trade1_end_time = datetime.time(11, 30, 0)
trade2_begin_time = datetime.time(13, 0, 0)
trade2_end_time = datetime.time(15, 0, 0)


def to_sina_stock_symbol(code):
    code = to_pure_stock_code(code)
    return _code_to_symbol(code)


def to_pure_stock_code(code):
    # noinspection PyUnresolvedReferences
    val = re.search('\d+', code)[0]
    return val


