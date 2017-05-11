from contextlib import suppress
from queue import Empty

from common.log_helper import jqd
from data_server.day_data_manager import update_etf
from stock_basic.stock_helper import etf_t1, etf_t0
from trade.comm_message import CommMessage
from trade.trade_constant import *

_tcc = TradeCommicationConstant


def thread_buy_after_drop(**param):
    obj = BuyAfterDrop(param)
    obj.run_loop()


class BuyAfterDrop:
    def __init__(self, param_dict):
        self.realtime_stock_info = None
        self.drop_days = param_dict[ModelConstant.bsm_drop_days]
        self.trade_loop_queue = param_dict[_tcc.id_trade_manager]
        self.data_server_queue = param_dict[_tcc.id_data_server]
        self.name = param_dict[_tcc.model_name]
        self.self_queue = param_dict[self.name]
        self.etf_day_data = None

        self.prepare()
        self.run_loop()

    def prepare(self):
        self.etf_day_data = update_etf()

    def run_loop(self):
        self.data_server_queue.put(
            CommMessage(self.name, _tcc.msg_set_monitor_stock,
                        [*etf_t1, *etf_t0]))

        while True:
            with suppress(Empty):
                msg = self.self_queue.get()
                self.dispatch_msg(msg)

    def on_realtime_stock_info(self, sender, param):
        del sender
        self.realtime_stock_info = param

    def dispatch_msg(self, commmsg: CommMessage):
        jqd(f'BuyAfterDrop: Receive Message: {commmsg}')
        sender = commmsg.sender
        func = self.find_operation(commmsg.operation)
        param = commmsg.param
        func(sender, param)

    def find_operation(self, operation_name):
        operdict = {_tcc.msg_push_realtime_stocks: self.on_realtime_stock_info}
        return operdict[operation_name]


def main():
    pass


if __name__ == '__main__':
    main()
