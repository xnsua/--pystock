import copy
from itertools import islice
from typing import List

from common.scipy_helper import pdDF
from common_stock.trade_day import get_close_trade_date_range
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
    emu_trade = EmuTrade()

    def __init__(self, balance=0, total_assert=0):
        self.balance = balance
        self.stocks = {}

        self.total_assert = total_assert

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


def max_date_range(dfs):
    start_dates = []
    end_dates = []
    for df in dfs:
        if len(df.index) >= 2:
            start_dates.append(df.index[0])
            end_dates.append(df.index[1])
    begin_date = min(start_dates)
    end_date = max(end_dates)
    return begin_date, end_date

class ModelBuyAfterDropTester:
    def __init__(self, dfs: List[pdDF]):
        assert len(dfs) and len(dfs[0])

        self.i_open = 0
        self.i_close = 1
        self.df_map = {}
        for df in dfs:
            dfm = dict(zip(df.index, zip(df.open, df.close)))
            self.df_map[df.code[0]] = dfm
        self.l_daterange = get_close_trade_date_range(
            max_date_range(dfs)
        )

        self.drop_days = 1
        self.accounts = [None] * len(self.l_daterange)  # type: List[EmuAccount]

    def need_buy(self, df, date, drop_days):
        i_date = df.index.get_loc(date)
        if i_date > drop_days:
            for i in range(i_date - drop_days, i_date):
                if df.iat(i, self.i_open) > df.iat(i - 1, self.i_open):
                    return False
            else:
                return True
        else:
            return False

    def cal_day_attribute(self, data, day):


    def run(self):
        self.accounts[0] = EmuAccount(balance=1, total_assert=1)
        for index, day in islice(enumerate(self.l_daterange), 1, None):
            cur_account = copy.deepcopy(self.accounts[index - 1])
            for stock, data in self.df_map:
                if self.need_buy(data, day, self.drop_days):
                    cur_account.buy_all(stock, data[day][self.i_open])



def main():
    df = DayBar.read_etf_day_data('510900')
    df = df[['open', 'close']]
    df = df.iloc[0:100, :]
    tester = ModelBuyAfterDropTester(df)
    tester.drop_days = 1
    tester.run()


if __name__ == '__main__':
    main()
