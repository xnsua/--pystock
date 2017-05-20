import datetime
import queue
import threading
from typing import List

import pandas

from common.datetime_manager import DateTimeManager
from data_server.data_server_main import DataServer
from stock_basic.client_access import visit_client_server
from trading.comm_message import CommMessage
from trading.model_runner import ModelRunnerThread
from trading.models.model_base import ModelBase
from trading.models.model_buy_after_drop import ModelBuyAfterDrop
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_

pandas.options.display.max_rows = 10


def begin_trade():
    model_buy_after_drop = ModelBuyAfterDrop()

    trade = TradeManager(
        trade_models=[model_buy_after_drop],
        datetime_manager=DateTimeManager()
    )
    trade.start_threads()
    trade.handle_msgs()


class TradeManager:
    def __init__(self, trade_models=None, datetime_manager=None):
        self.dtm = datetime_manager

        # Queue member
        self.trade_manager_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        # Trade models
        self.trade_models = trade_models  # type: List[ModelBase]

        # Trade context
        self.trade_context = None
        self.init_trade_context()

        self.threads = []  # type: List[threading.Thread]

    def start_threads(self):
        self.init_trade_context()

        data_server = DataServer(self.trade_context,
                                 push_time_interval=datetime.timedelta(seconds=1))
        data_server_thread = threading.Thread(target=lambda: data_server.run_loop())
        data_server_thread.start()

        for model in self.trade_models:
            model.context = self.trade_context
            thread = threading.Thread(
                target=lambda: ModelRunnerThread(self.trade_context, model).run_loop(),
            )
            self.threads.append(thread)
            thread.start()

    def init_trade_context(self):
        model_queue_dict = {}
        for model, param in self.trade_models:
            model_queue_dict[type(model).__name__] = queue.Queue

        queue_dict = {ktc_.id_trade_manager: self.trade_manager_queue,
                      ktc_.id_data_server: self.data_server_queue,
                      **model_queue_dict}

        self.trade_context = TradeContext(queue_dict, self.dtm)
        self.trade_context.thread_local.name = ktc_.id_trade_manager

    def handle_msgs(self):
        while 1:
            msg = self.trade_manager_queue.get()
            self.dispatch_msgs(msg)

    def dispatch_msgs(self, msg: CommMessage):
        operation_list = [ktc_.msg_buy_stock, ktc_.msg_sell_stock,
                          ktc_.msg_cancel_entrust, ktc_.msg_query_account_info]
        if msg.operation in operation_list:
            visit_client_server(msg.param1)

        if msg.operation == ktc_.msg_quit_loop:
            for thread in self.threads:
                thread.join()

        raise Exception(f'Unknown msg: {msg}')


def main():
    begin_trade()


if __name__ == '__main__':
    main()
