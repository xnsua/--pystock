import datetime as dt
import queue
import sys

import pandas as pd

from common.helper import LogicException, to_logstr
from common.log_helper import mylog
from data_server.stock_querier.sina_api import get_realtime_stock_info
from trade.comm_message import CommMessage
from trade.trade_constant import *
from trade.trade_context import TradeContext
from trade.trade_utility import is_in_expanded_stage

_tcc = TradeCommicationConstant
_stc = StockTimeConstant


def thread_data_server_loop(trade_context, **kwargs):
    try:
        data_server = DataServer(trade_context, kwargs)
        trade_context.thread_local.name = _tcc.id_data_server
        data_server.run_loop()
    except Exception as e:
        mylog.fatal(to_logstr(e))


class DataServer:
    def __init__(self, trade_context: TradeContext, param_dict):
        self.trade_context = trade_context
        self.trade_context.thread_local.name = _tcc.id_data_server
        self.dtm = self.trade_context.dtm
        self.self_queue = self.trade_context.get_thread_queue()

        self.push_interval_time = param_dict.get(_tcc.push_realtime_interval, 1)

        self.monitored_stock_map = {}
        self.df_readtime_stock_info = None  # type: pd.DataFrame

        self.msg_function_dict = {_tcc.msg_set_monitored_stock: self.add_monitered_stock,
                                  _tcc.msg_quit_loop: self.quit_loop}

        self.quit = False

    def add_monitered_stock(self, sender, param):
        self.monitored_stock_map[sender] = param

    # noinspection PyUnusedLocal
    def quit_loop(self, sender, param):
        self.quit = True

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
        in_stage1 = is_in_expanded_stage(self.dtm.time(), _stc.trade1, td1)
        in_stage2 = is_in_expanded_stage(self.dtm.time(), _stc.trade2, td2)
        if not in_stage1 and not in_stage2:
            return False
        return True

    def push_realtime_stock_info(self):
        if self.in_expand_trade_time() and self.monitored_stock_map:
            dfstockinfo = self.update_realtime_stock_info()
            for sender, liststock in self.monitored_stock_map.items():
                df = dfstockinfo[dfstockinfo.index.isin(liststock)]
                if len(df.index) == len(liststock):
                    self.trade_context.push_realtime_info(sender, df)
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
        try:
            func = self.find_func_by_operation(operation)
            rval = func(sender, param)
            msg.put_result(rval)
        except Exception as e:
            msg.put_result((Exception.__name__, e))
            mylog.error(to_logstr(e))

    def find_queue_by_sender(self, sender):
        if sender == _tcc.id_trade_manager:
            return self.trade_manager_queue
        try:
            return self.model_queue_dict[sender]
        except:
            raise LogicException(f'Can not find out queue of sender {sender}')

    def find_func_by_operation(self, operation):
        return self.msg_function_dict[operation]


def main():
    pass


if __name__ == '__main__':
    main()
