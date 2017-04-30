import multiprocessing

from common.helper import sleep_ms
from common.log_helper import jqd
from data_server.data_server_constant import k_id_trade_loop, k_id_data_server
from data_server.data_server_main import data_server_loop
from trade.buy_after_drop import buy_after_drop_loop_for_etfs


class TradeLoop:
    def __init__(self):
        self.out_queues = []
        self.self_queue = multiprocessing.Queue()
        self.data_server_queue = multiprocessing.Queue()

        self.queue_dict = {k_id_trade_loop: self.self_queue,
                           k_id_data_server: self.data_server_queue}
        self.model_queue_dict = {}
        self.trade_models = [(buy_after_drop_loop_for_etfs, {'drop_days': 2})]

    def add_model(self, model):
        self.trade_models.append(model)

    def prepare(self):
        process_queue = []
        # Create data server process
        for v in self.trade_models:
            new_queue = multiprocessing.Queue()
            self.model_queue_dict.update({v[0].__name__: new_queue})
            process = multiprocessing.Process(
                target=v[0],
                kwargs={**v[1], **self.queue_dict, v[0].__name__: new_queue})
            process_queue.append(process)

        data_server_process = multiprocessing.Process(
            target=data_server_loop,
            kwargs={**self.queue_dict, **self.model_queue_dict})
        data_server_process.start()

        for v in process_queue:
            v.start()

    def process_loop(self):
        jqd('Trade loop')
        for key, val in self.model_queue_dict.items():
            val.put('Trade Loop -> Model')
        self.data_server_queue.put('Trade Loop -> Data server')

        while 1:
            val = self.self_queue.get()
            sleep_ms(1000)
            jqd(f'In Trade Loop: {val}')


def begin_trade():
    tradeloop = TradeLoop()
    tradeloop.add_model((buy_after_drop_loop_for_etfs, {'drop_days': 2}))
    tradeloop.prepare()
    tradeloop.process_loop()


def main():
    begin_trade()
    pass


if __name__ == '__main__':
    main()
