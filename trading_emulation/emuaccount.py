import copy
from typing import List

from nose.tools import assert_equal

from ip.st import EntrustWay
from stock_data_updater.classify import etf_stdcode2name
from stock_data_updater.data_provider import gdata_pv
from trading.abstract_account import AbstractAccount

def set_account_none_fee():
    EmuAccount.buy_fee = 0
    EmuAccount.buy_fee_tuple = (0, 10000)
    EmuAccount.sell_fee = 0
    EmuAccount.tax = 0

def set_account_etf_fee():
    EmuAccount.buy_fee = 25 / 100_000
    EmuAccount.buy_fee_tuple = (25, 100_000)
    EmuAccount.sell_fee = 25 / 100_000
    EmuAccount.tax = 1 / 1_000

class EmuAccount(AbstractAccount):
    @property
    def entrust_items(self):
        return None

    @property
    def share_items(self):
        return None

    def cancel_order(self, enetrust_id, code, way: EntrustWay):
        pass

    @property
    def available(self):
        return None

    # <editor-fold desc="Description">
    buy_fee = None
    buy_fee_tuple = None
    sell_fee = None
    tax = None

    # </editor-fold>

    def __init__(self, balance, day):
        self.balance = float(balance)
        self._total_asset = None

        self.stock2amount = {}
        self.non_sell_stocks2amount = {}
        self.day = day
        self.trade_times = 0
        set_account_etf_fee()

    def copy_for_day(self, day):
        ea = EmuAccount(self.balance, day)
        ea.stock2amount = copy.deepcopy(self.stock2amount)
        # Do NOT copy self.non_sell_stocks2amount = {}
        return ea

    def buy_stock(self, code, price, amount, entrust_type=None):
        self.trade_times += 1
        assert amount % 100 == 0, 'Not proper amount'
        need_money = round(price * amount * (1 + self.buy_fee), 3)
        assert self.balance >= need_money
        self.balance -= need_money
        self.balance = round(self.balance, 3)
        self.stock2amount[code] = self.stock2amount.get(code, 0) + amount
        self.non_sell_stocks2amount[code] = self.non_sell_stocks2amount.get(code, 0) + amount
        return self

    @property
    def available(self):
        return self.balance

    def sell_stock(self, code, price, amount, entrust_type=None):
        assert self.stock2amount.get(code, 0) >= amount
        sell_money = round(price * amount * (1 - self.sell_fee), 3)
        if code not in etf_stdcode2name and not code.startswith('i'):
            # print('not in etf code list')
            sell_money = round(sell_money * (1 - self.tax), 3)
        self.balance += sell_money
        self.balance = round(self.balance, 3)
        self.stock2amount[code] = self.stock2amount[code] - amount
        if self.stock2amount[code] == 0:
            del self.stock2amount[code]
        self.non_sell_stocks2amount[code] = self.non_sell_stocks2amount.get(code, 0) - amount

    def buy_at_most(self, code, price, entrust_type=None):
        amount = self.balance * self.buy_fee_tuple[1] // \
                 ((self.buy_fee_tuple[1] + self.buy_fee_tuple[0]) * price * 100)
        amount = 100 * int(amount)
        return self.buy_stock(code, price, amount)

    def sell_at_most(self, code, price, entrust_type=None):
        if code in self.stock2amount:
            self.sell_stock(code, price, self.stock2amount[code])

    def calc_total_asset(self):
        try:
            self._total_asset = self.balance
            for stock, amount in self.stock2amount.items():
                self._total_asset += gdata_pv.open(stock, self.day) * amount
            return self._total_asset
        except KeyError:
            return None

    def __repr__(self):
        asset = -1.0 if self._total_asset is None else self._total_asset
        return f'TotalAssert:{asset: <12.12} Balance:{self.balance:<12} Stocks:{self.stock2amount}'


class EmuDayAccounts:
    def __init__(self, date_range):
        self.date_range = date_range
        self.day2index = dict(zip(date_range, range(len(date_range))))
        self.accounts = [None] * len(date_range)  # type: List[EmuAccount]

    def account_of(self, day):
        index = self.day2index[day]
        if not self.accounts[index]:
            self.accounts[index] = self.accounts[index - 1].copy_for_day(day)
            self.accounts[index].day = day
        return self.accounts[self.day2index[day]]

    @property
    def init_account(self):
        return self.accounts[0]

    @init_account.setter
    def init_account(self, value):
        self.accounts[0] = value

        # <editor-fold desc="Description">


def test_copy_for_new_day():
    acc = EmuAccount(1000, 1000)
    acc.non_sell_stocks = {1: 2}
    acc_new = acc.copy_for_day('2011-01-05')
    assert not acc_new.non_sell_stocks2amount


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
    ea = EmuAccount(1.2, None)
    ea.stock2amount = {'510900': 100000}
    ea.sell_stock('510900', 1, 100000)
    assert ea.balance == 99975


def test_sell_stock():
    ea = EmuAccount(1, '1900-01-01')
    ea.stock2amount = {'000001': 100000}
    ea.sell_stock('000001', 1, 100000)
    assert ea.balance == 99875.025


def test_buy_all():
    ea = EmuAccount(1, '1900-01-01')
    ea.balance = 100025
    ea.buy_at_most('510900', 1)
    assert_equal(ea.balance, 0)
    assert_equal(ea.stock2amount['510900'], 100000)
    assert_equal(ea.non_sell_stocks2amount, {'510900': 100000})

    # </editor-fold>
