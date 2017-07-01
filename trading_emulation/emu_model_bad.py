from common_stock.py_dataframe import RealtimeDataRepr
from ip.st import FIXED_PRICE
from models.abstract_model import AbstractModel
from stock_analyser.day_attr_analyser import gdroprise_pv
from stock_data_updater.data_provider import gdata_pv
from trading.abstract_context import AbstractContext


class EmuModelBad(AbstractModel):
    def __init__(self, stock_codes, drop_threshold):
        super().__init__()
        self.stock_codes = stock_codes
        self.drop_threshold = drop_threshold

        self.rise_cnt = None
        self.drop_cnt = None

    def name(self):
        return 'EmuModelBad'

    def init_model(self, ctx: AbstractContext):
        super().init_model(ctx)

    def on_bid_over(self, context: AbstractContext, rdr: RealtimeDataRepr):
        date_str = context.date_str
        super().on_bid_over(context, rdr)
        code = self.stock_codes[0]
        ##
        # if gdata_pv.has_data(code, date_str):
        #     drop_cnt = gdroprise_pv.drop(code, date_str)
        #     if drop_cnt == self.drop_threshold:
        #         context.account.buy_at_most(code, gdata_pv.open(code, date_str), FIXED_PRICE)
        #         context.account.sell_at_most(code, gdata_pv.open(code, gtrade_day.next(date_str)), FIXED_PRICE)
        #     print(context.date_str, context.account.available)

        #
        if gdata_pv.has_data(code, date_str):
            drop_cnt = gdroprise_pv.drop(code, date_str)
            if drop_cnt == self.drop_threshold:
                context.account.buy_at_most(code, gdata_pv.open(code, date_str), FIXED_PRICE)
            else:
                context.account.sell_at_most(code, gdata_pv.open(code, date_str), FIXED_PRICE)
            # print(context.date_str, context.account.available)

    def handle_bar(self, context: AbstractContext, rdr: RealtimeDataRepr):
        super().handle_bar(context, rdr)

    def on_trade_over(self, context: AbstractContext, rdr: RealtimeDataRepr):
        super().on_trade_over(context, rdr)

