from trading_emulation.trade_with_fee import EtfTrade


class EmuAccount:
    emu_trade = EtfTrade()

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
        return amount
