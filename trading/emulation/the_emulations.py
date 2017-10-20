from typing import List

import talib

from common_stock.common_indicator import ArrayIndicator
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


def support_line_emu(df, window_len):
    pass


def do_support_line_emus(codes, window_len):
    for code in codes:
        ddr = read_ddr_fast(code)
        df = ddr.df
        sl_high = ArrayIndicator.is_max_poses(df.high.values, window_len)
        sl_low = ArrayIndicator.is_min_poses(df.low.values, window_len)

        acc = SingleEmuAccount(code, ddr, 10000, 50)


def macd_emu_bs_open_open(codes, fast, slow, signal)->List[SingleEmuAccount]:
    # Use open price to buy and sell
    accs = []
    for code in codes:
        df = read_ddr_fast(code).df.tail(300)
        days = df.index.values
        o, c = df.open.values, df.close.values
        skip_days = slow + signal + 1
        macd_vals = talib.MACD(df.close.values, fast, slow, signal)[2]

        index_day = list(enumerate(days))[skip_days:]
        sday, eday = index_day[0], index_day[-1]
        yield_ = c[eday[0]]  / c[sday[0]]
        acc = SingleEmuAccount(code, (sday[1], eday[1]), yield_)
        accs.append(acc)

        for index, day in index_day:
            if index <= skip_days: continue

            if macd_vals[index - 1] > 0:
                acc.buy(day, o[index])
            elif macd_vals[index - 1] < 0:
                acc.sell(day, o[index])
    return accs


def main():
    accs = macd_emu_bs_open_open(['510050.XSHG'], 12, 26, 9)
    for item in accs:
        df = item.calc_addition_infos().df
        print(df)
        print(item)




if __name__ == '__main__':
    main()
