from contextlib import suppress
from queue import Empty

from common.helper import sleep_ms
from stock_basic.stock_helper import etf_t1, etf_t0
from trade.comm_message import CommMessage
from trade.trade_constant import *


def buy_after_drop_loop_for_etfs(**param):
    obj = BuyAfterDrop(param)
    obj.loop()


class BuyAfterDrop:
    def __init__(self, param_dict):
        self.drop_days = param_dict['drop_days']
        self.trade_loop_queue = param_dict[k_id_trade_loop]
        self.data_server_queue = param_dict[k_id_data_server]
        self.name = k_idm_buy_after_drop
        self.self_queue = param_dict[self.name]

    def loop(self):
        # toch
        # etf_data = query_etfs()
        self.data_server_queue.put(
            CommMessage(self.name, k_msg_set_monitor_stock,
                        [*etf_t1, *etf_t0]))

        while True:
            with suppress(Empty):
                msg = self.self_queue.get()
                self.dispatch_msg(msg)
                sleep_ms(1000)

    def on_push_stock_info(self, sender, param):
        print('On push stock info: ', type(param))

    def dispatch_msg(self, commmsg: CommMessage):
        sender = commmsg.sender
        func = self.find_operation(commmsg.operation)
        param = commmsg.param
        func(sender, param)

    def find_operation(self, operation_name):
        operdict = {k_msg_push_monitor_stocks: self.on_push_stock_info}
        return operdict[operation_name]


def main():
    pass


if __name__ == '__main__':
    main()
