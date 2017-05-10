import queue

from common.helper import ObjectCabinet
from trade.comm_message import CommMessage
from trade.trade_constant import ks_msg_wait_result_queue


class TradeContext:
    def __init__(self):
        self.queue_dict = {}
        self.cabinet_of_wait_result_queue = queue.Queue()
        self.queue_cabinet = ObjectCabinet(queue.Queue)

    def fetch_model_queue(self, model_name):
        self.queue_dict[model_name] = queue.Queue()
        return self.queue_dict[model_name]

    def find_queue_by_name(self, name):
        return self.queue_dict[name]

    def send_message(self, sender, dest, operation, param_dict):
        dest_queue = self.find_queue_by_name(dest)
        with self.queue_cabinet.use_one() as result_queue:
            msg = CommMessage(sender, operation,
                              {**param_dict, ks_msg_wait_result_queue: result_queue})
            dest_queue.put(msg)
            result = result_queue.get()
        return result

    def buy_stock(self, stock_code, price, amount, mode):
        params = {ks_stock_code: stock_code,
                  ks_price: price,
                  ks_amount: amount,
                  k
                  }
