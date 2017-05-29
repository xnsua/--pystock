import datetime
from statistics import mean

from common.scipy_helper import pdDF
from common_stock.stock_data_constants import etf_with_amount
from common_stock.trade_day import last_n_trade_day
from data_manager.stock_day_bar_manager import DayBar
from project_helper.logbook_logger import jqd, mylog
from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext


class ModelBuyAfterDrop(AbstractModel):
    @classmethod
    def name(cls):
        return '__MODEL_BAD'

    def __init__(self, trade_context: TradeContext):
        super().__init__()
        self.context = trade_context
        self.etf_code_range = etf_with_amount
        self.etf_dict = None
        self.etf_to_buy = None

    def log(self, msg):
        jqd(f'{self.context.thread_local.name}:: {msg}')

    def init_model(self):
        mylog.debug('Init model')
        self.context.add_push_stock(self.etf_to_buy)
        self.etf_dict = read_df_dict(self.etf_code_range)
        self.etf_to_buy = query_stock_to_buy(self.etf_dict, datetime.datetime.now())

    def on_bid_over(self, df: pdDF):
        assert all(df.open)

    def handle_bar(self, df: pdDF):
        mylog.debug('Handle bar')
        del df
        pass

    def on_account_info(self, type_, content):
        mylog.debug(f'On account info: {type_}, {content}')
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


def query_stock_to_buy(df_dict, now):
    buy_stocks = []
    for stock_code in etf_with_amount:
        try:
            if is_buy(df_dict[stock_code], now):
                buy_stocks.append(stock_code)
        except Exception:
            mylog.exception('Query stock to buy')
    return buy_stocks


def read_df_dict(etfs):
    etf_dict = {}
    for etf in etfs:
        etf_dict[etf] = DayBar.read_etf_day_data(etf)
    return etf_dict
