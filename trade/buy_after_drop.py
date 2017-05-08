from contextlib import suppress
from queue import Empty

from common.log_helper import jqd
from data_server.day_data_manager import update_etf
from stock_basic.stock_helper import etf_t1, etf_t0
from trade.comm_message import CommMessage
from trade.trade_constant import *


def thread_buy_after_drop(**param):
    obj = BuyAfterDrop(param)
    obj.loop()


class BuyAfterDrop:
    def __init__(self, param_dict):
        self.realtime_stock_info = None
        self.drop_days = param_dict[ks_drop_days]
        self.trade_loop_queue = param_dict[ks_id_trade_loop]
        self.data_server_queue = param_dict[ks_id_data_server]
        self.name = param_dict[ks_model_name]
        self.self_queue = param_dict[self.name]
        self.etf_day_data = None

        self.prepare()
        self.loop()

    def prepare(self):
        self.etf_day_data = update_etf()

    def loop(self):
        self.data_server_queue.put(
            CommMessage(self.name, ks_msg_set_monitor_stock,
                        [*etf_t1, *etf_t0]))

        while True:
            with suppress(Empty):
                msg = self.self_queue.get()
                self.dispatch_msg(msg)

    def on_realtime_stock_info(self, sender, param):
        self.realtime_stock_info = param

    def dispatch_msg(self, commmsg: CommMessage):
        jqd(f'BuyAfterDrop: Receive Message: {commmsg}')
        sender = commmsg.sender
        func = self.find_operation(commmsg.operation)
        param = commmsg.param
        func(sender, param)

    def find_operation(self, operation_name):
        operdict = {ks_msg_push_monitor_stocks: self.on_realtime_stock_info}
        return operdict[operation_name]


def main():
    pass


if __name__ == '__main__':
    main()
