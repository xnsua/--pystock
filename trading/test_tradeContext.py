import queue
import threading
from unittest import TestCase

from common.datetime_manager import DateTimeManager
from common.helper import dt_from_time
from trading.trade_context import TradeContext
from trading.trade_helper import TradeCommunicationConstant

_tcc = TradeCommunicationConstant


class TestTradeContext(TestCase):
    def setUp(self):
        self.trade_manager_queue = queue.Queue()
        self.data_server_queue = queue.Queue()
        self.model_buy_after_drop = queue.Queue()
        queue_dict = {_tcc.id_trade_manager: self.trade_manager_queue,
                      _tcc.id_data_server: self.data_server_queue}
        self.dtm_manager = DateTimeManager(dt_from_time(9, 30, 0), 2)

        self.trade_context = TradeContext(queue_dict, self.dtm_manager)
        self.trade_context.thread_local.name = _tcc.id_trade_manager

    def tearDown(self):
        pass

    def test_send_msg(self):
        param_in = 'param_in'
        param_out = 'param_out'
        message_operation = 'message_operation'

        def thread_fetch_msg(queue_):
            val = queue_.get()
            assert val.param == param_in
            val.put_result(param_out)

        fetch_thread = threading.Thread(target=thread_fetch_msg,
                                        args=(self.trade_manager_queue,))
        fetch_thread.start()
        rval = self.trade_context.send_msg(_tcc.id_trade_manager, message_operation,
                                           param_in)
        assert rval == param_out
        fetch_thread.join()

