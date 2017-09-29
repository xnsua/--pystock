from trading.abstract_context import AbstractContext


class EmuContext(AbstractContext):
    def __init__(self, account):
        super().__init__(account)

    def buy_stock(self, *args):
        return self.account.buy_stock(*args)

    def sell_stock(self, *args):
        return self.account.sell_stock(*args)

    def buy_all(self, *args):
        return self.account.buy_at_most(*args)
