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
        self.total_hold_len = None
        self.earn = None
        self.year_earn = None
        self.max_earn = None  # type: _HoldPeriod
        self.max_lose = None  # type: _HoldPeriod
        self.max_year_earn = None  # type: _HoldPeriod
        self.max_year_lose = None  # type: _HoldPeriod
        self.hold_percentage = None

        self.recent_year_earn = None

        # Assign by others because calculation need skiplen.
        self.original_year_earn = None
        self.original_earn = None


class SingleEmuAccount:
    def __init__(self, code, ddr, init_money=10000, skip_len=0):
        self.init_money = init_money

        self._cur_money = init_money
        self._cur_stock = 0
        self._cur_hold_day = 0
        self.assets = []
        self.operations = []  # type: List[_AccountOperation]
        self.hold_periods = []  # type: List[_HoldPeriod]
        self.hold_days = []

        self.buy_count = 0
        self.current_index = None

        self.dates = [int_to_date(val) for val in ddr.days]

        self.stat = _Statistic()

        self.prices = []
        self.code = code
        self.model_str = None
        self.skip_len = skip_len

    def on_date_begin(self, index):
        assert not self.current_index or self.current_index == index - 1
        self.current_index = index

    def on_date_finished(self, index, price):
        assert self.current_index == index
        self.assets.append(self._cur_money + self._cur_stock * price)
        self.prices.append(price)
        if self._cur_stock != 0:
            self._cur_hold_day += 1
        self.hold_days.append(self._cur_hold_day)

    def buy(self, price, add_info=None):
        if self._cur_money:
            self._cur_stock += self._cur_money / price
            self.buy_count += 1
            self.operations.append(_AccountOperation(1, price, self.current_index, add_info))
            self._cur_money = 0

    def sell(self, price, add_info=None):
        if self._cur_stock:
            self._cur_money += self._cur_stock * price
            self.operations.append(_AccountOperation(0, price, self.current_index, add_info))
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

        self.stat.recent_year_earn = self.calc_recent_year_info()
        self.stat.original_earn = self.prices[-1] / self.prices[self.skip_len]
        self.stat.original_year_earn = self.stat.original_earn ** (
            245 / (len(self.assets) - self.skip_len))

    def print_hold_period(self):
        for item in self.hold_periods:
            print(f_repr(item.yield_), self.dates[item.start_index], self.dates[item.end_index], item.hold_len, sep='  ')


    def print_statistic(self):
        if not self.stat.hold_percentage:
            self.calc_statistics()
        print('STATUS:: Code: ', self.code, 'Modle:', self.model_str)
        print(self.dates[0], self.dates[-1])
        t_recent_earn = list(zip(*self.stat.recent_year_earn))
        earns1 = list(map(f_repr, t_recent_earn[0]))
        earns2 = list(map(f_repr, t_recent_earn[1]))
        hold_pers = list(map(f_repr, t_recent_earn[2]))
        self._print_line(['Earn: ', f_repr(self.stat.year_earn), *earns1], [10, 8, *[8] * 4],
                         [1, 0, *[0] * 4])
        self._print_line(['OriEarn: ', f_repr(self.stat.original_year_earn), *earns2],
                         [10, 8, *[8] * 4],
                         [1, 0, *[0] * 4])
        self._print_line(['HoldPer: ', f_repr(self.stat.hold_percentage), *hold_pers],
                         [10, 8, *[8] * 4],
                         [1, 0, *[0] * 4])
        print('')
        return
        original_year_earn = (self.prices[-1] / self.prices[0]) ** (245 / len(self.dates))
        print(
            f'     year_earn : {f_repr(self.stat.year_earn)},  original year earn : {f_repr(original_year_earn)}')
        current_period = self.stat.max_earn
        recent_year_earn = self.stat.recent_year_earn
        earn_str = ''
        original_earn_str = ''
        for i in recent_year_earn:
            earn_str += f_repr(i[0]) + '  '

        print(f' 1-2-3-5 :', f_repr(self.pri))
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

    def _print_line_item(self, val, width, align):
        if align == 0:
            print('{:<{}s}'.format(str(val), width, end=''))
        else:
            print('{:>{}s}'.format(str(val), width), end='')

    def calc_recent_year_info(self):
        earns = []
        year_days = 245
        period_pos = -1
        for i in [1, 2, 3, 5]:
            days = year_days * i
            if len(self.assets) > days:
                hold_percentage = (self.hold_days[-1] - self.hold_days[-days]) /days
                days = i * year_days
                year_earn = (self.assets[-1] / self.assets[-days]) ** (1 / i)
                original_year_earn = (self.prices[-1] / self.prices[-days]) ** (1 / i)
                earns.append((year_earn, original_year_earn, hold_percentage))
            else:
                earns.append((None, None, None))
        return earns
