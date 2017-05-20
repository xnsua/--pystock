import queue
import threading

from common.helper import ObjectCabinet
from trading.base_structure.trade_constants import ktc_, kca_
from trading.base_structure.trade_message import TradeMessage


class TradeContext:
    def __init__(self, queue_dict, datetime_manager):
        self.dtm = datetime_manager
        self.queue_dict = queue_dict

        self.queue_cabinet = ObjectCabinet(queue.Queue, None)
        self.thread_local = threading.local()
        self.thread_local.name = None

    def on_init_model(self, model_context):
        pass

    def update_queue_dict(self, queue_dict):
        self.queue_dict.update(queue_dict)

    def post_msg(self, dest, operation, param1, param2=None):
        assert self.thread_local.name
        dest_queue = self.queue_dict[dest]
        msg = TradeMessage(self.thread_local.name, operation, param1, param2,
                           result_queue=None, msg_time=self.dtm.now())
        dest_queue.put(msg)

    def send_msg(self, dest, operation, param1, param2=None):
        assert self.thread_local.name
        dest_queue = self.queue_dict[dest]
        with self.queue_cabinet.use_one() as result_queue:
            msg = TradeMessage(self.thread_local.name, operation, param1, param2,
                               result_queue=result_queue, msg_time=self.dtm.now())
            dest_queue.put(msg)
            result = result_queue.get()
        return result

    def get_current_thread_queue(self):
        assert self.thread_local.name
        return self.queue_dict[self.thread_local.name]

    def push_realtime_info(self, dest, stocks):
        self.post_msg(dest, ktc_.msg_realtime_push, stocks)

    def add_monitored_stock(self, stocks):
        self.send_msg(ktc_.id_data_server, ktc_.msg_set_monitored_stock, stocks)

    def buy_stock(self, stock_code, price, amount, entrust_type):
        params = {kca_.operation: kca_.buy,
                  kca_.stock_code: stock_code,
                  kca_.price: price,
                  kca_.amount: amount,
                  kca_.entrust_type: entrust_type}
        return self.send_msg(ktc_.id_trade_manager, ktc_.msg_buy_stock, params)

    def sell_stock(self, stock_code, price, amount, entrust_type):
        params = {kca_.operation: kca_.sell,
                  kca_.stock_code: stock_code,
                  kca_.price: price,
                  kca_.amount: amount,
                  kca_.entrust_type: entrust_type}
        return self.send_msg(ktc_.id_trade_manager, ktc_.msg_sell_stock, params)

    def cancel_entrustment(self, entrust_id, stock_code, buy_or_sell):
        params = {kca_.operation: kca_.cancel_entrust,
                  kca_.entrust_id: entrust_id,
                  kca_.stock_code: stock_code,
                  kca_.buy_or_sell: buy_or_sell}
        return self.send_msg(ktc_.id_trade_manager, ktc_.msg_cancel_entrust, params)

    def query_account_info(self, account_info_type):
        params = {kca_.operation: kca_.query_account_info,
                  kca_.account_info_type: account_info_type}
        return self.send_msg(ktc_.id_trade_manager, ktc_.msg_query_account_info, params)

    def quit_all(self):
        for key in self.queue_dict:
            self.post_msg(key, ktc_.msg_quit_loop, None, None)
