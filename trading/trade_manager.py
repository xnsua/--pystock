import datetime
import queue
import threading
from typing import List

import pandas

from common.datetime_manager import DateTimeManager
from common.log_helper import jqd
from data_manager.data_server_main import DataServer
from stock_utility.client_access import visit_client_server
from trading.base_structure.trade_constants import ktc_
from trading.base_structure.trade_message import TradeMessage
from trading.model_runner import ModelRunnerThread
from trading.models.model_buy_after_drop import ModelBuyAfterDrop
from trading.trade_context import TradeContext

pandas.options.display.max_rows = 10


def begin_trade():
    trade = TradeManager(
        trade_models=[ModelBuyAfterDrop],
        datetime_manager=DateTimeManager()
    )
    trade.start_threads()
    trade.handle_msgs()


class TradeManager:
    def __init__(self, trade_models=None, datetime_manager=None):
        self.dtm = datetime_manager

        # Queue member
        self.self_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        # Trade models
        self.trade_models = trade_models

        # Trade context
        self.trade_context = self.init_trade_context()
        self.init_trade_context()

        self.threads = []  # type: List[threading.Thread]

    def log(self, msg):
        jqd(f'{ktc_.id_trade_manager}:: {msg}')

    def start_threads(self):
        self.init_trade_context()

        def thread_data_server():
            data_server = DataServer(self.trade_context,
                                     push_time_interval=datetime.timedelta(seconds=1))
            data_server.run_loop()

        data_server_thread = threading.Thread(target=thread_data_server)
        data_server_thread.start()
        self.threads.append(data_server_thread)

        for model_class in self.trade_models:
            def thread_fun():
                runner = ModelRunnerThread(self.trade_context,
                                           model_class(self.trade_context))
                runner.run_loop()

            thread = threading.Thread(target=thread_fun)
            self.threads.append(thread)
            jqd('model thread start')
            thread.start()

    def init_trade_context(self):
        model_queue_dict = {}
        for model_cls in self.trade_models:
            model_queue_dict[model_cls.__name__] = queue.Queue()

        queue_dict = {ktc_.id_trade_manager: self.self_queue,
                      ktc_.id_data_server: self.data_server_queue,
                      **model_queue_dict}

        trade_context = TradeContext(queue_dict, self.dtm)
        trade_context.thread_local.name = ktc_.id_trade_manager
        return trade_context

    def handle_msgs(self):
        while 1:
            msg = self.self_queue.get()

            self.log(f'Handle message {msg}')
            if msg.operation == ktc_.msg_quit_loop:
                for thread in self.threads:
                    thread.join()
                return
            self.dispatch_msgs(msg)

    def dispatch_msgs(self, msg: TradeMessage):
        self.log(f'Dispatch message:: {msg}')
        operation_list = [ktc_.msg_buy_stock, ktc_.msg_sell_stock,
                          ktc_.msg_cancel_entrust, ktc_.msg_query_account_info]
        if msg.operation in operation_list:
            visit_client_server(msg.param1)
        else:
            raise Exception(f'Unknown msg: {msg}')


def main():
    begin_trade()


if __name__ == '__main__':
    main()
