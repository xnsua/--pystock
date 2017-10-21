from typing import List

import talib

from common.helper import iterable_extend
from common_stock import stock_cache_one_week
from stock_data_manager import stock_sector
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


def macd_emu_bs_open_open(code, fast, slow, signal, day_len) -> List[SingleEmuAccount]:
    df = read_ddr_fast(code).df.tail(day_len)
    if len(df) < day_len / 2: return
    days = df.index.values
    o, c = df.open.values, df.close.values
    skip_days = slow + signal + 1
    macd_vals = talib.MACD(df.close.values, fast, slow, signal)[2]

    index_day = list(enumerate(days))[skip_days:]
    sday, eday = index_day[0], index_day[-1]
    yield_ = c[eday[0]] / c[sday[0]]
    acc = SingleEmuAccount(code, (sday[1], eday[1]), yield_)
    for index, day in index_day:
        if index <= skip_days: continue

        if macd_vals[index - 1] > 0:
            acc.buy(day, o[index])
        elif macd_vals[index - 1] < 0:
            acc.sell(day, o[index])
    acc.calc_addition_infos()
    return acc

def multi_level_macd_emu_bs_open_open(code, fast, slow, signal, day_len) -> List[SingleEmuAccount]:
    df = read_ddr_fast(code).df.tail(day_len)
    if len(df) < day_len / 2: return
    days = df.index.values
    o, c = df.open.values, df.close.values
    skip_days = slow + signal + 1
    macd_vals = talib.MACD(df.close.values, fast, slow, signal)[2]

    index_day = list(enumerate(days))[skip_days:]
    sday, eday = index_day[0], index_day[-1]
    yield_ = c[eday[0]] / c[sday[0]]
    acc = SingleEmuAccount(code, (sday[1], eday[1]), yield_)
    for index, day in index_day:
        if index <= skip_days: continue

        if macd_vals[index - 1] > 0:
            acc.buy(day, o[index])
        elif macd_vals[index - 1] < 0:
            acc.sell(day, o[index])
    acc.calc_addition_infos()
    return acc

@stock_cache_one_week
def macd_emulation():
    codes = stock_sector.khs300_com
    accs = macd_emu_bs_open_open(codes, 12, 26, 9, 500)
    for item in accs: item.calc_addition_infos()
    return accs


# @stock_cache_one_week
def macd_emulation2():
    codes = stock_sector.kcs_codes
    accs = iterable_extend(macd_emu_bs_open_open)(codes, 13, 29, 11, 500)
    accs = list(filter(bool, accs))
    return accs


def macd_ana():
    import datetime
    s_time = datetime.datetime.now()
    accs = macd_emulation2()  # type: List[SingleEmuAccount]
    accs = list(filter(bool, accs))
    print(datetime.datetime.now() - s_time)

    hold_yyields = [item.hold_yyield for item in accs]
    yyields = [item.yyield for item in accs]
    import numpy
    val = numpy.divide(hold_yyields, yyields)
    # plot_histogram(val)
    val = numpy.prod(val) ** (1 / len(val))
    print(val)






def main():
    macd_ana()
    pass


if __name__ == '__main__':
    main()
