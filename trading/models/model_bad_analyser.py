import copy
from itertools import islice
from typing import List, Dict

from common.data_structures.py_dataframe import DayDataRepr
from common.scipy_helper import pdDF
from common_stock.analyser.day_attr_analyser import calc_day_attr
from common_stock.trade_day import get_close_trade_date_range
from data_manager.stock_day_bar_manager import DayBar
from trading_emulation.emu_account import EmuAccount


class ModelBadAnalyser:
    def __init__(self, dfs: List[pdDF]):
        assert len(dfs) and len(dfs[0])
        self.ddr_list = [calc_day_attr(DayDataRepr(df)) for df in dfs]
        self.ddr_map = {ddr.code: ddr for ddr in self.ddr_list}  # type: Dict[str, DayDataRepr]
        min_date = min(ddr.index[0] for ddr in self.ddr_list)
        max_date = max(ddr.index[-1] for ddr in self.ddr_list)
        self.daterange = get_close_trade_date_range(min_date, max_date)

        self.drop_days = 1
        self.accounts = [None] * len(self.daterange)  # type: List[EmuAccount]

    def run(self):
        self.accounts[0] = EmuAccount(balance=1, total_assert=1)
        for index, day in islice(enumerate(self.l_daterange), 1, None):
            cur_account = copy.deepcopy(self.accounts[index - 1])
            for stock, data in self.df_map:
                cur_ddr = self.ddr_map[stock]  # type: DayDataRepr
                if cur_ddr.drop_cnt == self.drop_days:
                    amount = cur_account.buy_all(stock, cur_ddr.get_close(day))
                    cur_account.total_assert = cur_account.balance
                    for stock, amount in cur_account:
                        cur_account.total_assert += self.ddr_map[stock].get_close(day)
                self.accounts[index] = cur_account

def main():
    df = DayBar.read_etf_day_data('510900')
    df = df[['open', 'close']]
    df = df.iloc[0:100, :]

    tester = ModelBadAnalyser(df)
    tester.drop_days = 1
    tester.run()


if __name__ == '__main__':
    main()
