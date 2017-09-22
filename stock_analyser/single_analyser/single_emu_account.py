from operator import attrgetter
from typing import List

from common_stock.stock_helper import int_to_date, f_repr


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
    def __init__(self):
        self.max_earn = None  # type: _HoldPeriod
        self.max_lose = None  # type: _HoldPeriod
        self.max_year_earn = None  # type: _HoldPeriod
        self.max_year_lose = None  # type: _HoldPeriod

        # include Earn, YearEarn and Hold percentage, Hold Earn.
        self.recent_year_infos = None


class SingleEmuAccount:
    def __init__(self, code, ddr, init_money=10000, skip_len=0, loss_stop=None):
        self.init_money = init_money

        self._cur_money = init_money
        self._cur_stock = 0
        self._cur_hold_day = 0
        self._cur_index = None

        self.assets = []
        self.operations = []  # type: List[_AccountOperation]
        self.hold_periods = []  # type: List[_HoldPeriod]
        self.hold_days = []

        self.buy_count = 0

        self.dates = [int_to_date(val) for val in ddr.days]

        self.stat = _Statistic()

        self.prices = []
        self.code = code
        self.model_str = None
        self.skip_len = skip_len
        self.loss_stop = loss_stop

        self.ddr = ddr

    def on_date_begin(self, index):
        assert not self._cur_index or self._cur_index == index - 1
        self._cur_index = index

    def on_date_finished(self, index, ochl):
        # loss stop
        open_price = ochl[0]
        close_price = ochl[1]
        low_price = ochl[3]
        if self.loss_stop and self.operations:
            oper = self.operations[-1]
            stop_price = oper.price * (1 - self.loss_stop)
            if oper.index != index and oper.isbuy and stop_price > low_price:
                stop_price = min(stop_price, open_price)
                if stop_price:
                    self.sell(stop_price)

        assert self._cur_index == index
        self.assets.append(self._cur_money + self._cur_stock * close_price)
        self.prices.append(close_price)
        if self._cur_stock != 0:
            self._cur_hold_day += 1
        self.hold_days.append(self._cur_hold_day)

    def buy(self, price, add_info=None):
        if self._cur_money:
            self._cur_stock += self._cur_money / price
            self.buy_count += 1
            self.operations.append(_AccountOperation(1, price, self._cur_index, add_info))
            self._cur_money = 0

    def sell(self, price, add_info=None):
        if self._cur_stock:
            self._cur_money += self._cur_stock * price
            self.operations.append(_AccountOperation(0, price, self._cur_index, add_info))
            self._cur_stock = 0

    def calc_statistics(self):
        assert len(self.assets) == len(self.dates)
        self.hold_periods = []  # type: List[_HoldPeriod]
        for val1, val2 in zip(self.operations[0::2], self.operations[1::2]):
            duration = val2.index - val1.index
            yield_ = val2.price / val1.price
            year_yield = yield_ ** (245 / duration)
            self.hold_periods.append(
                _HoldPeriod(val1.index, val2.index, duration, yield_, year_yield))

        total_hold_len = sum([item.hold_len for item in self.hold_periods])
        self.stat.hold_percentage = total_hold_len / len(self.dates)

        self.stat.max_earn = max(self.hold_periods, key=attrgetter('yield_'))
        self.stat.max_year_earn = max(self.hold_periods, key=attrgetter('year_yield'))

        self.stat.max_lose = min(self.hold_periods, key=attrgetter('yield_'))
        self.stat.max_year_lose = min(self.hold_periods, key=attrgetter('year_yield'))

        self.stat.earn = (self.assets[-1] / self.init_money)
        self.stat.year_earn = self.stat.earn ** (245 / len(self.dates))

        self.stat.recent_year_infos = self.calc_recent_year_info()
        self.stat.original_earn = self.prices[-1] / self.prices[self.skip_len]
        self.stat.original_year_earn = self.stat.original_earn ** (
            245 / (len(self.assets) - self.skip_len))

    def print_hold_period(self):
        print('Hold period:')
        for item in self.hold_periods:
            print('yield:', f_repr(item.yield_), self.dates[item.start_index],
                  self.dates[item.end_index], f_repr(item.yield_), item.hold_len, sep='  ')

    def print_statistic(self):
        if not self.stat.recent_year_infos:
            self.calc_statistics()
        print('STATUS:: Code: ', self.code, 'Modle:', self.model_str)
        print('from', self.dates[0], 'to', self.dates[-1])
        t_recent_earn = list(zip(*self.stat.recent_year_infos))
        earns1 = list(map(f_repr, t_recent_earn[0]))
        earns2 = list(map(f_repr, t_recent_earn[1]))
        hold_pers = list(map(f_repr, t_recent_earn[2]))
        hold_earns = list(map(f_repr, t_recent_earn[3]))
        self._print_line(['', '_All_', '1_y', '2_y', '3_y', '5_y'], [10, *[8] * 5],
                         [1, *[0] * 5])
        self._print_line(['Earn: ', *earns1], [10, *[8] * 5], [1, *[0] * 5])
        self._print_line(['OriEarn: ', *earns2], [10, *[8] * 5], [1, *[0] * 5])
        self._print_line(['HoldPer: ', *hold_pers], [10, *[8] * 5], [1, *[0] * 5])
        self._print_line(['HoldEarn: ', *hold_earns], [10, *[8] * 5], [1, *[0] * 5])
        print('')
        return
        current_period = self.stat.max_earn
        print(
            f'      max_earn : {f_repr(current_period.yield_)} , {self.dates[current_period.start_index]}__{self.dates[current_period.end_index]}')
        current_period = self.stat.max_earn
        print(
            f' max_year_earn : {f_repr(current_period.yield_)} , {self.dates[current_period.start_index]}__{self.dates[current_period.end_index]}')
        current_period = self.stat.max_lose
        print(
            f'      max_lose : {f_repr(current_period.yield_)} , {self.dates[current_period.start_index]}__{self.dates[current_period.end_index]}')
        current_period = self.stat.max_year_lose
        print(
            f' max_year_lose : {f_repr(current_period.yield_)} , {self.dates[current_period.start_index]}__{self.dates[current_period.end_index]}')
        print()

    def _print_line(self, items, widths, aligns, new_line=True):
        for i, val in enumerate(items):
            if aligns[i] == 0:
                print('{:<{}s}'.format(str(val), widths[i]), end='')
            else:
                print('{:>{}s}'.format(str(val), widths[i]), end='')
        if new_line:
            print('')

    def calc_recent_year_info(self):
        earns = []
        year_days = 245
        for i in [0, 1, 2, 3, 5]:
            if i == 0:
                days = len(self.dates) - self.skip_len
            else:
                days = year_days * i

            if len(self.assets) >= days + self.skip_len:
                hold_percentage = (self.hold_days[-1] - self.hold_days[-days]) / days
                year_earn = (self.assets[-1] / self.assets[-days]) ** (245 / days)
                hold_year_earn = year_earn ** (1 / hold_percentage)
                original_year_earn = (self.prices[-1] / self.prices[-days]) ** (245 / days)
                earns.append((year_earn, original_year_earn, hold_percentage, hold_year_earn))
            else:
                earns.append((None, None, None, None))
        return earns
