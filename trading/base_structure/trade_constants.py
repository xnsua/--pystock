import datetime

from common.base_functions import object_with_repr
from common.scipy_helper import pdDF
from ip.constants import ClientHttpAccessConstant


class MsgPushStocks(object_with_repr):
    def __init__(self, stocks):
        self.stocks = stocks  # type: pdDF


class MsgAddPushStocks(object_with_repr):
    def __init__(self, stocks):
        self.stocks = stocks


class MsgQuitLoop(object_with_repr):
    pass


class TradeCommunicationConstant:
    id_data_server = 'DATA_SERVER'
    id_trade_manager = 'TRAD_MANAGE'

    msg_set_monitored_stock = 'msg_set_monitor_stock'
    msg_realtime_push = 'msg_push_realtime_stocks'
    msg_wait_result_queue = 'msg_wait_result_queue'
    msg_client_operation = 'msg_client_operation'

    msg_exception_occur = 'msg_exception_occur'
    msg_buy_stock = 'msg_buy_stock'
    msg_sell_stock = 'msg_sell_stock'
    msg_cancel_entrust = 'msg_cancel_entrust'
    msg_query_account_info = 'msg_query_account_info'

    msg_before_trading = 'msg_before_trading'
    msg_after_trading = 'msg_after_trading'
    msg_bid_over = 'msg_is_bid_over'
    msg_push_account_info = 'msg_push_account_info'

    msg_quit_loop = 'msg_quit_loop'


class ModelConstant:
    bsm_drop_days = 'drop_days'


# class StockTimeConstant:
#
#     before_bid = 'before_day_trade'
#     bid_stage1 = 'bid_stage1'
#     bid_stage2 = 'bid_stage2'
#     bid_over = 'bid_over'
#     trade1 = 'trade1'
#     midnoon_break = 'midnoon_break'
#     trade2 = 'trade2'
#     after_trade = 'after_day_trade'
#
#     before_bid_time = (datetime.time.min, datetime.time(9, 15, 0))
#     bid_stage1_time = (datetime.time(9, 15, 0), datetime.time(9, 20, 0))
#     bid_stage2_time = (datetime.time(9, 20, 0), datetime.time(9, 25, 0))
#     bid_over_time = (datetime.time(9, 25, 0), datetime.time(9, 30, 0))
#     trade1_time = (datetime.time(9, 30, 0), datetime.time(11, 30, 0))
#     midnoon_break_time = (datetime.time(11, 30, 0), datetime.time(13, 00, 0))
#     trade2_time = (datetime.time(13, 0, 0), datetime.time(15, 00, 0))
#     after_trade_time = (datetime.time(15, 0, 0), datetime.time.max)
#
#     trade_stage_dict = {before_bid: before_bid_time,
#                         bid_stage1: bid_stage1_time,
#                         bid_stage2: bid_stage2_time,
#                         bid_over: bid_over_time,
#                         trade1: trade1_time,
#                         midnoon_break: midnoon_break_time,
#                         trade2: trade2_time,
#                         after_trade: after_trade_time}
#

class StockTermConstant:
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
ktc_ = TradeCommunicationConstant
kst_ = StockTermConstant
kmc_ = ModelConstant

stock_start_day = datetime.date(1990, 12, 19)
stock_start_datetime = datetime.datetime(1990, 12, 19)

trade_bid_time = datetime.time(9, 15, 0)
trade_bid_end_time = datetime.time(9, 25, 0)
trade1_time = datetime.time(9, 30, 0)
trade_break_time = datetime.time(11, 30, 0)
trade2_time = datetime.time(13, 0, 0)
trade_end_time = datetime.time(15, 0, 0)
