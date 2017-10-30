from typing import List

import talib

from common.helper import iterable_extend, print_line_item
from common_stock.stock_helper import stock_result_saver
from project_config.config_module import STOCK_ANALYSE_RESULT
from stock_data_manager import stock_sector
from stock_data_manager.ddr_file_cache import read_ddr_fast
from trading.emulation.single_emu_account import SingleEmuAccount


class SingleStockEmu:
    @staticmethod
    def bs_open_open(code, time_period, day_len) -> List[SingleEmuAccount]:
        df = read_ddr_fast(code).df.tail(day_len)
        assert len(df) > day_len / 2, 'data len is too small'

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
    def emu_hs300_p2() -> List[SingleEmuAccount]:
        # codes = stock_sector.khs300_com
        codes = ['510050.XSHG']
        accs = iterable_extend(SingleStockEmu.bs_open_open)(codes, 31, day_len=300)
        accs = list(filter(bool, accs))
        return accs

    @staticmethod
    def get_hsall_filepath():
        path = STOCK_ANALYSE_RESULT / 'moving_average'
        path.mkdir(exist_ok=True)
        return str(path / 'hsall.pickle')

    @staticmethod
    @stock_result_saver('moving_average/hsall.pickle')
    def emu_hs_all_sv() -> List[SingleEmuAccount]:
        codes = stock_sector.kcs_codes
        accs = iterable_extend(SingleStockEmu.bs_open_open)(codes, 31, day_len=500)
        accs = list(filter(bool, accs))
        return accs


class Analyser:
    @classmethod
    def analyser1(cls):
        accs = SpecificRunner.emu_hs300_p2()
        for trim_len in [0, 3, 5, 7]:
            for acc in accs:
                acc = acc.trim_hold_periods(trim_len, read_ddr_fast(acc.code).df.open)
                print(acc)
                acc.plot()
                print()
            print_line_item(cls.gain_from_acc(accs))

    @staticmethod
    def gain_from_acc(accs):
        hold_yyields = [item.hold_yyield for item in accs]
        yyields = [item.yyield for item in accs]
        import numpy
        val = numpy.divide(hold_yyields, yyields)
        val = numpy.prod(val) ** (1 / len(val))
        return val


def main():
    for trim_len in [0, 3, 5]:
        import datetime
        s_time = datetime.datetime.now()
        accs = SpecificRunner.emu_hs_all_sv()
        # accs = [item for item in accs if item.hold_yyield < 0.6]
        # numpy.random.shuffle(accs)
        # accs = [item for item in accs if item.code == '300099.XSHE']
        # for acc in accs:
        #     acc = acc.trim_hold_periods(trim_len, read_ddr_fast(acc.code).df.open)

        accs = [item.trim_hold_periods(trim_len, read_ddr_fast(item.code).df.open) for item in
                accs]
        # hold_len = []
        # for val in accs:
        #     hold_len.extend([item.hold_len for item in val.hold_periods])
        # plot_histogram(hold_len)

        # print('Time: ', datetime.datetime.now() - s_time)

        print('Gain:', Analyser.gain_from_acc(accs))
        pass


if __name__ == '__main__':
    main()
