import datetime as dt
import queue
import threading
from unittest import TestCase

import common.helper as hp
from common.log_helper import jqd
from data_server.data_server_main import thread_data_server_loop
from stock_basic.stock_helper import etf_t0
from trade.comm_message import CommMessage
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import *

_tcc = TradeCommicationConstant


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
            kwargs={_tcc.id_data_server: data_server_queue,
                    _tcc.id_trade_manager: trading_queue,
                    _tcc.model_queue_dict: {_tcc.idm_buy_after_drop: model_queue},
                    _tcc.datetime_manager: datetime_manager,
                    _tcc.push_realtime_interval: push_realtime_interval})
        data_server_queue.put(
            CommMessage(_tcc.idm_buy_after_drop, _tcc.msg_set_monitored_stock,
                        [*etf_t0]))

        data_server_thread.start()
        sleep_seconds = 5
        # Time is not accurate, so substract 0.5
        datetime_manager.sleep(sleep_seconds - 0.5)
        data_server_queue.put(
            CommMessage(_tcc.id_trade_manager, _tcc.msg_quit_loop, None))
        data_server_thread.join()
        assert len(model_queue.queue) == 3
        for val in model_queue.queue:
            assert val.operation == _tcc.msg_push_realtime_stocks

    def test_data_server_trade_msg(self):
        data_server_queue = queue.Queue()
        trading_queue = queue.Queue()
        model_queue = queue.Queue()
        datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 29, 58)), 2)
        # For speed2 each call need 200ms
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={_tcc.id_data_server: data_server_queue,
                    _tcc.id_trade_manager: trading_queue,
                    _tcc.model_queue_dict: {_tcc.idm_buy_after_drop: model_queue},
                    _tcc.datetime_manager: datetime_manager,
                    _tcc.push_realtime_interval: push_realtime_interval})
        data_server_queue.put(
            CommMessage(_tcc.idm_buy_after_drop, _tcc.msg_set_monitored_stock,
                        [*etf_t0]))

        data_server_thread.start()
        sleep_seconds = 5
        # Time is not accurate, so substract 0.5
        datetime_manager.sleep(sleep_seconds - 0.5)
        data_server_queue.put(
            CommMessage(_tcc.id_trade_manager, _tcc.msg_quit_loop, None))
        data_server_thread.join()
        # jqd(model_queue.queue)
        jqd('Len', len(model_queue.queue))
        assert len(model_queue.queue) == int(sleep_seconds / push_realtime_interval)
        for val in model_queue.queue:
            assert val.operation == _tcc.msg_push_realtime_stocks

    def test_data_server_before_trade_msg(self):
        data_server_queue = queue.Queue()
        trading_queue = queue.Queue()
        model_queue = queue.Queue()
        datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 25, 0)), 2)
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            kwargs={_tcc.id_data_server: data_server_queue,
                    _tcc.id_trade_manager: trading_queue,
                    _tcc.model_queue_dict: {_tcc.idm_buy_after_drop: model_queue},
                    _tcc.datetime_manager: datetime_manager,
                    _tcc.push_realtime_interval: push_realtime_interval})
        data_server_thread.start()
        data_server_queue.put(
            CommMessage(_tcc.idm_buy_after_drop, _tcc.msg_set_monitored_stock,
                        [*etf_t0]))

        sleep_seconds = 5
        datetime_manager.sleep(sleep_seconds)
        data_server_queue.put(
            CommMessage(_tcc.id_trade_manager, _tcc.msg_quit_loop, None))
        data_server_thread.join()
        assert len(model_queue.queue) == 0
        for val in model_queue.queue:
            assert val.operation == _tcc.msg_push_realtime_stocks
