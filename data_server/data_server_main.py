import queue

import pandas as pd

from common.datetime_manager import DateTimeManager
from common.helper import to_log_str
from common.log_helper import mylog, jqd
from data_server.stock_querier.sina_api import get_realtime_stock_info
from trading.comm_message import CommMessage
from trading.trade_context import TradeContext
from trading.trade_helper import *
from trading.trade_utility import is_in_expanded_stage

_tcc = TradeCommunicationConstant
_stc = StockTimeConstant


def thread_data_server_loop(trade_context, **kwargs):
    try:
        data_server = DataServer(trade_context, kwargs)
        trade_context.thread_local.name = _tcc.id_data_server
        data_server.run_loop()
    except Exception as e:
        mylog.fatal(to_log_str(e))
        alert_exception(10)


# noinspection PyUnusedLocal
class DataServer:
    def __init__(self, trade_context: TradeContext, param_dict):
        self.trade_context = trade_context
        self.trade_context.thread_local.name = _tcc.id_data_server
        self.dtm = self.trade_context.dtm  # type: DateTimeManager
        self.self_queue = self.trade_context.get_current_thread_queue()  # type:queue.Queue

        self.param_dict = param_dict

        self.monitored_stock_map = {}
        self.df_realtime_stock_info = None  # type: pd.DataFrame

        self.msg_function_dict = {_tcc.msg_set_monitored_stock: self.add_monitored_stock,
                                  _tcc.msg_quit_loop: self.quit_loop}

        self.quit = False

    def add_monitored_stock(self, sender, param, msg_dt):
        self.monitored_stock_map[sender] = param

    # noinspection PyUnusedLocal
    def quit_loop(self, sender, param, msg_dt):
        self.quit = True
        jqd('self.quit\n', self.quit, self.dtm.now())

    def update_realtime_stock_info(self):
        stock_list = []
        for k, v in self.monitored_stock_map.items():
            stock_list.extend(v)

        if not stock_list:
            return None
        self.df_realtime_stock_info = get_realtime_stock_info(stock_list)
        return self.df_realtime_stock_info

    def run_loop(self):
        mylog.info('Running data server loop')
        interval = self.param_dict[_tcc.push_realtime_interval]
        self.dtm.set_timer()
        while 1:
            try:
                # Handle all message first
                while 1:
                    real_timeout = interval.total_seconds() / self.dtm.speed
                    msg = self.self_queue.get(timeout=real_timeout)
                    self.dispatch_msg(msg)

            except queue.Empty:
                if self.quit:
                    break
                self.push_realtime_stock_info()

    def in_expand_trade_time(self):
        td1 = self.param_dict[_tcc.trade1_timedelta]
        td2 = self.param_dict[_tcc.trade2_timedelta]
        in_stage1 = is_in_expanded_stage(self.dtm.time(), _stc.trade1, *td1)
        in_stage2 = is_in_expanded_stage(self.dtm.time(), _stc.trade2, *td2)
        if not in_stage1 and not in_stage2:
            return False
        return True

    def push_realtime_stock_info(self):
        # jqd('PPP begin', self.dtm.now())
        if self.in_expand_trade_time() and self.monitored_stock_map:
            df_stock_info = self.update_realtime_stock_info()
            for sender, list_stock in self.monitored_stock_map.items():
                df = df_stock_info[df_stock_info.index.isin(list_stock)]
                if len(df.index) == len(list_stock):
                    self.trade_context.push_realtime_info(sender, df)
                else:
                    mylog.warn('Cannot find push data')
                    # jqd('PPP End', self.dtm.now())
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
        msg_dt = msg.msg_dt
        try:
            func = self.find_func_by_operation(operation)
            rval = func(sender, param, msg_dt)
            msg.put_result(rval)
        except Exception as e:
            msg.put_result((Exception.__name__, e))
            mylog.error(to_log_str(e))

    def find_func_by_operation(self, operation):
        return self.msg_function_dict[operation]


def main():
    pass


if __name__ == '__main__':
    main()
