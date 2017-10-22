from typing import List

import talib

from common.helper import iterable_extend, print_line_item
from stock_data_manager import stock_sector
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


class SingleStockEmu:
    @staticmethod
    def bs_open_open(code, time_period, day_len) -> List[SingleEmuAccount]:
        df = read_ddr_fast(code).df.tail(day_len)
        if len(df) < day_len / 2: return

        days = df.index.values
        o, c = df.open.values, df.close.values
        skip_days = time_period
        sma = talib.EMA(df.close.values, time_period)

        index_day = list(enumerate(days))[skip_days:]
        sday, eday = index_day[0], index_day[-1]
        yield_ = c[eday[0]] / c[sday[0]]
        acc = SingleEmuAccount(code, (sday[1], eday[1]), yield_)
        for index, day in index_day:
            if index <= skip_days: continue

            if sma[index - 1] < c[index - 1]:
                acc.buy(day, o[index])
            elif sma[index - 1] > c[index - 1]:
                acc.sell(day, o[index])
        acc.calc_addition_infos()
        return acc

class SpecificRunner:
    @staticmethod
    def emu_hs300_p2()->List[SingleEmuAccount]:
        codes = stock_sector.khs300_com
        accs = iterable_extend(SingleStockEmu.bs_open_open)(codes, 31, day_len=500)
        accs = list(filter(bool, accs))
        return accs


class Analyser:
    @classmethod
    def analyser1(cls):
        accs = SpecificRunner.emu_hs300_p2()
        for acc in accs:
            acc.plot()
        print_line_item(cls.gain_from_acc(accs))

    @staticmethod
    def gain_from_acc(accs):
        hold_yyields = [item.hold_yyield for item in accs]
        yyields = [item.yyield for item in accs]
        import numpy
        val = numpy.divide(hold_yyields, yyields)
        # plot_histogram(val)
        val = numpy.prod(val) ** (1 / len(val))
        return val


def main():
    Analyser.analyser1()
    pass


if __name__ == '__main__':
    main()
