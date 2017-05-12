import queue
import threading

import pandas as pd

from common.datetime_manager import DateTimeManager
from common.helper import dttimedelta
from data_server.data_server_main import thread_data_server_loop
from stock_basic.client_access import visit_client_server
from trade.buy_after_drop import thread_buy_after_drop
from trade.comm_message import CommMessage
from trade.trade_constant import *
from trade.trade_context import TradeContext

pd.options.display.max_rows = 10

_tcc = TradeCommicationConstant
_hc = ClientHttpAccessConstant


def thread_begin_trade():
    trade_model = [(thread_buy_after_drop, _tcc.idm_buy_after_drop,
                    {ModelConstant.bsm_drop_days: 2})]
    tradeloop = trade(trade_model=trade_model,
                      datetime_manager=DateTimeManager())
    tradeloop.handle_msg()


class trade:
    def __init__(self, trade_model=None, datetime_manager=None):
        self.dtm = datetime_manager

        # Queue member
        self.trade_manager_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        # Trade models
        self.trade_models = trade_model

        # Trade context
        self.trade_context = None
        self.init_trade_context()

        # Run loop
        self.prepare()
        self.handle_msg()

        self.msg_map = {
            _hc.buy: self.buy_stock,
            _hc.sell: self.sell_stock,
            _hc.cancel_entrust: self.cancel_entrust,
            _hc.query_account_info: self.query_account_info
        }

    def init_trade_context(self):
        model_queue_dict = {}
        for arget, model_name, param in self.trade_models:
            model_queue_dict[model_name] = queue.Queue

        queue_dict = {_tcc.id_trade_manager: self.trade_manager_queue,
                      _tcc.id_data_server: self.data_server_queue,
                      **model_queue_dict}

        self.trade_context = TradeContext(queue_dict, self.dtm)
        self.trade_context.thread_local.name = _tcc.id_trade_manager

    def prepare(self):
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            args=(self.trade_context,),
            kwargs={
                _tcc.push_realtime_interval: 1,
                _tcc.trade1_timedelta: dttimedelta(seconds=60),
                _tcc.trade2_timedelta: dttimedelta(seconds=30)
            })
        data_server_thread.start()

        for val in self.trade_models:
            target, model_name, param_dict = val
            thread = threading.Thread(
                target=target,
                args=(self.trade_context,),
                kwargs=param_dict)
            thread.start()

    def handle_msg(self):
        while 1:
            msg = self.trade_manager_queue.get()
            self.dispatch_msg(msg)

    def dispatch_msg(self, msg: CommMessage):
        operlist = [_tcc.msg_buy_stock, _tcc.msg_sell_stock,
                    _tcc.msg_cancel_entrust, _tcc.msg_query_account_info]
        if msg.operation in operlist:
            visit_client_server(msg.param)
        raise Exception(f'Unknown msg: {msg}')


def main():
    thread_begin_trade()
    pass


if __name__ == '__main__':
    main()
