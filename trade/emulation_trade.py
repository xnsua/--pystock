import queue
import threading

import pandas as pd

from common.helper import sleep_ms
from data_server.data_server_main import data_server_loop
from trade.buy_after_drop import buy_after_drop_loop_for_etfs
from trade.trade_constant import *

pd.options.display.max_rows = 10


class TradeLoop:
    def __init__(self):
        self.out_queues = []
        self.self_queue = queue.Queue()
        self.data_server_queue = queue.Queue()

        self.queue_dict = {k_id_trade_loop: self.self_queue,
                           k_id_data_server: self.data_server_queue}
        self.model_queue_dict = {}
        self.trade_models = []
        self.threads = []

    def add_model(self, model):
        self.trade_models.append(model)

    def prepare(self):
        for v in self.trade_models:
            target, model_name, param_dict = v
            new_queue = queue.Queue()
            self.model_queue_dict.update({model_name: new_queue})

        data_server_thread = threading.Thread(
            target=data_server_loop,
            kwargs={**self.queue_dict, **self.model_queue_dict})
        data_server_thread.start()

        for v in self.trade_models:
            target, model_name, param_dict = v
            thread = threading.Thread(target=target,
                                      kwargs={**self.queue_dict,
                                              model_name: self.model_queue_dict[
                                                  model_name],
                                              **param_dict})
            self.threads.append(thread)
            thread.start()

    def process_loop(self):
        self.prepare()
        while 1:
            val = self.self_queue.get()
            sleep_ms(1000)


def begin_trade():
    tradeloop = TradeLoop()
    tradeloop.add_model(
        (buy_after_drop_loop_for_etfs, k_idm_buy_after_drop, {k_drop_days: 2}))
    tradeloop.process_loop()


def main():
    begin_trade()
    pass


if __name__ == '__main__':
    main()
