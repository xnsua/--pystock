from typing import List

from common.helper import p_repr
from stock_data_manager.stock_data.int_trade_day import intday_span


class HoldPeriod:
    def __init__(self, stock_code, start_date, end_date, buy_price, sell_price):
        self.stock_code = stock_code
        self.start_date = start_date
        self.buy_price = buy_price
        self.end_date = end_date
        self.sell_price = sell_price

        self.period_len = None
        self.yield_ = None
        self.yyield = None

        self._calc_info()

    def _calc_info(self):
        # May not use.
        self.period_len = intday_span(self.start_date, self.end_date)
        self.yield_ = (self.sell_price / self.buy_price)
        self.yyield = self.yield_ ** (245 / self.period_len)


class SingleEmuAccount:
    def __init__(self, code, date_range, yield_):
        self.code = code
        self.hold_periods = []  # type: List[HoldPeriod]

        self._buy_day = None
        self._buy_price = None

        self.date_range = date_range
        self.day_len = intday_span(*date_range)

        self.yield_ = yield_
        self.yyield = yield_ ** (245 / self.day_len)

        self.hold_len = None
        self.hold_yield = None
        self.hold_yyield = None
        self.occupy_per = None

        self.df = None

    def buy(self, day, price):
        if not self._buy_day:
            self._buy_day = day
            self._buy_price = price

    def sell(self, day, price):
        if self._buy_day:
            self.hold_periods.append(
                HoldPeriod(self.code, self._buy_day, day, self._buy_price, price)
            )
            self._buy_day = None

    def calc_addition_infos(self):
        if self.df is None:
            import pandas
            pandas.options.display.float_format = '{:,.3f}'.format
            df = pandas.DataFrame([item.__dict__ for item in self.hold_periods])
            df = df[
                ['stock_code', 'start_date', 'end_date', 'buy_price', 'sell_price', 'period_len',
                 'yield_', 'yyield']]
            self.df = df
        self.hold_len = self.df.period_len.sum()
        self.hold_yield = self.df.yield_.prod()
        self.hold_yyield = self.hold_yield ** (245 / self.hold_len)

        self.occupy_per = self.hold_len / self.day_len

        return self

    def __repr__(self):
        occupy_per = p_repr(self.occupy_per)
        yyield, hold_yyield = p_repr(self.yyield), p_repr(self.hold_yyield)
        return f'Acc:{{day_len: {self.day_len}  hold_len: {self.hold_len}  occupy_per: {occupy_per}\n' \
               f'       yyield: {yyield}  hold_yyield: {hold_yyield}'
