from itertools import islice
from typing import List

import pandas

from common.scipy_helper import pdDF
from data_manager.stock_day_bar_manager import DayBar


class EmuTrade:
    _buy_fee = 2.5 / 10_000
    _sell_fee = 2.5 / 10_000
    _tax = 0

    def __init__(self):
        self.buy_fee = self._buy_fee
        self.sell_fee = self._sell_fee
        self.tax = self._tax

    def need_buy_money(self, stock_price, amount):
        return stock_price * amount * (1 + self.buy_fee)

    def obtain_sell_money(self, stock_price, amount):
        return stock_price * amount * (1 - self._sell_fee)

    def buy_stock(self, stock_price, amount, money):
        return money - stock_price * amount * (1 + self.buy_fee)

    def sell_stock(self, stock_price, amount, money):
        return money + stock_price * amount * (1 - self.sell_fee)

    def buy_all(self, price, money):
        return money / (1 + self.buy_fee) / price


class EmuAccount:
    def __init__(self):
        self.balance = 0
        self.stocks = {}
        self.emu_trade = EmuTrade()
        self.total_assert = 0

    def buy_stock(self, code, price, amount):
        balance = self.emu_trade.buy_stock(price, amount, self.balance)
        if balance > 0:
            self.balance = balance
            self.stocks[code] = self.stocks.get(code, 0) + amount
        else:
            raise Exception('Money not enough')

    def buy_all(self, code, price):
        amount = self.emu_trade.buy_all(price, self.balance)
        self.stocks[code] = self.stocks.get(code, 0) + amount
        self.balance = 0


class ModelBuyAfterDropTester:
    def __init__(self, dfs: List[pdDF]):
        assert len(dfs) and len(dfs[0])

        self.drop_days = 1
        self.dfs = dfs

        self.codes = [df.code[0] for df in self.dfs]
        self.longest_index = max([df.index for df in dfs], key=len)
        self.accounts = pandas.Series(index=self.longest_index)  # type: List[EmuAccount]
        self.i_open = dfs[0].columns.get_loc['open']
        self.i_close = dfs[0].columns.get_loc['close']

    def need_buy(self, df, date, drop_days):
        i_date = df.index.get_loc(date)
        if i_date > drop_days:
            for i in range(i_date - drop_days, i_date):
                if df.iat(i, self.i_open) > df.iat(i - 1, self.i_open):
                    return False
            else:
                return True

    def run(self):
        account = self.accounts
        for date in islice(self.longest_index, 1):
            for df in self.dfs:
                is_buy = self.need_buy(df, date, self.drop_days)
                if is_buy:
                    pass

        acc = EmuAccount()
        acc.balance = 1
        acc.stocks = []
        acc.total_assert = 1

        stock_code = self.codes[0]
        self.accounts[0] = acc

        # for index, date in enumerate(dates):
        #     if index < self.drop_days: continue
        #
        #     for i in range(index, index - self.drop_days, -1):
        #         The equality
        # if close[i] > close[i - 1]:
        #     self.accounts[i] = self.accounts[i - 1]
        #     break
        # else:
        #     acc = copy.deepcopy(self.accounts[i - 1])
        #     acc.buy_all(self.)
        #     pass


def main():
    df = DayBar.read_etf_day_data('510900')
    df = df[['open', 'close']]
    df = df.iloc[0:100, :]
    tester = ModelBuyAfterDropTester(df)
    tester.drop_days = 1
    tester.run()


if __name__ == '__main__':
    main()
