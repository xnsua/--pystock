from common.scipy_helper import pdDF
from trading_emulation.account import Account
from trading_emulation.data_providor import DataProvider
from trading_emulation.model_base import ModelBase


class EmuModelBad(ModelBase):
    def __init__(self, codes, date_range):
        self.codes = codes
        self.date_range = date_range

    def init(self, dp: DataProvider):
        super().init(dp)
        if not self.date_range:
            for code in codes:
                dp.

    def on_trading(self, day: str, acc: Account, rtdata: pdDF):
        super().on_trading(day, acc, rtdata)

    def on_bid_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    def on_trade_over(self, day: str, acc: Account, rtdata: pdDF):
        pass

    def name(self):
        return 'EmuModelBad'
