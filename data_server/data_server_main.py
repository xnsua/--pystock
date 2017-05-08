import multiprocessing
import queue

import pandas as pd

from common.helper import LogicException, exception_to_logstr, \
    seconds_from_epoch, dttime, sleep_for_seconds
from common.log_helper import mylog
from data_server.etf_updater import update_etf
from data_server.stock_querier.sina_api import get_realtime_stock_info
from stock_basic.stock_helper import is_trade_day
from trade.comm_message import CommMessage
from trade.trade_constant import ks_id_data_server, ks_msg_set_monitor_stock, \
    ks_msg_push_monitor_stocks, find_stage, \
    ks_before_bid, ks_bid_stage1, ks_bid_stage2, ks_bid_over, ks_trade1, \
    ks_midnoon_break, ks_trade2, ks_after_trade, ks_model_queue_dict, \
    ks_stage_entered


def thread_data_server_loop(**queue_dict):
    data_server = DataServer(queue_dict)
    data_server.run_loop()


def query_etfs():
    etfs = update_etf()
    return etfs


class DataServer:
    def __init__(self, queue_dict):
        self.self_queue = queue_dict[
            ks_id_data_server]  # type: multiprocessing.Queue
        self.model_queue_dict = queue_dict[ks_model_queue_dict]

        self.monitored_stocks_map = {}
        self.stage = None
        self.stage_func_map = {
            ks_before_bid: self.handle_before_bid,
            ks_bid_stage1: self.handle_bid_stage1,
            ks_bid_stage2: self.handle_bid_stage2,
            ks_bid_over: self.handle_bid_over,
            ks_trade1: self.handle_trade1,
            ks_midnoon_break: self.handle_midnoon_break,
            ks_trade2: self.handle_trade2,
            ks_after_trade: self.handle_after_trade,
        }
        self.calc_stage()
        self.sent_message = set()  # Store Message send only one time
        self.df_readtime_stock_info = None  # type: pd.DataFrame

    # <editor-fold desc="Handle functions">
    def handle_before_bid(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_before_bid))

    def handle_bid_stage1(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_bid_stage1))

    def handle_bid_stage2(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_bid_stage2))

    def handle_bid_over(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_bid_over))
        self.push_realtime_stock_info()

    def handle_trade1(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_trade1))
        self.push_realtime_stock_info()

    def handle_midnoon_break(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_midnoon_break))

    def handle_trade2(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_trade2))
        self.push_realtime_stock_info()

    def handle_after_trade(self):
        self.send_model_msg_once(
            CommMessage(ks_id_data_server, ks_stage_entered, ks_after_trade))

    def send_model_msg(self, commmsg):
        for k, v in self.model_queue_dict.items():
            v.put(commmsg)

    def send_model_msg_once(self, commmsg):
        if commmsg not in self.sent_message:
            for k, v in self.model_queue_dict.items():
                self.sent_message.add(commmsg)
                v.put(commmsg)

    # </editor-fold>

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
            begintime = seconds_from_epoch()

            if self.handle_msg():
                continue

            if self.handle_stage():
                continue

            sleep_duration = 1 - (seconds_from_epoch() - begintime)
            mylog.warn_if(sleep_duration < 0)
            if sleep_duration > 0:
                sleep_for_seconds(sleep_duration)

    def handle_stage(self):
        assert is_trade_day()
        func = self.stage_func_map[find_stage(dttime())]
        return func()

    def push_realtime_stock_info(self):
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
