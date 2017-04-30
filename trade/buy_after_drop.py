from contextlib import suppress
from queue import Empty

from common.helper import sleep_ms
from common.log_helper import MyLog
from trade.trade_constant import k_id_data_server, k_id_trade_loop

mylog3 = MyLog(filename='buy_after_drop.log')


# mylog3 = logging.getLogger('3')
# mylog3.addHandler(logging.FileHandler('3.log', 'w', 'utf-8'))

# def jqd(*args):
#     errstr = ' '.join(str(v) for v in args)
#     mylog.log_with_level(mylog.debug, errstr, outputfilepos=False)


def buy_after_drop_loop_for_etfs(**param):
    obj = BuyAfterDrop(param)
    obj.loop()


class BuyAfterDrop:
    def __init__(self, param_dict):
        self.drop_days = param_dict['drop_days']
        self.trade_loop_queue = param_dict[k_id_trade_loop]
        self.data_server_queue = param_dict[k_id_data_server]
        self.self_queue = param_dict[buy_after_drop_loop_for_etfs.__name__]

    def loop(self):
        mylog3.debug('trade loop')
        # jqd('Model run loop')
        self.trade_loop_queue.put('Model -> TradeLoop')
        self.data_server_queue.put('Model -> DataServer')
        while True:
            with suppress(Empty):
                val = self.self_queue.get()
                #jqd(f'In Model:{val}')
                sleep_ms(1000)


def main():
    pass


if __name__ == '__main__':
    main()
