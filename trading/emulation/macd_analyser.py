from typing import List, Tuple

import talib

from common.helper import iterable_extend
from common_stock import stock_cache_one_week
from stock_data_manager import stock_sector
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


class SingleStockEmu:
    @staticmethod
    def bs_open_open(code, macd_param, day_len) -> List[SingleEmuAccount]:
        fast, slow, signal = macd_param
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


class SpecificRunner:
    @staticmethod
    def macd_emu_510050()->SingleEmuAccount:
        code = '510050.XSHG'
        accs = SingleStockEmu.bs_open_open(code, (12, 26, 9), day_len=500)
        return accs

    @staticmethod
    @stock_cache_one_week
    def macd_emu_hs300_p2():
        codes = stock_sector.khs300_com
        accs = iterable_extend(SingleStockEmu.bs_open_open)(codes, (13, 29, 11),
                                                            day_len=500)
        accs = list(filter(bool, accs))
        return accs

    @staticmethod
    @stock_cache_one_week
    def multi_level_emulations1() -> Tuple[List[SingleEmuAccount], List[SingleEmuAccount]]:
        codes = stock_sector.khs300_com
        accs1 = iterable_extend(SingleStockEmu.bs_open_open)(
            codes, (13, 29, 11), day_len=500)
        accs2 = iterable_extend(SingleStockEmu.bs_open_open)(
            codes, (27, 59, 23), day_len=600)

        return accs1, accs2


class Analyser:
    @staticmethod
    def multi_level_macd_ana1():
        accs1, accs2 = SpecificRunner.multi_level_emulations1()
        print('Gain1: ', Analyser.gain_from_acc(list(filter(bool, accs1))))
        print('Gain2: ', Analyser.gain_from_acc(list(filter(bool, accs2))))
        accs = [item1.overlap_other(item2) for item1, item2 in zip(accs1, accs2) if
                item1 and item2]
        print('Overlap Gain: ', Analyser.gain_from_acc(accs))

    @staticmethod
    def gain_from_acc(accs):
        import numpy
        val = numpy.prod([val.gain for val in accs]) ** (1 / len(accs))
        return val


def main():
    Analyser.multi_level_macd_ana1()
    # val = SpecificRunner.macd_emu_510050()
    # print_line_item(*[(item.buy_ts, item.sell_ts) for item in val.hold_periods])
    pass


if __name__ == '__main__':
    main()
