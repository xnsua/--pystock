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
        return money / (1 + self.buy_stock()) / price


class EmuAccount:
    def __init__(self):
        self.balance = 0
        self.stocks = {}
        self.emu_trade = EmuTrade()

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
    def __init__(self, df: pdDF):
        self.drop_days = 1
        self.buy_time = 0
        self.df = df
        self.df_money = pdDF(index=df.index, data=[1] * len(df.index), columns=['balance'])

        self.account = EmuAccount()

    def run(self):
        openp = self.df.open
        close = self.df.close
        dates = self.df.index
        balance = self.df_money.balance
        for index, date in enumerate(dates):
            if index < self.drop_days: continue
            for i in range(index, index - self.drop_days, -1):
                if close[i] > close[i - 1]:
                    balance[i] = balance[i - 1]
                    break
            else:
                balance[i] =
                pass


def main():
    df = DayBar.read_etf_day_data('510900')
    df = df[['open', 'close']]
    df = df.iloc[0:100, :]
    tester = ModelBuyAfterDropTester(df)
    tester.drop_days = 1
    tester.run()


if __name__ == '__main__':
    main()
