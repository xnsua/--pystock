import queue
from collections import namedtuple

import pandas

from common.datetime_manager import DateTimeManager
from common.helper import to_log_str
from common.log_helper import mylog, jqd
from data_server.stock_querier import sina_api
from stock_basic.stock_helper import etf_with_amount
from trading.comm_message import CommMessage
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_, ksti_


# def thread_data_server_loop(trade_context, **kwargs):
#     try:
#         data_server = DataServer(trade_context, kwargs)
#         trade_context.thread_local.name = ktc_.id_data_server
#         data_server.run_loop()
#     except Exception:
#         mylog.exception()
#         alert_exception(10)


# noinspection PyUnusedLocal
class DataServer:
    def __init__(self, trade_context: TradeContext, push_time_interval=None):
        self.trade_context = trade_context

        self.tls = self.trade_context.thread_local
        self.dtm = self.trade_context.dtm  # type: DateTimeManager
        self.self_queue = self.trade_context.get_current_thread_queue()  # type:queue.Queue

        self.push_time_interval = push_time_interval

        self._monitored_stock_map = {}
        self._df_realtime_stock_info = None  # type: pandas.DataFrame

        self.msg_sent = {ktc_.msg_before_trading: None,
                         ktc_.msg_after_trading: None,
                         ktc_.msg_bid_over: None}

        self._quit = False

        self._msg_function_dict = {ktc_.msg_set_monitored_stock: self.add_monitored_stock,
                                   ktc_.msg_quit_loop: self.quit_loop}

    def init_thread_param(self):
        self.tls.name = ktc_.id_data_server

    def __call__(self, *args, **kwargs):
        self.trade_context.thread_local.name = ktc_.id_data_server
        self.run_loop()

    def add_monitored_stock(self, sender, param, msg_dt):
        self._monitored_stock_map[sender] = param

    # noinspection PyUnusedLocal
    def quit_loop(self, sender, param, msg_dt):
        self._quit = True
        jqd('self.quit\n', self._quit, self.dtm.now())

    def update_realtime_stock_info(self):
        stock_list = []
        for k, v in self._monitored_stock_map.items():
            stock_list.extend(v)

        if not stock_list:
            return None
        self._df_realtime_stock_info = sina_api.get_realtime_stock_info(stock_list)
        return self._df_realtime_stock_info

    def run_loop(self):
        self.init_thread_param()

        mylog.info('Running data server loop')
        self.dtm.set_timer()
        while 1:
            try:
                # Handle all message first
                while 1:
                    real_timeout = self.push_time_interval.total_seconds() / self.dtm.speed
                    msg = self.self_queue.get(timeout=real_timeout)
                    self.dispatch_msg(msg)

            except queue.Empty:
                if self._quit:
                    break
                self.push_all()

    def _is_bid_over(self):
        nt_result = namedtuple('bid_over_result', ['is_bid_over', 'first_bid_over'])
        if self.dtm.today() == self.msg_sent[ktc_.msg_bid_over]:
            return nt_result(True, False)
        dfs = sina_api.get_realtime_stock_info(etf_with_amount)
        open_prices = dfs.open
        is_bid_over = all(open_prices)

        if is_bid_over:
            self.msg_sent[ktc_.msg_bid_over] = self.dtm.today()

        return nt_result(is_bid_over, True)

    def push_all(self):

        if self.dtm.time() < ksti_.bid_over_time[0]:
            return

        bid_over_result = self._is_bid_over()
        if not bid_over_result.is_bid_over:
            return

        monitored_stock_info_dict = self.query_monitored_stock_info()
        for sender, df in monitored_stock_info_dict.items():
            if bid_over_result.first_bid_over:
                self.trade_context.post_msg(sender, ktc_.msg_bid_over, df)
            else:
                self.trade_context.push_realtime_info(sender, df)

    def query_monitored_stock_info(self):
        realtime_stock_info_dict = {}
        df_stock_info = self.update_realtime_stock_info()
        for sender, list_stock in self._monitored_stock_map.items():
            df = df_stock_info[df_stock_info.index.isin(list_stock)]
            if len(df.index) == len(list_stock):
                realtime_stock_info_dict[sender] = df
                # self.trade_context.push_realtime_info(sender, df)
            else:
                mylog.warn(f'Cannot find push data for sender {sender}')

        return realtime_stock_info_dict

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
        param = msg.param1
        msg_dt = msg.msg_dt
        try:
            func = self.find_func_by_operation(operation)
            rval = func(sender, param, msg_dt)
            msg.put_result(rval)
        except Exception as e:
            msg.put_result((Exception.__name__, e))
            mylog.error(to_log_str(e))

    def find_func_by_operation(self, operation):
        return self._msg_function_dict[operation]


def main():
    pass


if __name__ == '__main__':
    main()
