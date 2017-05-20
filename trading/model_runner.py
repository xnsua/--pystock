from statistics import mean

from common.helper import to_log_str
from common.log_helper import jqd, mylog
from stock_basic.stock_helper import etf_with_amount
from trading.comm_message import CommMessage
from trading.models import model_buy_after_drop
from trading.scipy_helper import pdDF
from trading.trade_context import TradeContext
from trading.trade_helper import ktc_, alert_exception, last_n_trade_day, kca_, kst_


def thread_model(trade_context, model, **param):
    try:
        obj = ThreadModel(trade_context, model, param)
        obj.run_loop()
    except Exception:
        mylog.exception('Trade model exception')
        alert_exception(10)


class ThreadModel:
    def __init__(self, trade_context: TradeContext, model_class, param_dict):
        trade_context.thread_local.name = model_class.__name__
        self.trade_context = trade_context

        self.model = model_class(trade_context, param_dict)
        self.self_queue = trade_context.get_current_thread_queue()

        self.model = model_class(param_dict)  # type: model_buy_after_drop

    # Initiate the model
    def prepare(self):
        context = self.model.init_model()
        self.trade_context.on_init_model(context)

    def run_loop(self):
        self.prepare()
        while True:
            msg = self.self_queue.get()
            self.dispatch_msg(msg)

    # noinspection PyUnusedLocal
    def on_realtime_stock_info(self, sender, param, msg_dt):
        if self.stocks_to_buy is None:
            stocks_to_buy = self.query_buy_stocks(self.etf_day_data, msg_dt)

        for stock in stocks_to_buy:
            result = self.trade_context.buy_stock(stock, param[kst_.open], 100, kca_.fixed_price)

    def dispatch_msg(self, msg: CommMessage):
        jqd(f'BuyAfterDrop: Receive Message: {msg}')
        sender = msg.sender
        func = self.find_operation(msg.operation)
        param = msg.param
        msg_dt = msg.msg_dt
        rval = func(sender, param, msg_dt)
        msg.put_result(rval)

    def find_operation(self, operation_name):
        operation_dict = {ktc_.msg_push_realtime_stocks: self.on_realtime_stock_info}
        return operation_dict[operation_name]

    @staticmethod
    def is_buy(df: pdDF, now):
        last_ndays = last_n_trade_day(now.date(), 4)
        last_trade_day = last_ndays[-2]
        row_index = df.index.get_loc(str(last_trade_day))
        start_index = row_index - 2
        new_df = df.iloc[start_index:row_index + 1, :]
        if list(map(str, last_ndays[:-1])) == list(new_df.index):
            close_prices = new_df.close
            trade_amount = new_df.close * new_df.volume * 100
            mean_amount = (mean(trade_amount))
            if mean_amount > 1_000_000:
                buy = all(j < i for i, j in zip(close_prices, close_prices[1:]))
                return buy
        return False

    def query_buy_stocks(self, df_dict, now):
        buy_stocks = []
        for stock_code in etf_with_amount:
            try:
                if self.is_buy(df_dict[stock_code], now):
                    buy_stocks.append(stock_code)
            except Exception as inst:
                mylog.info(f'Buy stock fail with exception {to_log_str(inst)}')
        return buy_stocks


def main():
    pass


if __name__ == '__main__':
    main()
