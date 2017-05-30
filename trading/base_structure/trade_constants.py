import datetime
from typing import List

from common.base_functions import ObjectWithIndentRepr, ObjectWithRepr
from common.scipy_helper import pdDF
from ip.constants import ClientHttpAccessConstant


class MsgBidOver(ObjectWithIndentRepr):
    def __init__(self, stocks):
        self.stocks = stocks  # type: pdDF


class MsgPushStocks(ObjectWithIndentRepr):
    def __init__(self, stocks):
        self.stocks = stocks  # type: pdDF


class MsgAddPushStocks(ObjectWithIndentRepr):
    def __init__(self, stock_list):
        self.stock_list = stock_list  # type: List


class MsgBidOver(ObjectWithIndentRepr):
    def __init__(self, stocks):
        self.stocks = stocks


class MsgQuitLoop(ObjectWithRepr):
    pass


class MsgBeforeTrade(ObjectWithIndentRepr):
    pass


class MsgAfterTrade(ObjectWithIndentRepr):
    pass


class TradeId:
    data_server = 'DATA_SERVER'
    trade_manager = 'TRAD_MANAGE'


class StockTerm:
    open = 'open'
    close = 'close'
    low = 'low'
    high = 'high'
    scale = 'scale'


class PushInterval:
    day = 'day'
    minute = 'minute'
    second = 'second'


kca_ = ClientHttpAccessConstant

stock_start_day = datetime.date(1990, 12, 19)
stock_start_datetime = datetime.datetime(1990, 12, 19)

trade_bid_time = datetime.time(9, 15, 0)
trade_bid_end_time = datetime.time(9, 25, 0)
trade1_time = datetime.time(9, 30, 0)
trade_break_time = datetime.time(11, 30, 0)
trade2_time = datetime.time(13, 0, 0)
trade_end_time = datetime.time(15, 0, 0)


def test():
    print(MsgQuitLoop())
