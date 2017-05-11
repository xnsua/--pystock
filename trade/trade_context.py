import queue
import threading

from common.helper import ObjectCabinet
from trade.comm_message import CommMessage
from trade.trade_constant import ClientHttpAccessConstant, TradeCommicationConstant

_hc = ClientHttpAccessConstant
_tcc = TradeCommicationConstant


class TradeContext:
    def __init__(self, queue_dict, datetime_manager):
        self.dtm = datetime_manager
        self.queue_dict = queue_dict
        self.queue_cabinet = ObjectCabinet(queue.Queue, None)
        self.thread_local = threading.local()
        self.thread_local.name = None

    def update_queue_dict(self, queue_dict):
        self.queue_dict.update(queue_dict)

    def send_msg(self, dest, operation, param):
        assert self.thread_local.name
        dest_queue = self.queue_dict[dest]
        with self.queue_cabinet.use_one() as result_queue:
            msg = CommMessage(self.thread_local.name, operation,
                              param, result_queue)
            dest_queue.put(msg)
            result = result_queue.get()
        return result

    def push_realtime_info(self, dest, stocks):
        self.send_msg(dest, _tcc.msg_push_realtime_stocks, stocks)

    def add_monitored_stock(self, stocks):
        self.send_msg(self.thread_local.name, _tcc.id_data_server,
                      _tcc.msg_set_monitored_stock, stocks)

    def buy_stock(self, stock_code, price, amount, entrust_type):
        params = {_hc.operation: _hc.buy,
                  _hc.stock_code: stock_code,
                  _hc.price: price,
                  _hc.amount: amount,
                  _hc.entrust_type: entrust_type}
        return self.send_msg(_tcc.id_trade_manager, _tcc.msg_buy_stock, params)

    def sell_stock(self, stock_code, price, amount, entrust_type):
        params = {_hc.operation: _hc.sell,
                  _hc.stock_code: stock_code,
                  _hc.price: price,
                  _hc.amount: amount,
                  _hc.entrust_type: entrust_type}
        return self.send_msg(_tcc.id_trade_manager, _tcc.msg_sell_stock, params)

    def cancel_entrustment(self, entrust_id, stockcode, buy_or_sell):
        params = {_hc.operation: _hc.cancel_entrust,
                  _hc.entrust_id: entrust_id,
                  _hc.stock_code: stockcode,
                  _hc.buy_or_sell: buy_or_sell}
        return self.send_msg(_tcc.id_trade_manager, _tcc.msg_cancel_entrust, params)

    def query_account_info(self, account_info_type):
        params = {_hc.operation: _hc.query_account_info,
                  _hc.account_info_type: account_info_type}
        return self.send_msg(_tcc.id_trade_manager, _tcc.msg_query_account_info, params)
