from contextlib import suppress
from queue import Empty

from common.helper import to_logstr
from common.log_helper import jqd, mylog
from data_server.day_data_manager import update_etf
from stock_basic.stock_helper import etf_t1, etf_t0
from trade.comm_message import CommMessage
from trade.trade_constant import *
from trade.trade_context import TradeContext

_tcc = TradeCommicationConstant


def thread_buy_after_drop(**param):
    try:
        obj = BuyAfterDrop(param)
        obj.run_loop()
    except Exception as e:
        mylog.fatal(to_logstr(e))


class BuyAfterDrop:
    def __init__(self, trade_context: TradeContext, **param_dict):
        trade_context.thread_local.name = _tcc.idm_buy_after_drop
        self.tc = trade_context

        self.drop_days = param_dict[ModelConstant.bsm_drop_days]

        self.etf_day_data = None

    def prepare(self):
        self.etf_day_data = update_etf()
        self.tc.add_monitored_stock([*etf_t1, *etf_t0])

    def run_loop(self):
        self.prepare()
        while True:
            with suppress(Empty):
                msg = self.self_queue.get()
                self.dispatch_msg(msg)

    def on_realtime_stock_info(self, sender, param):
        del sender
        del param

    def dispatch_msg(self, msg: CommMessage):
        jqd(f'BuyAfterDrop: Receive Message: {msg}')
        sender = msg.sender
        func = self.find_operation(msg.operation)
        param = msg.param
        rval = func(sender, param)
        msg.put_result(rval)

    def find_operation(self, operation_name):
        operdict = {_tcc.msg_push_realtime_stocks: self.on_realtime_stock_info}
        return operdict[operation_name]


def main():
    pass


if __name__ == '__main__':
    main()
