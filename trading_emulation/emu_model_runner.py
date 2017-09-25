import copy
import os
import pathlib
import pickle
from operator import attrgetter

import numpy
from stock_analyser.plot import LineAndStyle, plot_with_annotation, TextAnnotation

from common.helper import dt_now
from common_stock.py_dataframe import EmuRealTimeDataRepr
from common_stock.stock_analyser.stock_indicators import MddInfo, calc_max_drawdown_info
from common_stock.stock_analyser.stock_indicators import calc_max_drawdown_pos_and_value
from common_stock.stock_helper import dict_with_float_repr, calc_year_yield_arr
from common_stock.trade_day import gtrade_day
from models.abstract_model import AbstractModel
from models.model_utility import calc_date_range
from stock_data_updater.data_provider import ddr_pv
from trading_emulation.emu_model_bad import EmuModelBad
from trading_emulation.emu_trade_context import EmuContext
from trading_emulation.emuaccount import EmuAccount, EmuDayAccounts, set_account_none_fee
from trading_emulation.emuaccount import WinInfo


class EmuModelRunner:
    # noinspection PyTypeChecker
    def __init__(self, model: AbstractModel):
        self.context = EmuContext(None)
        self.model = model
        pass

    def run_model(self, init_money=10000, days=None):
        if not days:
            days = calc_date_range(self.model.codes, ddr_pv)
        self.model.init_model(self.context)

        init_account = EmuAccount(init_money, days[0])
        day_accounts = EmuDayAccounts(days)
        day_accounts.init_account = init_account

        rdr = EmuRealTimeDataRepr()
        for date in days:
            rdr.day = date
            self.context.account = day_accounts.account_of(date)
            self.context.datetime = gtrade_day.int_to_date(date)
            self.model.on_bid_over(self.context, rdr)
            self.model.handle_bar(self.context, rdr)
            self.model.on_trade_over(self.context, rdr)
        return day_accounts


class AnalyseResult:
    def __init__(self, model, day_accounts: EmuDayAccounts, yield_, year_yield, normal_year_yield,
                 mdd_info, buy_count, max_lose, max_win, win_cnt_percentage, days, hold_days,
                 bench_data, bench_year_yield, bench_yield, bench_mdd_info,
                 additional_param_dict=None):
        self.win_cnt_percentage = win_cnt_percentage
        self.model = model
        self.day_accounts = day_accounts
        self.bench_data = bench_data
        self.yield_ = yield_
        self.year_yield = year_yield
        self.normal_year_yield = normal_year_yield
        self.mdd_info = mdd_info  # type: MddInfo

        self.buy_count = buy_count

        self.max_lose = max_lose  # type: WinInfo
        self.max_win = max_win  # type: WinInfo

        self.days = days
        self.hold_days = hold_days
        self.trade_day_cnt = sum(
            item.win_info.day_count for item in self.day_accounts.accounts if item.win_info)

        self.bench_yield = bench_yield
        self.bench_year_yield = bench_year_yield
        self.bench_mdd_info = bench_mdd_info  # type: MddInfo
        self.additional_param = additional_param_dict

    def __repr__(self):
        other = copy.copy(self)
        del other.model
        del other.day_accounts
        del other.bench_data
        other.days = [other.days[0], other.days[1]]
        return dict_with_float_repr(other.__dict__)


def analyse_emu_result(model, day_accounts: EmuDayAccounts):
    days = day_accounts.days
    day_asset_arr = numpy.asarray(day_accounts.total_assets)


    buy_count = sum([account.buy_count for account in day_accounts.accounts])

    wininfos = [account.win_info for account in day_accounts.accounts]
    valid_wininfo = [item for item in wininfos if item]
    max_win = max(valid_wininfo, key=attrgetter('win_percentage'))
    max_lose = min(valid_wininfo, key=attrgetter('win_percentage'))
    win_cnt_percentage = sum(item.win_percentage > 0 for item in valid_wininfo) / len(
        valid_wininfo)

    years = len(day_accounts.days) / 245
    hold_days = sum(bool(account.stock_to_share) for account in day_accounts.accounts)

    yield_ = day_asset_arr[-1] / day_asset_arr[1]
    year_yield = yield_ ** (1 / years)
    normal_year_yield = yield_ ** (245 / hold_days if hold_days >= 1 else 1)
    mdd_info = calc_max_drawdown_info(days, day_asset_arr)

    bench_data = model.model_bench()
    bench_data = bench_data[days]
    bench_vals = list(bench_data)
    bench_yield = bench_vals[-1] / bench_vals[0]
    bench_year_yield = bench_yield ** (245 / len(days))
    bench_mdd_info = calc_max_drawdown_info(bench_data.index.values, bench_data.values)

    return AnalyseResult(model=model, day_accounts=day_accounts, days=days,
                         yield_=yield_, year_yield=year_yield,
                         normal_year_yield=normal_year_yield, mdd_info=mdd_info,
                         buy_count=buy_count,
                         max_win=max_win, max_lose=max_lose,
                         win_cnt_percentage=win_cnt_percentage,
                         hold_days=hold_days, bench_yield=bench_yield, bench_data=bench_vals,
                         bench_year_yield=bench_year_yield, bench_mdd_info=bench_mdd_info)


def plot_analyse_result(ana_result: AnalyseResult, show_figure=True, figure_filename=None):
    if not show_figure and not figure_filename:
        return
    yvals = [item.total_asset for item in ana_result.day_accounts.accounts]
    xvals = [gtrade_day.int_to_date(item) for item in ana_result.days]
    yield_arr = calc_year_yield_arr(yvals)
    bench_vals = ana_result.bench_data
    mdd_pos1, mdd_pos2, mdd = calc_max_drawdown_pos_and_value(yvals)
    mdd_xs = [xvals[mdd_pos1], xvals[mdd_pos2]]
    mdd_ys = [yvals[mdd_pos1], yvals[mdd_pos2]]

    lines = [
        LineAndStyle(xvals, yvals, 'b', alpha=1, label='Value', show_value_in_annotaion=True),
        LineAndStyle(xvals, bench_vals, 'k', alpha=0.3, label='Base',
                     show_value_in_annotaion=True, bench_vals=yvals),
        LineAndStyle(mdd_xs, mdd_ys, 'y', alpha=0.9),
        LineAndStyle(xvals, yield_arr, 'm', alpha=0.2, bench_vals=yvals)
    ]

    def percentage_formatter(key, val):
        return f"{key}: {val:.1%}".replace('%', ' %')

    line1annotations = [
        TextAnnotation('  YIELD', ana_result.yield_, 1, 'b', formatter=percentage_formatter),
        TextAnnotation(' Y_YIELD', ana_result.normal_year_yield, 1, 'b',
                       formatter=percentage_formatter),
        TextAnnotation('MDD:', mdd, 1, 'b', formatter=percentage_formatter),
    ]
    line2annotations = [
        # Hide this
        TextAnnotation('B_YIELD', ana_result.bench_yield, 1, 'k', formatter=percentage_formatter),
        TextAnnotation('BY_YIELD', ana_result.bench_year_yield, 1, 'k',
                       formatter=percentage_formatter),
        TextAnnotation.empty_annotation(),
    ]
    line3annotations = [
        # Hide this
        TextAnnotation('WinCntPer', ana_result.win_cnt_percentage, color='k',
                       formatter=percentage_formatter),
        TextAnnotation('  EFFECT', ana_result.normal_year_yield / ana_result.bench_year_yield, 1,
                       'r',
                       formatter=percentage_formatter),
    ]

    rline1annotations = [
        TextAnnotation('BUY_CNT', ana_result.buy_count),
        TextAnnotation('MaxWin', ana_result.max_win.win_percentage,
                       formatter=percentage_formatter),
        TextAnnotation('Days', len(ana_result.days))
    ]
    rline2annotations = [
        TextAnnotation.empty_annotation(),
        TextAnnotation('MaxLose', ana_result.max_lose.win_percentage,
                       formatter=percentage_formatter),
        TextAnnotation('TradeDays', ana_result.trade_day_cnt)
    ]
    plot_with_annotation(lines, [line1annotations, line2annotations, line3annotations],
                         [rline1annotations, rline2annotations],
                         show=show_figure, image_file_name=figure_filename)


def run_emu_for_single_code(days, model, show_figure):
    set_account_none_fee()
    emu_runner = EmuModelRunner(model)
    day_accounts = emu_runner.run_model(days=days)
    ana_result = analyse_emu_result(model, day_accounts)

    plpath = pathlib.Path(
        os.path.expanduser('~/ModelResult/emulation/') + model.__class__.__name__ + '/')
    plpath.mkdir(exist_ok=True, parents=True)
    filename = str(model.format_parameter() + dt_now().strftime('__%y%m%d-%H%M%S'))
    pickle_path = plpath / (filename + '.pickle')
    pickle_path.write_bytes(pickle.dumps(ana_result))

    pickle_text_path = plpath / (filename + '.txt')
    pickle_text_path.write_text(repr(ana_result))

    figure_filename = plpath / (filename + '.png')
    plot_analyse_result(ana_result, show_figure=show_figure, figure_filename=str(figure_filename))

    return ana_result


def main():
    ddr_pv.ddr_of('sh510050').df.to_csv('jqtt.csv')
    days = ddr_pv.ddr_of('sh510050').days[0:900]
    model_bad = EmuModelBad(['sh510050'], 2)
    # noinspection PyUnusedLocal
    ana_result = run_emu_for_single_code(days, model_bad, show_figure=True)

    # val = ([print(item.day, item.total_asset, item) for item in ana_result.day_accounts.accounts])
    # balance = [item.balance for item in ana_result.day_accounts.accounts]
    # print(balance)


if __name__ == '__main__':
    main()
