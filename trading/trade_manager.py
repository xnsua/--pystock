import datetime
import queue
import threading
from typing import Dict, Tuple

import pandas

from data_manager.data_server_main import DataServer
from ip.st import OperQuery
from project_helper.phelper import mylog, jqd
from stock_utility.client_access import is_client_server_running, \
    fire_operation
from trading.base_structure.trade_constants import ktc_, kca_
from trading.base_structure.trade_message import TradeMessage
from trading.model_runner import ModelRunnerThread
from trading.models.model_buy_after_drop import ModelBuyAfterDrop
from trading.trade_context import TradeContext

pandas.options.display.max_rows = 10


def begin_trade():
    trade = TradeManager(trade_models=[ModelBuyAfterDrop])
    trade.start_threads()
    trade.handle_msgs()


class TradeManager:
    def __init__(self, trade_models=None):

        # Queue member
        self.self_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        # Trade models
        self.trade_models = trade_models

        # Trade context
        self.trade_context = self.init_trade_context()
        self.init_trade_context()
        self.account_manager = self.trade_context.account_manager

        self.threads = {}  # type: Dict[threading.Thread, str]

        self.need_update_entrust_status = False

    def log(self, msg, level=None):
        text = f'{ktc_.id_trade_manager}:: {msg}'
        if not level:
            jqd(text)
        else:
            level(text)

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
            oper = OperQuery(kca_.all)
            success, rs_oper = fire_operation(oper)  # type: Tuple[bool, OperQuery]

            if success and rs_oper.result.success:
                self.trade_context.account_manager \
                    .set_init_account_info(rs_oper.result.data)
            else:
                raise Exception('Query account info failed')

        else:
            raise Exception('Cannot connect to client server')

    def run_loop(self):
        try:
            self.query_initial_account_info()
        except Exception:
            mylog.exception('Query initial account info failed')
            self.trade_context.quit_all()

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

    def on_msg_client_operation(self, msg: TradeMessage):
        msg_result = fire_operation(msg.param1)
        self.account_manager.on_operation_result(msg_result)
        msg.try_put_result(msg_result)

    def dispatch_msgs(self, msg: TradeMessage):
        msg_map = {ktc_.msg_client_operation: self.on_msg_client_operation}

        try:
            func = msg_map[msg.operation]
            func(msg)
        except KeyError:
            raise Exception(f'Unknown msg: {msg}')


def main():
    # begin_trade()
    test_begin_trade()


def test_begin_trade():
    trade = TradeManager(trade_models=[ModelBuyAfterDrop])
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
