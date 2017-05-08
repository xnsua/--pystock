from contextlib import suppress
from queue import Empty

import sortedcontainers

from common.helper import sleep_for_milliseconds, dttoday
from common.log_helper import jqd
from stock_basic.stock_helper import etf_t1, etf_t0
from trade.comm_message import CommMessage
from trade.trade_constant import *


def thread_buy_after_drop(**param):
    obj = BuyAfterDrop(param)
    obj.loop()


class BuyAfterDrop:
    def __init__(self, param_dict):
        self.realtime_stock_info = None
        self.drop_days = param_dict[ks_drop_days]
        self.trade_loop_queue = param_dict[ks_id_trade_loop]
        self.data_server_queue = param_dict[ks_id_data_server]
        self.name = param_dict[ks_model_name]
        self.self_queue = param_dict[self.name]

    def loop(self):
        # toch
        # etf_data = query_etfs()
        self.data_server_queue.put(
            CommMessage(self.name, ks_msg_set_monitor_stock,
                        [*etf_t1, *etf_t0]))

        while True:
            with suppress(Empty):
                msg = self.self_queue.get()
                self.dispatch_msg(msg)
                sleep_for_milliseconds(1000)

    def on_push_stock_info(self, sender, param):
        self.realtime_stock_info = param

    def dispatch_msg(self, commmsg: CommMessage):
        jqd(f'BuyAfterDrop: Receive Message: {commmsg}')
        sender = commmsg.sender
        func = self.find_operation(commmsg.operation)
        param = commmsg.param
        func(sender, param)

    def find_operation(self, operation_name):
        operdict = {ks_msg_push_monitor_stocks: self.on_push_stock_info}
        return operdict[operation_name]


class TimePoints:
    def __init__(self, time_points=None):
        self.time_points = sortedcontainers.SortedDict(time_points)
        self.time_points_used = {}
        pass

    def hit(self, vdatetime):
        vtime = vdatetime.time()
        index = self.time_points.bisect_right(vtime)
        index = index - 1
        if index >= 0:
            time_point = self.time_points.iloc[index]
            if vtime > time_point \
                    and self.time_points_used.get(time_point,
                                                  None) != dttoday():
                self.time_points_used[time_point] = dttoday()
                time_point_name = self.time_points[time_point]
                if not time_point_name:
                    return 'default_time_point'
                return time_point_name
        return None


def test_time_point():
    tp = TimePoints({datetime.time(1, 1, 1): 't1',
                     datetime.time(1, 2, 1): 't2',
                     datetime.time(1, 3, 1): 't3',
                     })
    assert 't1' == tp.hit(
        datetime.datetime.combine(dttoday(), datetime.time(1, 1, 2)))
    assert not tp.hit(
        datetime.datetime.combine(dttoday(), datetime.time(1, 1, 2)))
    assert 't3' == tp.hit(
        datetime.datetime.combine(dttoday(), datetime.time(1, 3, 2)))


def main():
    pass


if __name__ == '__main__':
    main()
