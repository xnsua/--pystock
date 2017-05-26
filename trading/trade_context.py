import queue
import threading

from common.helper import ObjectCabinet
from stock_utility.client_access import fire_operation
from trading.account_manager import AccountManager
from trading.base_structure.trade_constants import ktc_
from trading.base_structure.trade_message import TradeMessage


class TradeContext:
    def __init__(self, queue_dict):
        self.queue_dict = queue_dict

        self.queue_cabinet = ObjectCabinet(queue.Queue, None)
        self.thread_local = threading.local()
        self.thread_local.name = None

        self.account_manager = AccountManager()

    def post_msg(self, dest, operation, param1, param2=None):
        assert self.thread_local.name
        dest_queue = self.queue_dict[dest]
        msg = TradeMessage(self.thread_local.name, operation, param1, param2, result_queue=None)
        dest_queue.put(msg)

    def send_msg(self, dest, operation, param1, param2=None):
        assert self.thread_local.name
        dest_queue = self.queue_dict[dest]
        with self.queue_cabinet.use_one() as result_queue:
            msg = TradeMessage(self.thread_local.name, operation, param1, param2,
                               result_queue=result_queue)
            dest_queue.put(msg)
            result = result_queue.get()
        return result

    def get_current_thread_queue(self):
        assert self.thread_local.name
        return self.queue_dict[self.thread_local.name]

    def add_monitored_stock(self, stocks):
        self.send_msg(ktc_.id_data_server, ktc_.msg_set_monitored_stock, stocks)

    def push_realtime_info(self, dest, stocks):
        self.post_msg(dest, ktc_.msg_realtime_push, stocks)

    def fire_order(self, order):
        fire_operation(order)

    def quit_all(self):
        for key in self.queue_dict:
            self.post_msg(key, ktc_.msg_quit_loop, None, None)

    def _is_model_queue(self, queue_name):
        return queue_name != ktc_.id_data_server and queue_name != ktc_.id_trade_manager
