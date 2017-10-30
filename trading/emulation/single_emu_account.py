from typing import List

from common.helper import p_repr
from stock_data_manager.stock_data import int_trade_day
from stock_data_manager.stock_data.int_trade_day import intday_span


class HoldPeriod:
    def __init__(self, code, start_ts, end_ts, buy_price, sell_price):
        self.code = code
        self.buy_ts = start_ts
        self.buy_price = buy_price
        self.sell_ts = end_ts
        self.sell_price = sell_price

        # Field to calc
        self.hold_len = None
        self.yield_ = None
        self.yyield = None

        self._calc_info()

    def _calc_info(self):
        self.hold_len = intday_span(self.buy_ts, self.sell_ts)
        self.yield_ = (self.sell_price / self.buy_price)
        self.yyield = self.yield_ ** (245 / self.hold_len)

    def __bool__(self):
        return bool(self.buy_ts < self.sell_ts)

    def left_trim(self, day_len, price_series):
        new_intday = int_trade_day.increment_intday(self.buy_ts, day_len)
        try:
            loc = price_series.index.get_loc(new_intday, method='bfill')
        except:
            self.buy_ts = self.sell_ts
            return self
        self.buy_ts = price_series.index[loc]
        self.buy_price = price_series.values[loc]
        if self:
            self._calc_info()
        return self


class SingleEmuAccount:
    def __init__(self, code, date_range, yield_):
        self.code = code

        self._buy_time = None
        self._buy_price = None

        self.date_range = date_range
        self.day_len = intday_span(*date_range)

        self.yield_ = yield_
        self.yyield = yield_ ** (245 / self.day_len)

        self.hold_periods = []  # type: List[HoldPeriod]
        # These attr is calculated buy self.hold_periods
        self.hold_len = None
        self.hold_yield = None
        self.hold_yyield = None
        self.occupy_per = None

        self.ygain = None
        self.hold_df = None

    def buy(self, day, price):
        if not self._buy_time:
            self._buy_time = day
            self._buy_price = price

    def sell(self, day, price):
        if self._buy_time:
            self.hold_periods.append(
                HoldPeriod(self.code, self._buy_time, day, self._buy_price, price)
            )
            self._buy_time = None

    def reset_hold_period(self, hold_periods):
        self.hold_periods = hold_periods
        self.hold_df = None
        self.calc_addition_infos()

    def calc_addition_infos(self):
        if self.hold_df is None:
            import pandas
            pandas.options.display.float_format = '{:,.3f}'.format
            df = pandas.DataFrame([item.__dict__ for item in self.hold_periods])
            if len(df):
                df = df[
                    ['code', 'buy_ts', 'sell_ts', 'buy_price', 'sell_price',
                     'hold_len',
                     'yield_', 'yyield']]
                self.hold_len = df.hold_len.sum()
                self.hold_yield = df.yield_.prod()
                self.hold_yyield = self.hold_yield ** (245 / self.hold_len)

                self.occupy_per = self.hold_len / self.day_len

                self.ygain = self.hold_yyield / self.yyield
            else:
                self.hold_len = self.day_len
                self.hold_yield = 1
                self.hold_yyield = 1
                self.occupy_per = 1
            self.hold_df = df

        return self

    def __repr__(self):
        occupy_per = p_repr(self.occupy_per, 4)
        yyield, hold_yyield = p_repr(self.yyield, 4), p_repr(self.hold_yyield, 4)
        return f'Acc:{{day_len: {self.day_len}  hold_len: {self.hold_len}  occupy_per: {occupy_per}\n' \
               f'       yyield: {yyield}  hold_yyield: {hold_yyield}'

    # helper functions
    def plot(self):
        import matplotlib.pyplot as plt
        from common_stock.stock_plotter import StockAxisPlot
        from stock_data_manager.ddr_file_cache import read_ddr_fast
        df = read_ddr_fast(self.code).df
        df = df[df.index <= self.date_range[1]]
        df = df[df.index >= self.date_range[0]]

        fig, ax = plt.subplots()
        stock_plotter = StockAxisPlot((fig, ax), df, code=self.code)

        from common.scipy_helper import pdSr
        buy_series = pdSr(data=[item.buy_price for item in self.hold_periods],
                          index=[item.buy_ts for item in self.hold_periods])
        sell_series = pdSr(data=[item.sell_price for item in self.hold_periods],
                           index=[item.sell_ts for item in self.hold_periods])
        # print(buy_series)
        # print(sell_series)
        stock_plotter.add_scatter_point('buy', buy_series, color='k', marker='^')
        stock_plotter.add_scatter_point('sell', sell_series, color='k', marker='v')
        hold_days = [(item.buy_ts, item.sell_ts) for item in self.hold_periods]
        stock_plotter.add_hold_info(hold_days)
        plt.title(self.code)
        stock_plotter.plot()
        plt.show()

    def overlap_other(self, other: 'SingleEmuAccount'):
        new_periods = SingleEmuAccount._calc_overlapped_hold_periods(self.hold_periods,
                                                                     other.hold_periods)
        acc = SingleEmuAccount(self.code, self.date_range, self.yield_)
        acc.hold_periods = new_periods
        acc.calc_addition_infos()
        return acc

    @staticmethod
    def _calc_overlapped_hold_periods(ps1, ps2):
        index1 = 0
        index2 = 0
        periods1 = ps1  # type: List[HoldPeriod]
        periods2 = ps2  # type: List[HoldPeriod]

        new_periods = []

        while index1 < len(periods1) and index2 < len(periods2):
            p1 = periods1[index1]
            p2 = periods2[index2]

            max_start = max(p1.buy_ts, p2.buy_ts)
            min_end = min(p1.sell_ts, p2.sell_ts)
            buy_price = p1.buy_price if max_start == p1.buy_ts else p2.buy_price
            sell_price = p1.sell_price if min_end == p1.sell_ts else p2.sell_price
            if min_end > max_start:
                tmp = HoldPeriod(p1.code, max_start, min_end, buy_price, sell_price)
                new_periods.append(tmp)

            if p1.sell_ts < p2.sell_ts:
                index1 = index1 + 1
            else:
                index2 = index2 + 1
        return new_periods

    def trim_hold_periods(self, day_len, price_sr):
        if day_len == 0:
            return self
        hold_periods = [item.left_trim(day_len, price_sr) for item in self.hold_periods]
        hold_periods = list(filter(bool, hold_periods))
        self.reset_hold_period(hold_periods)
        return self
