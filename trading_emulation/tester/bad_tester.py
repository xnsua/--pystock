import concurrent
from concurrent import futures

from common.scipy_helper import pdDF
from stock_data_updater.classify import etf_with_amount
from stock_data_updater.data_provider import gdp
from stock_data_updater.index_info import gindex_pv
from trading_emulation.emu_model_bad import EmuModelBad
from trading_emulation.emu_model_runner import EmuModelRunner, analyse_emu_result
from trading_emulation.emuaccount import set_account_none_fee


def run_emu_for_single_code(stock, dropday, show_figure):
    set_account_none_fee()
    model_bad = EmuModelBad([stock], dropday)
    emu_runner = EmuModelRunner(model_bad)
    day_accounts = emu_runner.run_model()
    ana_result = analyse_emu_result(model_bad, day_accounts, show_figure=False)
    if show_figure:
        pass

    return ana_result


def run_bad_for_all_etf_non_fee():
    set_account_none_fee()
    etf_list = etf_with_amount
    # etf_list = etf_list[0:1]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist = list(executor.map(run_emu_for_single_code, etf_list, [1] * len(etf_list)))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist.extend(list(executor.map(run_emu_for_single_code, etf_list, [2] * len(etf_list))))
    data = [(item.stock, item.name, item.drop_days, item.yield_, item.yyield, item.base_yield,
             item.base_yyield) for item in rlist]
    df = pdDF(data=data,
              columns=['index', 'name', 'dropdays', 'base_yield', 'yield', 'base_yyield',
                       'yyield'])
    df = df.set_index('index')
    df.to_csv('~/ModelResult/bad_etf.csv', encoding='utf-8')
    return df


def run_bad_for_all_index_non_fee():
    set_account_none_fee()
    index_list = list(map(gdp.symbol_to_code, gindex_pv.main_index_symbol))
    # index_list = index_list[0:1]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist = list(executor.map(run_emu_for_single_code, index_list, [1] * len(index_list)))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist.extend(
            list(executor.map(run_emu_for_single_code, index_list, [2] * len(index_list))))
    data = [(item.stock, item.name, item.drop_days, item.base_yield, item.yield_,
             item.base_yyield, item.yyield)
            for item in rlist]
    df = pdDF(data=data,
              columns=['index', 'name', 'dropdays', 'base_yield', 'yield', 'base_yyield',
                       'yyield'])
    df = df.set_index('index')
    df.to_csv('~/ModelResult/bad_index.csv', encoding='utf-8')
    return df


def run_bad_for_codes(codes, drop_days, filename, multi_process=True, show_figure=False):
    set_account_none_fee()
    code_list = codes

    rlist = []
    for drop_day in drop_days:
        if multi_process:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                # noinspection PyArgumentList
                rlist.extend(
                    list(executor.map(run_emu_for_single_code, code_list,
                                      [drop_day] * len(code_list))),
                    [show_figure] * len(code_list))
        else:
            for code in code_list:
                rlist.append(run_emu_for_single_code(code, drop_day, show_figure))
    data = [(item.stock, item.name, item.drop_days, item.base_yield, item.yield_,
             item.base_yyield, item.yyield)
            for item in rlist]
    df = pdDF(data=data,
              columns=['index', 'name', 'dropdays', 'base_yield', 'yield', 'base_yyield',
                       'yyield'])
    df = df.set_index('index')
    df = df.assign(win=df.yyield > df.base_yyield)
    df.to_csv(f'~/ModelResult/Bad/{filename}.csv', encoding='utf-8')
    return df


def main():
    # index_list = list(map(gdata_pv.symbol_to_code, gindex_pv.main_index_symbol))
    # run_bad_for_codes(index_list, [1, 2, 3], 'main_indexes')

    # cons001 = gdata_pv.components_of('sh000001')
    # cons001 = [item for item in cons001 if not item.startswith('sh9')]
    # run_bad_for_codes(cons001, [1, 2], 'com000001')

    # cons016 = gdata_pv.components_of('sh000016')
    # cons016 = [item for item in cons016 if not item.startswith('sh9')]
    # run_bad_for_codes(cons016, [1, 2], 'cons016')

    # run_bad_for_codes(etf_with_amount, [1, 2], 'etf_with_amount', )

    val = run_bad_for_codes(['sz159919'], [2], 'single_test', show_figure=True,
                            multi_process=False)
    print(val)

    pass


if __name__ == '__main__':
    main()
