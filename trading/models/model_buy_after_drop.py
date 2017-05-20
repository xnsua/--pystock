from statistics import mean

from common.log_helper import mylog
from stock_basic.stock_helper import etf_with_amount
from trading.models.model_base import ModelBase
from trading.scipy_helper import pdDF
from trading.trade_helper import last_n_trade_day

logger = mylog


class ModelBuyAfterDrop(ModelBase):
    def __init__(self):
        super().__init__()
        pass

    def init_model(self):
        self.context.add_monitored_stock([etf_with_amount])

    def on_bid_over(self):
        pass


    def handle_bar(self):
        pass


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
            mylog.exception(inst)
    return buy_stocks
