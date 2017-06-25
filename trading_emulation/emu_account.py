import copy

from nose.tools import assert_equal
from stock_data_updater.classify import all_etf_code_list


class EmuAccount:
    buy_fee = 25 / 100_000
    buy_fee_tuple = (25, 100_000)
    sell_fee = 25 / 100_000
    tax = 1 / 1_000

    def __init__(self, balance=.0, total_assert=.0):
        assert total_assert >= balance
        self.balance = balance * 1.0
        self.total_assert = total_assert * 1.0

        self.stock2amount = {}
        self.non_sell_stocks2amount = {}

    def copy_for_new_day(self):
        ea = EmuAccount(self.balance, self.balance)
        ea.stock2amount = copy.deepcopy(self.stock2amount)
        return ea

    def buy_stock(self, code, price, amount):
        assert amount % 100 == 0, 'Not proper amount'
        need_money = round(price * amount * (1 + self.buy_fee), 3)
        assert self.balance >= need_money
        self.balance -= need_money
        self.balance = round(self.balance, 3)
        self.stock2amount[code] = self.stock2amount.get(code, 0) + amount
        self.non_sell_stocks2amount[code] = self.non_sell_stocks2amount.get(code, 0) + amount
        return self

    def sell_stock(self, code, price, amount):
        assert self.stock2amount.get(code, 0) >= amount
        sell_money = round(price * amount * (1 - self.sell_fee), 3)
        if code not in all_etf_code_list:
            print('not in etf code list')
            sell_money = round(sell_money * (1 - self.tax), 3)
        self.balance += sell_money
        self.balance = round(self.balance, 3)
        self.stock2amount[code] = self.stock2amount[code] - amount
        self.non_sell_stocks2amount[code] = self.non_sell_stocks2amount.get(code, 0) - amount

    def buy_all(self, code, price):
        amount = self.balance * self.buy_fee_tuple[1] // \
                 ((self.buy_fee_tuple[1] + self.buy_fee_tuple[0]) * price * 100)
        amount = 100 * int(amount)
        return self.buy_stock(code, price, amount)

    def calc_total_asset(self, stock2price):
        self.total_assert = self.balance
        price = [stock2price[stock] * amount for stock, amount in self.stock2amount.items()]
        self.total_assert += round(sum(price), 3)

    def __repr__(self):
        return f'TotalAssert:{self.total_assert: <12.12} Balance:{self.balance:<12} Stocks:{self.stock2amount}'


def test_copy_for_new_day():
    ea = EmuAccount(1000, 1000)
    ea.non_sell_stocks = {1: 2}
    ea_new = ea.copy_for_new_day()
    assert not ea_new.non_sell_stocks2amount


def test_buy_etf():
    ea = EmuAccount(100_025, 100_1025)
    ea.buy_stock('510900', 1, 100_000)
    assert_equal(ea.balance, 0)
    assert ea.stock2amount == {'510900': 100000}
    assert ea.non_sell_stocks2amount == {'510900': 100000}


def test_buy_stock():
    ea = EmuAccount(100_025, 100_1025)
    ea.buy_stock('510900', 1, 100_000)
    assert ea.stock2amount == {'510900': 100000}
    assert ea.non_sell_stocks2amount == {'510900': 100000}


def test_sell_etf():
    ea = EmuAccount()
    ea.stock2amount = {'510900': 100000}
    ea.sell_stock('510900', 1, 100000)
    assert ea.balance == 99975


def test_sell_stock():
    ea = EmuAccount()
    ea.stock2amount = {'000001': 100000}
    ea.sell_stock('000001', 1, 100000)
    assert ea.balance == 99875.025


def test_buy_all():
    ea = EmuAccount()
    ea.balance = 100025
    ea.buy_all('510900', 1)
    assert_equal(ea.balance, 0)
    assert_equal(ea.stock2amount['510900'], 100000)
    assert_equal(ea.non_sell_stocks2amount, {'510900': 100000})
