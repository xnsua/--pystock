from typing import List

from common_stock.stock_helper import int_to_date


class _AccountOperation:
    def __init__(self, isbuy, price, index, add_info):
        self.isbuy = isbuy
        self.price = price
        self.index = index
        self.add_info = add_info


class _HoldPeriod:
    def __init__(self, start_index, end_date, hold_days, yield_, year_yield):
        self.start_index = start_index
        self.end_index = end_date
        self.hold_len = hold_days
        self.yield_ = yield_
        self.year_yield = year_yield


class _Statistic:
    def __init__(self, hold_periods, max_earn, max_lose, hold_percentage):
        self.hold_periods = hold_periods  # type: List[_HoldPeriod]
        self.max_earn = max_earn
        self.max_lose = max_lose
        self.hold_percentage = hold_percentage


class SimpleEmuAccount:
    def __init__(self, init_money=10000, ddr=None):
        self.init_money = init_money

        self.money = init_money
        self.stock = None
        self.assets = []
        self.operations = []  # type: List[_AccountOperation]

        self.buy_count = 0
        self.current_index = None

        self.dates = [int_to_date(val) for val in self.ddr.days]
        self.ddr = ddr

        self.statistics = None

    def on_date_finished(self, index, price):
        self.current_index = index
        self.assets.append(self.money + self.stock * price)

    def buy(self, price, add_info=None):
        assert self.money
        if self.money:
            self.stock += self.money / price
            self.buy_count += 1
            self.operations += _AccountOperation(1, price, self.current_index, add_info)
            self.money = 0

    def sell(self, price, add_info=None):
        assert self.stock
        if self.stock:
            self.money += self.stock * price
            self.operations += _AccountOperation(0, price, self.current_index, add_info)
            self.stock = 0

    def calc_statistics(self):
        hold_periods = []  # type: List[_HoldPeriod]
        for val1, val2 in zip(self.operations[0::2], self.operations[1::2]):
                duration = val2.index - val1.index
                yield_ = val2.price / val1.price
                year_yield = yield_ ** (245 / duration)
                start_date = self.dates[val2.index]
                end_date = self.dates[val2.index]
                hold_periods.append(
                    _HoldPeriod(start_date, end_date, duration, yield_, year_yield))
        total_hold_len = sum([item.hold_len for item in hold_periods])
        hold_percentage = total_hold_len / len(self.ddr.days)


