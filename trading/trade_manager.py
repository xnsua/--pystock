import datetime
import queue
import threading
from typing import Dict

import pandas

from data_manager.data_server_main import DataServer
from ip.st import ClientOperQuery, ClientOperBase
from project_helper.logbook_logger import mylog
from trading.base_structure.trade_constants import TradeId, kca_, MsgQuitLoop
from trading.base_structure.trade_message import TradeMessage
from trading.client_access import is_client_server_running, \
    fire_operation
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
        self.account_manager = self.trade_context.account_manager

        self.data_push_time_interval = datetime.timedelta(seconds=2)
        self.client_push_time_interval = datetime.timedelta(seconds=2)

        self.threads = {}  # type: Dict[threading.Thread, str]

    def start_threads(self):

        def thread_data_server():
            data_server = DataServer(self.trade_context,
                                     push_time_interval=self.data_push_time_interval)
            data_server.run_loop()

        data_server_thread = threading.Thread(target=thread_data_server)
        data_server_thread.start()
        self.threads[data_server_thread] = TradeId.data_server

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

        queue_dict = {TradeId.trade_manager: self.self_queue,
                      TradeId.data_server: self.data_server_queue,
                      **model_queue_dict}

        trade_context = TradeContext(queue_dict)
        trade_context.thread_local.name = TradeId.trade_manager
        return trade_context

    def query_account_info(self):
        if is_client_server_running():
            query = ClientOperQuery(kca_.account_info)
            result = fire_operation(query)
            query.result = result
            self.account_manager.on_operation_result(query)
        else:
            raise Exception('Cannot connect to client server')

    def run_loop(self):
        mylog.info('Trade manager running .....')
        try:
            self.query_account_info()
        except Exception:
            mylog.exception('Query account info failed')
            self.trade_context.quit_all()

        self.start_threads()

        self.handle_msgs()
        mylog.info('Quit the program.')

    def handle_msgs(self):
        while 1:
            try:
                # Haitong do not allow too fast operation
                interval = self.client_push_time_interval.total_seconds()
                msg = self.self_queue.get(timeout=interval)
            except queue.Empty:
                self.do_when_idle()
                continue
            mylog.info(f'ReceiveMessage {msg}')
            if isinstance(msg.operation, MsgQuitLoop):
                for thread, name in self.threads.items():
                    mylog.info(f'Wait for thread {name} to exit')
                    thread.join()
                return
            self.dispatch_msgs(msg)

    def dispatch_msgs(self, msg: TradeMessage):
        if isinstance(msg.operation, ClientOperBase):
            msg_result = fire_operation(msg.operation)
            msg.operation.result = msg_result
            msg.try_put_result(msg_result)
            self.account_manager.on_operation_result(msg.operation)
        else:
            raise Exception(f'Unrecognized Message: {msg}')

    def do_when_idle(self):
        if self.account_manager.need_client_push:
            self.trade_context.post_msg(TradeId.trade_manager, ClientOperQuery(kca_.account_info))


def main():
    # begin_trade()
    tes_begin_trade()


def tes_begin_trade():
    trade = TradeManager(trade_models=[ModelBuyAfterDrop])
    trade_context = trade.trade_context

    # noinspection PyUnusedLocal
    def post_msg():
        import time
        time.sleep(3)
        trade_context.thread_local.name = 'TestThread'
        trade_context.quit_all()

    # threading.Thread(target=post_msg).start()
    # trade.start_threads()
    trade.run_loop()


if __name__ == '__main__':
    # with DateTimeManager(dt_from_time(9, 26, 0)):
    tes_begin_trade()

