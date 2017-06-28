from common.scipy_helper import pdDF
from common_stock.trade_day import gtrade_day
from trading_emulation.account import Account
from trading_emulation.data_provider import DataProvider, gdata_provider
from trading_emulation.model_base import ModelBase


class EmuModelBad(ModelBase):
    def __init__(self, code, date_range, params):
        super().init(code, date_range, params)
        self.rise =
        self.

    def init(self, dp: DataProvider):


    def on_trading(self, day: str, acc: Account, rtdata: pdDF):
        super().on_trading(day, acc, rtdata)

    def on_bid_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    def on_trade_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    def on_result(self, operation):
        pass

    def name(self):
        return 'EmuModelBad'

def main():
    ebad = EmuModelBad(['510900'], None, None)
    ebad.init(gdata_provider)
    ldate = list(ebad.date_range)
    print(ldate[0], ldate[-1])



if __name__ == '__main__':
    main()

