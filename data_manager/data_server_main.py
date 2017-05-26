import datetime
import queue
from collections import namedtuple

import pandas

from data_manager.stock_querier import sina_api
from project_helper.phelper import mylog, jqd
from stock_utility.stock_data_constants import etf_with_amount
from trading.base_structure.trade_constants import ktc_, trade_bid_end_time, trade_end_time
from trading.base_structure.trade_message import TradeMessage
from trading.trade_context import TradeContext


# def thread_data_server_loop(trade_context, **kwargs):
#     try:
#         data_manager = DataServer(trade_context, kwargs)
#         trade_context.thread_local.name = ktc_.id_data_server
#         data_manager.run_loop()
#     except Exception:
#         mylog.exception()
#         alert_exception(10)


# noinspection PyUnusedLocal
class DataServer:
    def __init__(self, trade_context: TradeContext, push_time_interval=None):
        self.trade_context = trade_context
        self.trade_context.thread_local.name = ktc_.id_data_server

        self.tls = self.trade_context.thread_local
        self.self_queue = self.trade_context.get_current_thread_queue()  # type:queue.Queue

        self.push_time_interval = push_time_interval

        self._monitored_stock_map = {}
        self._df_realtime_stock_info = None  # type: pandas.DataFrame

        self._msg_sent = {ktc_.msg_before_trading: None,
                          ktc_.msg_after_trading: None,
                          ktc_.msg_bid_over: None}

    def run_loop(self):
        self.log('Running data server loop')
        while 1:
            try:
                # Handle all message first
                while 1:
                    msg = self.self_queue.get(timeout=self.push_time_interval.total_seconds())
                    self.log(f'ReceiveMessage: {msg}')
                    if msg.operation == ktc_.msg_quit_loop:
                        return
                    self.dispatch_msg(msg)

            except queue.Empty:
                self.push_all()

    def push_all(self):
        self.log('Try push')
        if datetime.datetime.now().time() < trade_bid_end_time + datetime.timedelta(seconds=10) \
                or datetime.datetime.now().time() > trade_end_time:
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

    def log(self, msg):
        jqd(f'{self.trade_context.thread_local.name}:: {msg}')

    def on_add_monitored_stock(self, msg: TradeMessage):
        self._monitored_stock_map[msg.sender] = msg.param1

    def update_realtime_stock_info(self):
        stock_list = []
        for k, v in self._monitored_stock_map.items():
            stock_list.extend(v)

        if not stock_list:
            return None
        self._df_realtime_stock_info = sina_api.get_realtime_stock_info(stock_list)
        return self._df_realtime_stock_info

    def _is_bid_over(self):
        nt_result = namedtuple('bid_over_result', ['is_bid_over', 'first_bid_over'])
        if datetime.date.today() == self._msg_sent[ktc_.msg_bid_over]:
            return nt_result(True, False)
        dfs = sina_api.get_realtime_stock_info(etf_with_amount)
        open_prices = dfs.open
        is_bid_over = all(open_prices)

        if is_bid_over:
            self._msg_sent[ktc_.msg_bid_over] = datetime.date.today()

        return nt_result(is_bid_over, True)

    def query_monitored_stock_info(self):
        realtime_stock_info_dict = {}
        df_stock_info = self.update_realtime_stock_info()
        for sender, list_stock in self._monitored_stock_map.items():
            df = df_stock_info[df_stock_info.index.isin(list_stock)]
            if len(df.index) == len(list_stock):
                realtime_stock_info_dict[sender] = df
            else:
                mylog.warn(f'Cannot find push data for Model: {sender}')

        return realtime_stock_info_dict

    def handle_msg(self):
        try:
            msg = self.self_queue.get(block=False)
            self.dispatch_msg(msg)
            return True
        except queue.Empty:
            return False

    def dispatch_msg(self, msg: TradeMessage):
        if msg.operation == ktc_.msg_set_monitored_stock:
            msg.try_put_result(self.on_add_monitored_stock(msg))
        else:
            mylog.error(f'Can not dispatch msg {msg}')


def main():
    pass


if __name__ == '__main__':
    main()
