import datetime
import pathlib
from statistics import mean
from typing import List

from common.persistent_descriptor import create_persistent_descriptor_class
from common.scipy_helper import pdDF
from common_stock.stock_data_constants import etf_with_amount
from common_stock.stock_day_bar_manager import DayBar
from common_stock.trade_day import last_n_trade_day
from ip.st import EntrustItem
from ip.st import EntrustType, ClientOperCancel, EntrustWay, ClientOperSell
from project_helper.logbook_logger import mylog, jqd
from trading.models.model_base import AbstractModel
from trading.trade_context import TradeContext

persistent_descriptor = create_persistent_descriptor_class(
    str(pathlib.Path(pathlib.Path(__file__).parent) / 'model_buy_after_drop'))

class ModelBuyAfterDrop(AbstractModel):
    buy_entrust = persistent_descriptor('buy_entrust')  # type: List[EntrustItem]
    @classmethod
    def name(cls):
        return '__MODEL_BAD'

    def __init__(self, trade_context: TradeContext):
        super().__init__()
        self.context = trade_context
        self.account_manager = trade_context.account_manager
        self.etf_code_range = etf_with_amount
        self.etf_dict = None
        self.etf_to_buy = None

        self._push_times = 0
        self._oper_dict = {
            1: ClientOperSell('SH.510900', 1.23, 100, EntrustType.FIXED_PRICE)
        }

    def log_account_info(self):
        try:
            log_str = f'ACCOUNT_INFO: ' \
                      f'Available: {self.account_manager.available}  ' \
                      f'ShareCount: {len(self.account_manager.share_items)}  ' \
                      f'EntrustCount: {len(self.account_manager.entrust_items)}  '
            mylog.info(log_str)
        except Exception as e:
            # noinspection PyProtectedMember
            mylog.info(
                f'*** There is NO account info {self.account_manager._account_info}, Exception: {e}')

    def init_model(self):
        self.log_account_info()
        mylog.debug('Init model')
        self.etf_to_buy = ['510900', '510050']
        self.context.add_push_stock(self.etf_to_buy)
        self.etf_dict = read_df_dict(self.etf_code_range)
        self.etf_to_buy = query_stock_to_buy(self.etf_dict, datetime.datetime.now())

    def on_bid_over(self, df: pdDF):
        self.log_account_info()
        mylog.info('On bid over\n' + str(df))
        assert all(df.open)

    def handle_bar(self, df: pdDF):
        #        open    yclose  price  high   low   name
        # 510900  1.152   1.145  1.151  1.157  1.149  H股ETF
        # 510050  2.490   2.490  2.472  2.494  2.466  50ETF

        self._push_times += 1
        if self._push_times / 20 ==
        mylog.info('On handle bar --------')
        oper = self._oper_dict.get(self._push_times, None)
        if oper:
            mylog.info(f'Send operation {oper}')
            self.context.send_oper(oper)
            mylog.info(f'Operation result', oper.result)
            assert oper.result.success
            # noinspection PyAttributeOutsideInit
            self.entrust_id = oper.result.entrust_id
            jqd('self.entrust_id:::', self.entrust_id)
        else:
            if hasattr(self, 'entrust_id'):
                result = self.context.send_oper(
                    ClientOperCancel(self.entrust_id, 'SH.510900', EntrustWay.way_sell))
                mylog.warn(f'Cancel result {result.__dict__}')
                del self.entrust_id


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
