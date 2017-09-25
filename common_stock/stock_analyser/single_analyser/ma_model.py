import talib

from common_stock.py_dataframe import DayDataRepr
from common_stock.stock_analyser.single_analyser.single_abc_model import SingleAbcModel


class MaModel(SingleAbcModel):
    def __init__(self, period, ddr, ma_func):
        self.period = period
        self.buy_sells = []
        self.ddr = ddr
        self.ma = ma_func(self.ddr.close_nparr, period)
        self.ma[0:period] = self.ddr.close_nparr[0:period]
        # for i in range(len(ddr.days)):
        #     print(ddr.days[i], self.ma[i])

    def buy_sell_price(self, index):
        if self.ddr.closes[index - 1] > self.ma[index - 1]:
            return self.ddr.opens[index]
        else:
            return -self.ddr.opens[index]

    def skip_len(self):
        return self.period

    def __repr__(self):
        return f'{{MaModel: period={self.period}}}'


# Use oscillator
class MaModel1(MaModel):
    def __init__(self, period, ddr: DayDataRepr, ma_func):
        super().__init__(period, ddr, ma_func)
        # osci = numpy.abs(ddr.high_nparr - ddr.low_nparr)
        # self.oscillator = ma_func(osci)
        self.skip_len = self.period + 5

    def buy_sell_price(self, index):
        # Using two days is effective for sh510050 sh510090
        len_ = 3
        if all(self.ddr.lows[index - len_:index] > self.ma[index - len_:index]):
            return self.ddr.opens[index]
        len_ = 3
        if all(self.ddr.lows[index - len_:index] < self.ma[index - len_:index]):
            return -self.ddr.opens[index]
        else:
            return 0

    def __repr__(self):
        return f'{{MaModel2: period={self.period}}}'


class MacdModel(MaModel):
    def __init__(self, period, ddr: DayDataRepr):
        self.ma = talib.MACD(ddr.close_nparr, *period)[2]
        self.period = period
        self.skip_len = sum(period) + 1
        self.ddr = ddr

    def buy_sell_price(self, index):
        if self.ma[index - 1] > 0:
            return self.ddr.opens[index]
        else:
            return -self.ddr.opens[index]

    def __repr__(self):
        return f'{{MacdModel: period={self.period}}}'
