import datetime
import queue
import threading
from typing import Dict

import jsonpickle
import pandas

from common.datetime_manager import DateTimeManager
from common.log_helper import jqd, mylog
from data_manager.data_server_main import DataServer
from stock_utility.client_access import _visit_client_server, is_client_server_running
from trading.base_structure.trade_constants import ktc_, kca_
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

        # Queue member
        self.self_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        # Trade models
        self.trade_models = trade_models

        # Trade context
        self.trade_context = self.init_trade_context()
        self.init_trade_context()

        self.threads = {}  # type: Dict[threading.Thread, str]

        self.need_update_entrust_status = False

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
        self.threads[data_server_thread] = ktc_.id_data_server

        for model_class in self.trade_models:
            def thread_fun():
                runner = ModelRunnerThread(self.trade_context,
                                           model_class(self.trade_context))
                runner.run_loop()

            thread = threading.Thread(target=thread_fun)
            self.threads[thread] = model_class.name()
            thread.start()

    def init_trade_context(self):
        model_queue_dict = {}
        for model_cls in self.trade_models:
            model_queue_dict[model_cls.name()] = queue.Queue()

        queue_dict = {ktc_.id_trade_manager: self.self_queue,
                      ktc_.id_data_server: self.data_server_queue,
                      **model_queue_dict}

        trade_context = TradeContext(queue_dict)
        trade_context.thread_local.name = ktc_.id_trade_manager
        return trade_context

    def query_initial_account_info(self):
        if is_client_server_running():
            params = {kca_.operation: kca_.query_account_info,
                      kca_.account_info_type: kca_.all}
            success, resp_text = _visit_client_server(params)
            account_info = jsonpickle.loads(resp_text)
            self.trade_context.set_account_info(account_info)

    def run_loop(self):
        self.query_initial_account_info()
        self.handle_msgs()

    def handle_msgs(self):
        while 1:
            try:
                msg = self.self_queue.get(timeout=3)
            except queue.Empty:
                continue
            self.log(f'ReceiveMessage: {msg}')
            if msg.operation == ktc_.msg_quit_loop:
                for thread, name in self.threads.items():
                    self.log(f'Wait for thread {name} to exit')
                    thread.join()
                return
            self.dispatch_msgs(msg)

    def on_msg_buy_or_sell_or_cancel_stock(self, msg):
        success, resp_text = _visit_client_server(msg.param1, timeout=3)
        if success:
            result = jsonpickle.loads(resp_text)
            # If called sync
            if msg.result_queue:
                msg.result_queue.put(result)
            else:
                self.trade_context.push_account_info(msg.param1, result)
        else:
            mylog.warn('Visit client server failed with param', msg.param1, msg.param2)

    def on_msg_query_account_info(self, msg):
        success, resp_text = _visit_client_server(msg.param2)
        # if success:
        #     result = jsonpickle.loads(resp_text)
        #     if msg.res

    def dispatch_msgs(self, msg: TradeMessage):
        msg_map = {ktc_.msg_buy_stock: self.on_msg_buy_or_sell_or_cancel_stock,
                   ktc_.msg_sell_stock: self.on_msg_buy_or_sell_or_cancel_stock,
                   ktc_.msg_cancel_entrust: self.on_msg_buy_or_sell_or_cancel_stock}

        try:
            func = msg_map[msg.operation]
            func(msg)
        except KeyError:
            raise Exception(f'Unknown msg: {msg}')


def main():
    # begin_trade()
    test_begin_trade()


def test_begin_trade():
    trade = TradeManager(
        trade_models=[ModelBuyAfterDrop],
        datetime_manager=DateTimeManager()
    )
    trade_context = trade.trade_context

    def post_msg():
        import time
        time.sleep(3)
        trade_context.thread_local.name = 'TestThread'
        trade_context.quit_all()

    threading.Thread(target=post_msg).start()
    trade.start_threads()
    trade.run_loop()


if __name__ == '__main__':
    test_begin_trade()
    # main()
