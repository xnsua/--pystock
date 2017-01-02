class Config:
    def __init__(self):
        pass

    @property
    def database_path(self):
        return 'stock.db'

    @property
    def tax(self):
        return 1 / 1000

    @property
    def commission(self):
        return 2.5 / 10000


    @property
    def transfer_fee(self):
        raise NotImplemented()


class Constants:
    @property
    def oper_sell(self):
        return 'oper_sell'

    @property
    def oper_buy(self):
        return 'oper_buy'


constant = Constants()
config = Config()
