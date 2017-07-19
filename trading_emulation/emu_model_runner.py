import copy
import os
import pathlib
import pickle
from operator import attrgetter

from common.helper import dt_now
from common.scipy_helper import pdSr
from common_stock.py_dataframe import EmuRealTimeDataRepr
from common_stock.stock_helper import dict_with_float_repr
from common_stock.trade_day import gtrade_day
from models.abstract_model import AbstractModel
from models.model_utility import calc_date_range, fill_with_previous_value
from stock_analyser.stock_indicators.stock_indicator import MddInfo
from stock_analyser.stock_indicators.stock_indicator import calc_max_drawdown_pos
from stock_data_updater.data_provider import gdp
from trading_emulation.emu_model_bad import EmuModelBad
from trading_emulation.emu_trade_context import EmuContext
from trading_emulation.emuaccount import EmuAccount, EmuDayAccounts, set_account_none_fee


class EmuModelRunner:
    # noinspection PyTypeChecker
    def __init__(self, model: AbstractModel):
        self.context = EmuContext(None)
        self.model = model
        pass

    def run_model(self, init_money=1000000, days=None):
        if not days:
            days = calc_date_range(self.model.codes, gdp)
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
    def __init__(self, model, day_accounts, day_assets, yield_, year_yield, normal_year_yield,
                 mdd_info, buy_count, max_lose, max_win, win_time_percenatage, days, hold_days,
                 bench_data, bench_year_yield, bench_yield, bench_mdd_info,
                 additional_param_dict=None):
        self.win_time_percenatage = win_time_percenatage
        self.model = model
        self.day_accounts = day_accounts
        self.day_asset = day_assets
        self.bench_data = bench_data
        self.yield_ = yield_
        self.year_yield = year_yield
        self.normal_year_yield = normal_year_yield
        self.mdd_info = mdd_info  # type: MddInfo

        self.buy_count = buy_count

        self.max_lose = max_lose
        self.max_win = max_win

        self.days = days
        self.hold_days = hold_days
        self.trade_days = len(day_accounts.accounts)

        self.bench_yield = bench_yield
        self.bench_year_yield = bench_year_yield
        self.bench_mdd_info = bench_mdd_info  # type: MddInfo
        self.additional_param = additional_param_dict

    def __repr__(self):
        new_dict = copy.deepcopy(self.__dict__)
        new_dict['date_range'] = [new_dict['date_range'][0], new_dict['date_range'][-1]]
        del new_dict['model']
        del new_dict['day_accounts']
        return dict_with_float_repr(new_dict, 3)


def analyse_emu_result(model, day_accounts: EmuDayAccounts):
    days = day_accounts.days

    day_assets = [account._calc_total_asset() for account in day_accounts.accounts]
    # The stock have no data on some day
    day_assets = fill_with_previous_value(day_assets, None)

    buy_count = sum([account.buy_count for account in day_accounts.accounts])

    wininfos = [account.win_info for account in day_accounts.accounts]

    valid_wininfo = [item for item in wininfos if item]
    max_win = max(valid_wininfo, key=attrgetter('win_percentage'))
    max_lose = min(valid_wininfo, key=attrgetter('win_percentage'))
    win_time_percentage = sum(item.win_percentage > 0 for item in valid_wininfo) / len(
        valid_wininfo)

    years = len(day_accounts.days) / 245
    hold_days = sum(bool(account.stock_to_share) for account in day_accounts.accounts)

    yield_ = day_assets[-1] / day_assets[1]
    year_yield = yield_ ** (1 / years)
    normal_year_yield = yield_ ** (245 / hold_days if hold_days >= 1 else 1)
    mdd_info = calc_max_drawdown_pos(days, day_assets)

    bench_data = model.model_bench()
    bench_data = bench_data[days]
    bench_vals = list(bench_data)
    bench_yield = bench_vals[-1] / bench_vals[0]
    bench_year_yield = bench_yield ** (245 / len(days))
    bench_mdd_info = calc_max_drawdown_pos(bench_data.index.values, bench_data.values)

    return AnalyseResult(model=model, day_accounts=day_accounts, days=days,
                         yield_=yield_, year_yield=year_yield,
                         normal_year_yield=normal_year_yield, mdd_info=mdd_info,
                         buy_count=buy_count,
                         max_win=max_win, max_lose=max_lose,
                         win_time_percenatage=win_time_percentage,
                         hold_days=hold_days, bench_yield=bench_yield, bench_data= bench_vals,
                         bench_year_yield=bench_year_yield, bench_mdd_info=bench_mdd_info)


def run_emu_for_single_code(stock, days, dropday, plot_figure, save_figure):
    set_account_none_fee()
    model_bad = EmuModelBad([stock], dropday)
    emu_runner = EmuModelRunner(model_bad)
    day_accounts = emu_runner.run_model(days=days)
    ana_result = analyse_emu_result(model_bad, day_accounts)

    plpath = pathlib.Path(
        os.path.expanduser('~/ModelResult/emulation/') + model_bad.__class__.__name__ + '/')
    plpath.mkdir(exist_ok=True, parents=True)
    filename = str(model_bad.format_parameter() + dt_now().strftime('__%y%m%d-%H%M%S'))
    pickle_path = plpath / (filename + '.pickle')
    pickle_path.write_bytes(pickle.dumps(ana_result))

    pickle_text_path = plpath / (filename + '.txt')
    pickle_text_path.write_text(repr(ana_result))

    plot_image_path = plpath / (filename + '.png')

    day_asset = [item._calc_total_asset() for item in day_accounts.accounts]
    days = day_accounts.days
    assert len(day_asset) == len(days)
    asset_series = pdSr(data=day_asset, index=days)

    return ana_result


def plot_analyse_result(ana_result: AnalyseResult):
    yvals = ana_result.day_asset
    xvals = [gtrade_day.int_to_date(item) for item in ana_result.days]
    bench_vals = ana_result.bench_data
    mdd_values = ana_result.md

    lines = [
        LineAndStyle(xvals, yvals, 'b', alpha=1, label='Value', show_value_in_annotaion=True),
        LineAndStyle(xvals, bench_vals, 'k', alpha=0.3, label='Base', show_value_in_annotaion=True),
        LineAndStyle(mdd_x, mdd_y, 'k', alpha=0.3)
    ]
    line1annotations = [
        TextAnnotation('Key1', 0.1234, 6, 'b', formatter=percentage_formatter),
        TextAnnotation('Key2', 0.1234, 6, 'b', formatter=percentage_formatter),
    ]
    plot_image_with_annotation(lines, [line1annotations, line1annotations], [line1annotations],
                               show=False, save_file_name='d:/tfile.png')


def main():
    gdp.ddr('sh510050').df.to_csv('jqt.csv')
    days = gdp.ddr('sh510050').days[0:100]
    ana_result = run_emu_for_single_code('sh510050', days, 2, plot_figure=True, save_figure=True)
    # balance = [item.balance for item in ana_result.day_accounts.accounts]
    # print(balance)


if __name__ == '__main__':
    main()
