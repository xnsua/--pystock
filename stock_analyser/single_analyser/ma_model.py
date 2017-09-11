import talib

from stock_analyser.single_analyser.single_abc_model import SingleAbcModel


class MaModel(SingleAbcModel):
    def __init__(self, period, ddr):
        self.period = period
        self.buy_sells = []
        self.ddr = ddr
        self.ma = talib.MA(self.ddr.close_nparr, period)

    def buy_sell_price(self, index):
        if self.ddr.closes[index-1] > self.ma[index-1]:
            return self.ddr.opens[index]
        else:
            return -self.ddr.opens[index]

    def skip_len(self):
        return self.period

    def __repr__(self):
        return f'{{MaModel: period={self.period}}}'


class EmaModel(MaModel):
    def __init__(self, period, ddr):
        super().__init__(period, ddr)
        self.ma = talib.EMA(self.ddr.close_nparr, period)
    def __repr__(self):
        return f'{{EmaModel: period={self.period}}}'
