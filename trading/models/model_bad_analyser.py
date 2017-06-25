from itertools import islice
from typing import List, Dict

from common.data_structures.py_dataframe import DayDataRepr
from common.scipy_helper import pdDF
from common_stock.trade_day import get_close_trade_date_range
from stock_data_updater.analyser.day_attr_analyser import calc_fill_day_attr
from stock_data_updater.stock_day_bar_manager import StockUpdater
from trading_emulation.emu_account import EmuAccount


class ModelBadAnalyser:
    def __init__(self, dfs: List[pdDF]):
        assert len(dfs) and len(dfs[0])
        self.ddr_list = [calc_fill_day_attr(DayDataRepr(df)) for df in dfs]
        # noinspection PyUnresolvedReferences
        self.code2ddr = {ddr.code: ddr for ddr in self.ddr_list}  # type: Dict[str, DayDataRepr]
        min_date = min(ddr.index[0] for ddr in self.ddr_list)
        max_date = max(ddr.index[-1] for ddr in self.ddr_list)
        self.daterange = get_close_trade_date_range(min_date, max_date)

        self.drop_day_cnt = 1
        self.accounts = [None] * len(self.daterange)  # type: List[EmuAccount]

    def run(self):
        self.accounts[0] = EmuAccount(balance=100000, total_assert=100000)
        for index, day in islice(enumerate(self.daterange), 1, None):
            cur_account = self.accounts[index - 1].copy_for_new_day()  # type: EmuAccount
            for stock, data in self.code2ddr.items():
                cur_ddr = self.code2ddr[stock]  # type: DayDataRepr
                if day not in cur_ddr.index:
                    continue
                if cur_ddr.get_drop_cnt(day) == self.drop_day_cnt:
                    cur_account.buy_all(stock, cur_ddr.get_open(day))

                    cur_account.calc_total_asset(
                        {stock: cur_ddr.get_close(day) for stock in cur_account.stock2amount}
                    )
                else:
                    for sell_stock, amount in cur_account.stock2amount.items():
                        price = self.code2ddr[sell_stock].get_open(day)
                        cur_account.sell_stock(sell_stock, price, amount)
                    cur_account.calc_total_asset(
                        {stock: cur_ddr.get_close(day) for stock in cur_account.stock2amount}
                    )

            self.accounts[index] = cur_account

def main():
    df = StockUpdater.read_etf_day_data('510900')
    print(len(df))
    import datetime
    s_time = datetime.datetime.now()
    tester = ModelBadAnalyser([df])
    tester.drop_day_cnt = 1
    tester.run()
    print(datetime.datetime.now() - s_time)
    print(tester.accounts[-1])


if __name__ == '__main__':
    main()
