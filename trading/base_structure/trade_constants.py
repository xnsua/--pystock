from typing import List

from common.base_functions import ObjectWithIndentRepr, ObjectWithRepr
from common.scipy_helper import pdDF


class MsgBidOver(ObjectWithIndentRepr):
    def __init__(self, stocks):
        self.stocks = stocks  # type: pdDF


class MsgPushRealTimePrice(ObjectWithIndentRepr):
    def __init__(self, stocks):
        self.stocks = stocks  # type: pdDF


class MsgAddRealTimeStocks(ObjectWithIndentRepr):
    def __init__(self, stock_list):
        self.stock_list = stock_list  # type: List



class MsgQuitLoop(ObjectWithRepr):
    pass


class MsgBeforeTrade(ObjectWithIndentRepr):
    pass


class MsgAfterTrade(ObjectWithIndentRepr):
    pass


class TradeId:
    data_server = 'DATA_SERVER'
    trade_manager = 'TRAD_MANAGE'


class PushInterval:
    day = 'day'
    minute = 'minute'
    second = 'second'


def test():
    print(MsgQuitLoop())
