import queue
from unittest import TestCase

from common import hp
from common.datetime_manager import DateTimeManager
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_


class TestBuyAfterDrop(TestCase):
    def setUp(self):
        self.trade_manager_queue = queue.Queue()
        self.data_server_queue = queue.Queue()
        self.model_buy_after_drop = queue.Queue()
        queue_dict = {ktc_.id_trade_manager: self.trade_manager_queue,
                      ktc_.id_data_server: self.data_server_queue,
                      ktc_.idm_buy_after_drop: self.model_buy_after_drop}
        self.dtm_manager = DateTimeManager(hp.dt_from_time(9, 30, 0), 2)

        self.trade_context = TradeContext(queue_dict, self.dtm_manager)
        self.trade_context.thread_local.name = ktc_.id_trade_manager

    def test_on_realtime_stock_info(self):
        self.fail()
