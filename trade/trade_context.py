import queue
import threading

from common.helper import ObjectCabinet
from trade.comm_message import CommMessage
from trade.trade_constant import ClientHttpAccessConstant, TradeCommicationConstant

_hc = ClientHttpAccessConstant
_tcc = TradeCommicationConstant


class TradeContext:
    def __init__(self):
        self.queue_dict = {}
        self.queue_cabinet = ObjectCabinet(queue.Queue, None)
        self.thread_local = threading.local()
        self.thread_local.name = None

    # <editor-fold desc="Private">
    def __fetch_model_queue(self, model_name):
        self.queue_dict[model_name] = queue.Queue()
        return self.queue_dict[model_name]

    def __find_queue_by_name(self, name):
        return self.queue_dict[name]

    # </editor-fold>

    def send_msg(self, sender, dest, operation, param_dict):
        dest_queue = self.__find_queue_by_name(dest)
        with self.queue_cabinet.use_one() as result_queue:
            msg = CommMessage(sender, operation,
                              {**param_dict, _tcc.msg_wait_result_queue: result_queue})
            dest_queue.put(msg)
            result = result_queue.get()
        return result

    def send_msg_to_trade_manager(self, msg, params):
        trade_manager_queue = self.queue_dict[_tcc.id_trade_manager]
        sender = self.thread_local.name
        rval = self.send_msg(sender, trade_manager_queue, msg, params)
        return rval

    def buy_stock(self, stock_code, price, amount, entrust_type):
        params = {_hc.stock_code: stock_code,
                  _hc.price: price,
                  _hc.amount: amount,
                  _hc.entrust_type: entrust_type}
        return self.send_msg_to_trade_manager(_tcc.msg_buy_stock, params)

    def sell_stock(self, stock_code, price, amount, entrust_type):
        params = {_hc.stock_code: stock_code,
                  _hc.price: price,
                  _hc.amount: amount,
                  _hc.entrust_type: entrust_type}
        return self.send_msg_to_trade_manager(_tcc.msg_sell_stock, params)

    def cancel_entrustment(self, entrust_id, stockcode, buy_or_sell):
        params = {_hc.entrust_id: entrust_id,
                  _hc.stock_code: stockcode,
                  _hc.buy_or_sell: buy_or_sell}
        return self.send_msg_to_trade_manager(_tcc.msg_cancel_entrust, params)

    def query_account_info(self, account_info_type):
        params = {_hc.account_info_type: account_info_type}
        return self.send_msg_to_trade_manager(_tcc.msg_query_account_info, params)
