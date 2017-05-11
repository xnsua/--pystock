import datetime as dt
import queue
import threading
from unittest import TestCase

import common.helper as hp
from common.log_helper import jqd
from data_server.data_server_main import thread_data_server_loop
from stock_basic.stock_helper import etf_t0
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import *
from trade.trade_context import TradeContext

_tcc = TradeCommicationConstant


class TestDataServer(TestCase):
    def setUp(self):
        self.trade_manager_queue = queue.Queue()
        self.data_server_queue = queue.Queue()
        self.model_buy_after_drop = queue.Queue()
        queue_dict = {_tcc.id_trade_manager: self.trade_manager_queue,
                      _tcc.id_data_server: self.data_server_queue,
                      _tcc.idm_buy_after_drop: self.model_buy_after_drop}
        self.dtm_manager = DateTimeManager(hp.dt_from_time(9, 30, 0), 2)

        self.trade_context = TradeContext(queue_dict, self.dtm_manager)
        self.trade_context.thread_local.name = _tcc.id_trade_manager

    def test_data_server_interval_trade_time_msg(self):
        self.trade_context.dtm = DateTimeManager(hp.to_datetime(dt.time(9, 28, 58)), 2)
        # For speed2 each call need 200ms
        push_realtime_interval = 1
        data_server_thread = threading.Thread(
            target=thread_data_server_loop,
            args=(self.trade_context,),
            kwargs={_tcc.push_realtime_interval: push_realtime_interval})

        trade_manager_queue = self.trade_context.queue_dict[_tcc.id_trade_manager]
        data_server_thread.start()
        self.trade_context.add_monitored_stock([*etf_t0])
        sleep_seconds = 5
        # Time is not accurate, so substract 0.5
        self.trade_context.dtm.sleep(sleep_seconds - 0.5)

        self.trade_context.send_msg(_tcc.id_data_server, _tcc.msg_quit_loop, None)
        data_server_thread.join()
        # Use trade_manager_queue as data server queue
        data_server_queue = trade_manager_queue
        jqd(len(data_server_queue.queue))
        assert len(data_server_queue.queue) == 3
        for val in data_server_queue.queue:
            assert val.operation == _tcc.msg_push_realtime_stocks

            # def test_data_server_trade_msg(self):
            #     datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 28, 58)), 2)
            #     # For speed2 each call need 200ms
            #     push_realtime_interval = 1
            #     data_server_thread = threading.Thread(
            #         target=thread_data_server_loop,
            #         args=(self.trade_context,),
            #         kwargs={_tcc.push_realtime_interval: push_realtime_interval})
            #     self.trade_context.add_monitored_stock([*etf_t0])
            #
            #     data_server_thread.start()
            #     sleep_seconds = 5
            #     # Time is not accurate, so substract 0.5
            #     datetime_manager.sleep(sleep_seconds - 0.5)
            #
            #     self.trade_context.send_msg(_tcc.id_data_server, _tcc.msg_quit_loop, None)
            #     data_server_thread.join()
            #     data_server_queue = self.trade_context.queue_dict[_tcc.id_data_server]
            #     assert len(data_server_queue.queue) == 3
            #     for val in data_server_queue.queue:
            #         assert val.operation == _tcc.msg_push_realtime_stocks
            #
            # def test_data_server_before_trade_msg(self):
            #     datetime_manager = DateTimeManager(hp.to_datetime(dt.time(9, 28, 58)), 2)
            #     # For speed2 each call need 200ms
            #     push_realtime_interval = 1
            #     data_server_thread = threading.Thread(
            #         target=thread_data_server_loop,
            #         args=self.trade_context,
            #         kwargs={_tcc.push_realtime_interval: push_realtime_interval})
            #     self.trade_context.add_monitored_stock([*etf_t0])
            #
            #     data_server_thread.start()
            #     sleep_seconds = 5
            #     # Time is not accurate, so substract 0.5
            #     datetime_manager.sleep(sleep_seconds - 0.5)
            #
            #     self.trade_context.send_msg(_tcc.id_data_server, _tcc.msg_quit_loop, None)
            #     data_server_thread.join()
            #     data_server_queue = self.trade_context.queue_dict[_tcc.id_data_server]
            #     assert len(data_server_queue.queue) == 3
            #     for val in data_server_queue.queue:
            #         assert val.operation == _tcc.msg_push_realtime_stocks
            #
