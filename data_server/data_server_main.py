import multiprocessing
import queue
import random
from contextlib import suppress

from common.helper import LogicException, exception_to_logstr, sleep_ms, \
    seconds_from_epoch
from common.log_helper import mylog
from data_server.etf_updater import update_etf
from data_server.stock_querier.sina_api import get_realtime_stock_info
from stock_basic.stock_helper import is_trade_day
from trade.comm_message import CommMessage
from trade.trade_constant import k_id_data_server, k_msg_set_monitor_stock, \
    k_msg_push_monitor_stocks


def data_server_loop(**queue_dict):
    data_server = DataServer(queue_dict)
    data_server.run_loop()


def query_etfs():
    etfs = update_etf()
    return etfs


class DataServer:
    def __init__(self, queue_dict):
        self.self_queue = queue_dict[
            k_id_data_server]  # type: multiprocessing.Queue
        self.queue_dict = queue_dict
        self.real_time_stocks_dict = {}

    def do_day_work(self):
        if not is_trade_day():
            return

    def add_real_time_stock(self, sender, stocklist):
        self.real_time_stocks_dict[sender] = stocklist

    def get_realtime_stock_info(self):
        stocklist = []
        for k, v in self.real_time_stocks_dict.items():
            stocklist.extend(v)

        if not stocklist:
            return None
        df_stockinfo = get_realtime_stock_info(stocklist)
        return df_stockinfo

    def run_loop(self):
        while 1:
            seconds = seconds_from_epoch()
            self.handle_msg()
            self.push_real_time_info()
            ms = random.randint(300, 600)
            # random sleep for message.
            sleepseconds = ms - (seconds_from_epoch() - seconds) * 1000
            sleep_ms(sleepseconds if sleepseconds > 0 else 0)

    def push_real_time_info(self):
        if self.real_time_stocks_dict:
            dfstockinfo = self.get_realtime_stock_info()
            for sender, liststock in self.real_time_stocks_dict.items():
                df = dfstockinfo[dfstockinfo.index.isin(liststock)]
                if len(df.index) == len(liststock):
                    respqueue = self.find_queue_by_sender(sender)
                    respqueue.put(CommMessage(k_id_data_server,
                                              k_msg_push_monitor_stocks, df))
                else:
                    mylog.warn('Cannot find push data')

    def handle_msg(self):
        with suppress(queue.Empty):
            msg = self.self_queue.get(block=False)
            self.dispatch_msg(msg)

    def dispatch_msg(self, msg: CommMessage):
        sender = msg.sender
        operation = msg.operation
        param = msg.param
        out_queue = self.find_queue_by_sender(sender)
        try:
            func = self.find_func_by_operation(operation)
            func(sender, param)
        except Exception as e:
            out_queue.put((k_id_data_server, (Exception.__name__, e)))
            mylog.error(exception_to_logstr(e))

    def find_queue_by_sender(self, sender):
        try:
            return self.queue_dict[sender]
        except:
            raise LogicException(f'Can not find out queue of sender {sender}')

    def find_func_by_operation(self, operation):
        funcmap = {k_msg_set_monitor_stock: self.add_real_time_stock}
        return funcmap[operation]


def main():
    # ds = DataServer(myconfig.stock_data_path / 'day/data_server', None)
    # print(DataServer.__dict__['query_etfs']())
    # print(globals())
    # dayhistorys = ds.query_day_history(['000908', '000877'exbb''], ndays_ago(6))
    pass


if __name__ == '__main__':
    main()
