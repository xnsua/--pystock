import queue
import threading

import pandas as pd

from common.log_helper import jqd
from data_server.data_server_main import thread_data_server_loop
from trade.buy_after_drop import thread_buy_after_drop
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import *

pd.options.display.max_rows = 10

_tcc = TradeCommicationConstant


class Trading:
    def __init__(self, trade_model=None, datetime_manager=None):
        self.dtm = datetime_manager

        # Queue member
        self.self_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        self.model_queue_dict = {}

        # Trade models
        self.trade_models = trade_model

        # Run loop
        self.prepare()
        self.handle_msg()

    def prepare(self):
        for v in self.trade_models:
            target, model_name, param_dict = v
            new_queue = queue.Queue()
            self.model_queue_dict.update({model_name: new_queue})

        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={_tcc.id_trade_manager: self.self_queue,
                    _tcc.id_data_server: self.data_server_queue,
                    _tcc.model_queue_dict: self.model_queue_dict,
                    _tcc.datetime_manager: self.dtm})
        data_server_thread.start()

        for v in self.trade_models:
            target, model_name, param_dict = v
            thread = threading.Thread(
                target=target,
                kwargs={_tcc.id_trade_manager: self.self_queue,
                        _tcc.id_data_server: self.data_server_queue,
                        model_name: self.model_queue_dict[
                            model_name],
                        **param_dict})
            thread.start()

    def handle_msg(self):
        while 1:
            val = self.self_queue.get()
            jqd('Trading Receive Message: ', val)


def thread_begin_trade():
    trade_model = [
        (thread_buy_after_drop, _tcc.idm_buy_after_drop,
         {ModelConstant.bsm_drop_days: 2})]
    tradeloop = Trading(trade_model=trade_model,
                        datetime_manager=DateTimeManager())
    tradeloop.handle_msg()


def main():
    thread_begin_trade()
    pass


if __name__ == '__main__':
    main()
