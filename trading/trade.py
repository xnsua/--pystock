import queue
import threading

import pandas

from common.datetime_manager import DateTimeManager
from common.helper import dt
from data_server.data_server_main import thread_data_server_loop
from stock_basic.client_access import visit_client_server
from trading.buy_after_drop import thread_buy_after_drop
from trading.comm_message import CommMessage
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_, ModelConstant

pandas.options.display.max_rows = 10

def thread_begin_trade():
    trade_model = [(thread_buy_after_drop, ktc_.idm_buy_after_drop,
                    {ModelConstant.bsm_drop_days: 2})]
    trade_loop = Trade(trade_model=trade_model,
                       datetime_manager=DateTimeManager())
    trade_loop.handle_msg()


class Trade:
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

    def init_trade_context(self):
        model_queue_dict = {}
        for target, model_name, param in self.trade_models:
            model_queue_dict[model_name] = queue.Queue

        queue_dict = {ktc_.id_trade_manager: self.trade_manager_queue,
                      ktc_.id_data_server: self.data_server_queue,
                      **model_queue_dict}

        self.trade_context = TradeContext(queue_dict, self.dtm)
        self.trade_context.thread_local.name = ktc_.id_trade_manager

    def prepare(self):
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            args=(self.trade_context,),
            kwargs={
                ktc_.push_realtime_interval: 1,
                ktc_.trade1_timedelta: (dt.timedelta(seconds=60), dt.timedelta(seconds=60)),
                ktc_.trade2_timedelta: (dt.timedelta(seconds=30), dt.timedelta(seconds=30))
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
        operation_list = [ktc_.msg_buy_stock, ktc_.msg_sell_stock,
                          ktc_.msg_cancel_entrust, ktc_.msg_query_account_info]
        if msg.operation in operation_list:
            visit_client_server(msg.param)

        raise Exception(f'Unknown msg: {msg}')

def main():
    thread_begin_trade()
    pass


if __name__ == '__main__':
    main()
