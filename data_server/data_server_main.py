import datetime as dt
import multiprocessing
import queue
import sys

import pandas as pd

from common.helper import LogicException, to_logstr
from common.log_helper import mylog
from data_server.stock_querier.sina_api import get_realtime_stock_info
from trade.comm_message import CommMessage
from trade.datetime_manager import DateTimeManager
from trade.trade_constant import *
from trade.trade_utility import is_in_expanded_stage

_tcc = TradeCommicationConstant
_stc = StockTimeConstant


def thread_data_server_loop(**param_dict):
    trade_manager_queue = param_dict[_tcc.id_trade_manager]
    try:
        data_server = DataServer(param_dict)
        data_server.run_loop()
    except Exception as e:
        mylog.warn(to_logstr(e))
        trade_manager_queue.put(
            CommMessage(_tcc.id_data_server, _tcc.msg_exception_occur, e))
        pass


class DataServer:
    def __init__(self, param_dict):
        self.self_queue = param_dict[
            _tcc.id_data_server]  # type: multiprocessing.Queue
        self.trade_manager_queue = param_dict[
            _tcc.id_trade_manager]  # type: multiprocessing.Queue
        self.dtm = param_dict[_tcc.datetime_manager]  # type: DateTimeManager
        self.model_queue_dict = param_dict[_tcc.model_queue_dict]

        self.monitored_stock_map = {}
        self.df_readtime_stock_info = None  # type: pd.DataFrame
        self.push_interval_time = param_dict.get(_tcc.push_realtime_interval, 1)
        self.quit = False

    def add_monitered_stock(self, sender, stocklist):
        self.monitored_stock_map[sender] = stocklist

    def update_realtime_stock_info(self):
        stocklist = []
        for k, v in self.monitored_stock_map.items():
            stocklist.extend(v)

        if not stocklist:
            return None
        self.df_readtime_stock_info = get_realtime_stock_info(stocklist)
        return self.df_readtime_stock_info

    def run_loop(self):
        mylog.info('Running data server loop')

        start_time = self.dtm.now()
        for count in range(sys.maxsize):
            if not self.quit:
                if self.handle_msg():
                    continue
                self.push_realtime_stock_info()

                elapse_seconds = (self.dtm.now() - start_time).total_seconds()
                if elapse_seconds < count:
                    self.dtm.sleep(count - elapse_seconds)
            else:
                break

    def in_expand_trade_time(self):
        td1 = dt.timedelta(seconds=60)  # Test use this value
        td2 = dt.timedelta(seconds=30)  # Test use this value
        if not is_in_expanded_stage(self.dtm.time(), _stc.trade1, td1) \
                and not is_in_expanded_stage(self.dtm.time(), _stc.trade2, td2):
            return False
        return True

    def push_realtime_stock_info(self):
        if self.in_expand_trade_time() and self.monitored_stock_map:
            dfstockinfo = self.update_realtime_stock_info()
            for sender, liststock in self.monitored_stock_map.items():
                df = dfstockinfo[dfstockinfo.index.isin(liststock)]
                if len(df.index) == len(liststock):
                    respqueue = self.find_queue_by_sender(sender)
                    respqueue.put(CommMessage(_tcc.id_data_server,
                                              _tcc.msg_push_realtime_stocks, df))
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
        if msg.operation == _tcc.msg_quit_loop:
            self.quit = True
            return
        sender = msg.sender
        operation = msg.operation
        param = msg.param
        out_queue = self.find_queue_by_sender(sender)
        try:
            func = self.find_func_by_operation(operation)
            func(sender, param)
        except Exception as e:
            out_queue.put((_tcc.id_data_server, (Exception.__name__, e)))
            mylog.error(to_logstr(e))

    def find_queue_by_sender(self, sender):
        if sender == _tcc.id_trade_manager:
            return self.trade_manager_queue
        try:
            return self.model_queue_dict[sender]
        except:
            raise LogicException(f'Can not find out queue of sender {sender}')

    def find_func_by_operation(self, operation):
        funcmap = {_tcc.msg_set_monitor_stock: self.add_monitered_stock}
        return funcmap[operation]


def main():
    pass


if __name__ == '__main__':
    main()
