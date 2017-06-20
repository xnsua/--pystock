class EtfTrade:
    def __init__(self):
        self.buy_fee = 2.5 / 10_000
        self.sell_fee = 2.5 / 10_000

    def cost_buy_money(self, stock_price, amount):
        return stock_price * amount * (1 + self.buy_fee)

    def obtain_sell_money(self, stock_price, amount):
        return stock_price * amount * (1 - self.sell_fee)

    def buy_stock(self, stock_price, amount, money):
        return money - stock_price * amount * (1 + self.buy_fee)

    def sell_stock(self, stock_price, amount):
        return stock_price * amount * (1 - self.sell_fee)

    def buy_all(self, price, money):
        return money / (1 + self.buy_fee) / price

    def sell_all(self, price, amount):
        return price * amount * (1 - self.sell_fee)


def test():
    etf_trade = EtfTrade()

    val = etf_trade.cost_buy_money(1, 100000)
    assert round(val, 3) == 100000 + 25

    val = etf_trade.obtain_sell_money(1, 100000)
    assert round(val, 3) == 100000 - 25

    val = etf_trade.buy_stock(1, 100000, 100025)
    assert round(val, 3) == 0

    val = etf_trade.sell_stock(1, 100000)
    assert round(val, 3) == 100000 - 25

    val = etf_trade.buy_all(1, 100025)
    assert round(val, 3) == 100000

    val = etf_trade.sell_all(1, 100000)
    assert round(val, 3) == 100000 - 25
