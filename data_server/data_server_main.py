import multiprocessing
import queue

import pandas as pd

from common.helper import LogicException, exception_to_logstr, \
    sleep_for_seconds
from common.log_helper import mylog
from data_server.day_data_manager import update_etf
from data_server.stock_querier.sina_api import get_realtime_stock_info
from trade.comm_message import CommMessage
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import ks_id_data_server, ks_msg_set_monitor_stock, \
    ks_msg_push_monitor_stocks, ks_trade1, \
    ks_trade2, ks_model_queue_dict, \
    ks_datetime_manager, is_in_expanded_stage


# from trade.datetime_manager import DateTiddmeManager


def thread_data_server_loop(**param_dict):
    data_server = DataServer(param_dict)
    data_server.run_loop()


def query_etfs(date):
    etfs = update_etf()
    return etfs


class DataServer:
    def __init__(self, param_dict):
        self.self_queue = param_dict[ks_id_data_server]  # type: multiprocessing.Queue
        self.dtm = param_dict[ks_datetime_manager]  # type: DateTimeManager
        self.model_queue_dict = param_dict[ks_model_queue_dict]

        self.monitored_stocks_map = {}
        self.df_readtime_stock_info = None  # type: pd.DataFrame

    def add_monitered_stock(self, sender, stocklist):
        self.monitored_stocks_map[sender] = stocklist

    def update_realtime_stock_info(self):
        stocklist = []
        for k, v in self.monitored_stocks_map.items():
            stocklist.extend(v)

        if not stocklist:
            return None
        self.df_readtime_stock_info = get_realtime_stock_info(stocklist)
        return self.df_readtime_stock_info

    def run_loop(self):
        while 1:
            self.dtm.set_timer()
            if self.handle_msg():
                continue

            self.push_realtime_stock_info()

            if self.dtm.elapse_seconds() < 1:
                sleep_for_seconds(1 - self.dtm.elapse_seconds())

    def push_realtime_stock_info(self):
        if not is_in_expanded_stage(self.dtm.now(), ks_trade1) \
                and not is_in_expanded_stage(self.dtm.now(), ks_trade2):
            return
        if self.monitored_stocks_map:
            dfstockinfo = self.update_realtime_stock_info()
            for sender, liststock in self.monitored_stocks_map.items():
                df = dfstockinfo[dfstockinfo.index.isin(liststock)]
                if len(df.index) == len(liststock):
                    respqueue = self.find_queue_by_sender(sender)
                    respqueue.put(CommMessage(ks_id_data_server,
                                              ks_msg_push_monitor_stocks, df))
                else:
                    mylog.warn('Cannot find push data')

    def handle_msg(self):
        try:
            msg = self.self_queue.get(block=False)
            self.dispatch_msg(msg)
            return True
        except queue.Empty:
            return False

    def dispatch_msg(self, msg: CommMessage):
        sender = msg.sender
        operation = msg.operation
        param = msg.param
        out_queue = self.find_queue_by_sender(sender)
        try:
            func = self.find_func_by_operation(operation)
            func(sender, param)
        except Exception as e:
            out_queue.put((ks_id_data_server, (Exception.__name__, e)))
            mylog.error(exception_to_logstr(e))

    def find_queue_by_sender(self, sender):
        try:
            return self.model_queue_dict[sender]
        except:
            raise LogicException(f'Can not find out queue of sender {sender}')

    def find_func_by_operation(self, operation):
        funcmap = {ks_msg_set_monitor_stock: self.add_monitered_stock}
        return funcmap[operation]


def main():
    # ds = DataServer(myconfig.stock_data_path / 'day/data_server', None)
    # print(DataServer.__dict__['query_etfs']())
    # print(globals())
    # dayhistorys = ds.query_day_history(['000908', '000877'exbb''], ndays_ago(6))
    pass


if __name__ == '__main__':
    main()
