import datetime
import queue

import pandas

from common.helper import dt_now_time
from common_stock.stock_data_constants import etf_with_amount
from data_manager.stock_querier import sina_api
from project_helper.logbook_logger import mylog
from trading.base_structure.trade_constants import TradeId, trade_bid_end_time, trade_end_time, \
    MsgPushStocks, MsgAddPushStocks, MsgBidOver, MsgQuitLoop
from trading.base_structure.trade_message import TradeMessage
from trading.trade_context import TradeContext


# noinspection PyUnusedLocal
class DataServer:
    def __init__(self, trade_context: TradeContext, push_time_interval=None):
        self.trade_context = trade_context
        self.trade_context.thread_local.name = TradeId.data_server

        self.tls = self.trade_context.thread_local
        self.self_queue = self.trade_context.current_thread_queue  # type:queue.Queue

        self.push_time_interval = push_time_interval

        self._monitored_stock_map = {}
        self._df_realtime_stock_info = None  # type: pandas.DataFrame

        self._msg_sent = {MsgBidOver: None}

    def run_loop(self):
        mylog.info('Data server running .......')
        while 1:
            try:
                # Handle all message first
                while 1:
                    msg = self.self_queue.get(timeout=self.push_time_interval.total_seconds())
                    mylog.info(f'ReceiveMessage: {msg}')
                    if isinstance(msg.operation, MsgQuitLoop):
                        return
                    self.dispatch_msg(msg)

            except queue.Empty:
                self.push_all()

    def push_all(self):
        mylog.info('Try push ...')
        if dt_now_time() < trade_bid_end_time or dt_now_time() > trade_end_time:
            return

        bid_over_result = self._is_bid_over()
        if not bid_over_result.has_bid_over:
            return

        monitored_stock_info_dict = self.query_monitored_stock_info()
        for sender, df in monitored_stock_info_dict.items():
            if bid_over_result.first_bid_over:
                self.trade_context.post_msg(sender, MsgBidOver(df))
            else:
                self.trade_context.post_msg(sender, MsgPushStocks(df))

    def on_add_push_stock(self, msg: TradeMessage):
        assert isinstance(msg.operation, MsgAddPushStocks)
        self._monitored_stock_map[msg.sender] = msg.operation.stock_list

    def update_realtime_stock_info(self):
        stock_list = []
        for k, v in self._monitored_stock_map.items():
            stock_list.extend(v)

        if not stock_list:
            return None
        self._df_realtime_stock_info = sina_api.get_realtime_stock_info(stock_list)
        return self._df_realtime_stock_info

    def _is_bid_over(self):
        class BidResult:
            def __init__(self, has_bid_over, first_bid_over):
                self.has_bid_over = has_bid_over
                self.first_bid_over = first_bid_over

        if datetime.date.today() == self._msg_sent[MsgBidOver]:
            return BidResult(True, False)
        dfs = sina_api.get_realtime_stock_info(etf_with_amount)
        open_prices = dfs.open
        is_bid_over = all(open_prices)

        if is_bid_over:
            self._msg_sent[MsgBidOver] = datetime.date.today()
            return BidResult(True, True)
        else:
            return BidResult(False, False)

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
        if isinstance(msg.operation, MsgAddPushStocks):
            msg.try_put_result(self.on_add_push_stock(msg))
        else:
            mylog.error(f'Can not dispatch msg {msg}')


def main():
    pass


if __name__ == '__main__':
    main()
