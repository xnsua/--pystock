import datetime
import datetime as dt

import pandas as pd

from common import plPath
from common.helper import loop_for_seconds, play_wav
from config_module import myconfig


class TradeCommunicationConstant:
    id_data_server = 'id_data_server'
    id_trade_manager = 'id_trade_manager'
    model_name = 'model_name'
    idm_buy_after_drop = 'idm_buy_after_drop'
    model_queue_dict = 'model_queue_dict'

    msg_set_monitored_stock = 'msg_set_monitor_stock'
    msg_push_realtime_stocks = 'msg_push_realtime_stocks'
    msg_wait_result_queue = 'msg_wait_result_queue'

    push_realtime_interval = 'push_realtime_interval'
    trade1_timedelta = 'trade1_timedelta'
    trade2_timedelta = 'trade2_timedelta'

    datetime_manager = 'datetime_manager'
    msg_quit_loop = 'msg_quit_loop'
    msg_exception_occur = 'msg_exception_occur'
    msg_buy_stock = 'msg_buy_stock'
    msg_sell_stock = 'msg_sell_stock'
    msg_cancel_entrust = 'msg_cancel_entrust'
    msg_query_account_info = 'msg_query_account_info'


class ModelConstant:
    bsm_drop_days = 'drop_days'


class StockTimeConstant:
    not_trade_day = 'not_trade_day'
    stage_entered = 'stage_entered'

    before_bid = 'before_day_trade'
    bid_stage1 = 'bid_stage1'
    bid_stage2 = 'bid_stage2'
    bid_over = 'bid_over'
    trade1 = 'trade1'
    midnoon_break = 'midnoon_break'
    trade2 = 'trade2'
    after_trade = 'after_day_trade'

    before_bid_time = (datetime.time.min, datetime.time(9, 15, 0))
    bid_stage1_time = (datetime.time(9, 15, 0), datetime.time(9, 20, 0))
    bid_stage2_time = (datetime.time(9, 20, 0), datetime.time(9, 25, 0))
    bid_over_time = (datetime.time(9, 25, 0), datetime.time(9, 30, 0))
    trade1_time = (datetime.time(9, 30, 0), datetime.time(11, 30, 0))
    midnoon_break_time = (datetime.time(11, 30, 0), datetime.time(13, 00, 0))
    trade2_time = (datetime.time(13, 0, 0), datetime.time(15, 00, 0))
    after_trade_time = (datetime.time(15, 0, 0), datetime.time.max)

    trade_stage_dict = {before_bid: before_bid_time,
                        bid_stage1: bid_stage1_time,
                        bid_stage2: bid_stage2_time,
                        bid_over: bid_over_time,
                        trade1: trade1_time,
                        midnoon_break: midnoon_break_time,
                        trade2: trade2_time,
                        after_trade: after_trade_time}


class StockTermConstant:
    open = 'open'
    close = 'close'
    low = 'low'
    high = 'high'
    scale = 'scale'


class ClientHttpAccessConstant:
    operation = 'operation'
    stock_code = 'stock_code'
    price = 'price'
    amount = 'amount'
    entrust_type = 'entrust_type'
    entrust_id = 'entrust_id'
    account_info_type = 'account_info_type'
    buy = 'buy'
    sell = 'sell'
    cancel_entrust = 'cancel_entrust'
    query = 'query'
    buy_or_sell = 'buy_or_sell'
    fixed_price = 'fixed_price'
    query_account_info = 'query_account_info'

    myshare = "myshare"
    dayentrust = "dayentrust"
    dayfinentrust = "dayfinentrust"
    hisentrust = "hisentrust"
    hisfinentrust = "hisfinentrust"
    moneymovement = "moneymovement"
    deliveryentrust = "deliveryentrust"


kca_ = ClientHttpAccessConstant
ktc_ = TradeCommunicationConstant
kst_ = StockTermConstant
ksti_ = StockTimeConstant
kmc_ = ModelConstant


def alert_exception(seconds=3):
    val = ((myconfig.project_root / 'others' / 'alarm.wav').resolve())
    loop_for_seconds(lambda: play_wav(str(val)), seconds)


# <editor-fold desc="TradeDay">
class TradeDay:
    def __init__(self):
        self.df = self.read_df()
        self.date_map = self.build_date_map()

    def read_df(self):
        path = plPath(__file__).parent / 'trade_day.csv'
        return pd.read_csv(str(path), index_col='index')

    def build_date_map(self):
        date_map = {}
        for i in range(len(self.df.index)):
            date_map[self.df.iat[i, 0]] = i
        return date_map

    def is_trade_day(self, date_: dt.date):
        row_num = self.date_map[str(date_)]
        return self.df.iat[row_num, 1]

    def last_n_trade_day(self, date_: dt.date, days_num):
        row_num = self.date_map[str(date_)]
        n_trade_days = []
        while 1:
            if len(n_trade_days) == days_num:
                break
            if self.df.iat[row_num, 1]:
                date_str = self.df.iat[row_num, 0]
                n_trade_days.append(dt.date(*map(int, date_str.split('-'))))
            row_num -= 1
        return list(reversed(n_trade_days))


_trade_day = TradeDay()
is_trade_day = _trade_day.is_trade_day
last_n_trade_day = _trade_day.last_n_trade_day
# </editor-fold>
