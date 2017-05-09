import queue
import threading
from unittest import TestCase

from common.log_helper import jqd
from data_server.data_server_main import thread_data_server_loop
from stock_basic.stock_helper import etf_t0
from trade.comm_message import CommMessage
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import *


class TestDataServer(TestCase):
    def test_data_server_interval_msg(self):
        data_server_queue = queue.Queue()
        trading_queue = queue.Queue()
        model_queue = queue.Queue()
        datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 28, 58)), 2)
        # For speed2 each call need 200ms
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={ks_id_data_server: data_server_queue,
                    ks_id_trade_manager: trading_queue,
                    ks_model_queue_dict: {ks_idm_buy_after_drop: model_queue},
                    ks_datetime_manager: datetime_manager,
                    ks_push_realtime_interval: push_realtime_interval})
        data_server_queue.put(
            CommMessage(ks_idm_buy_after_drop, ks_msg_set_monitor_stock,
                        [*etf_t0]))

        data_server_thread.start()
        sleep_seconds = 5
        # Time is not accurate, so substract 0.5
        datetime_manager.sleep(sleep_seconds - 0.5)
        data_server_queue.put(CommMessage(ks_id_trade_manager, ks_msg_quit_loop, None))
        data_server_thread.join()
        # jqd(model_queue.queue)
        jqd('Len', len(model_queue.queue))
        assert len(model_queue.queue) == 3
        for val in model_queue.queue:
            assert val.operation == ks_msg_push_realtime_stocks

    def test_data_server_trade_msg(self):
        data_server_queue = queue.Queue()
        trading_queue = queue.Queue()
        model_queue = queue.Queue()
        datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 29, 58)), 2)
        # For speed2 each call need 200ms
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={ks_id_data_server: data_server_queue,
                    ks_id_trade_manager: trading_queue,
                    ks_model_queue_dict: {ks_idm_buy_after_drop: model_queue},
                    ks_datetime_manager: datetime_manager,
                    ks_push_realtime_interval: push_realtime_interval})
        data_server_queue.put(
            CommMessage(ks_idm_buy_after_drop, ks_msg_set_monitor_stock,
                        [*etf_t0]))

        data_server_thread.start()
        sleep_seconds = 5
        # Time is not accurate, so substract 0.5
        datetime_manager.sleep(sleep_seconds - 0.5)
        data_server_queue.put(CommMessage(ks_id_trade_manager, ks_msg_quit_loop, None))
        data_server_thread.join()
        # jqd(model_queue.queue)
        jqd('Len', len(model_queue.queue))
        assert len(model_queue.queue) == int(sleep_seconds / push_realtime_interval)
        for val in model_queue.queue:
            assert val.operation == ks_msg_push_realtime_stocks

    def test_data_server_before_trade_msg(self):
        data_server_queue = queue.Queue()
        trading_queue = queue.Queue()
        model_queue = queue.Queue()
        datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 25, 0)), 2)
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={ks_id_data_server: data_server_queue,
                    ks_id_trade_manager: trading_queue,
                    ks_model_queue_dict: {ks_idm_buy_after_drop: model_queue},
                    ks_datetime_manager: datetime_manager,
                    ks_push_realtime_interval: push_realtime_interval})
        data_server_thread.start()
        data_server_queue.put(
            CommMessage(ks_idm_buy_after_drop, ks_msg_set_monitor_stock,
                        [*etf_t0]))

        sleep_seconds = 5
        datetime_manager.sleep(sleep_seconds)
        data_server_queue.put(CommMessage(ks_id_trade_manager, ks_msg_quit_loop, None))
        data_server_thread.join()
        assert len(model_queue.queue) == 0
        for val in model_queue.queue:
            assert val.operation == ks_msg_push_realtime_stocks
