import concurrent
from concurrent import futures

from common.scipy_helper import pdDF
from stock_data_updater.classify import index2name
from stock_data_updater.data_provider import gdata_pv
from stock_data_updater.rq_data_proxy import grq_data
from trading_emulation.emu_model_bad import EmuModelBad
from trading_emulation.emu_model_runner import EmuModelRunner
from trading_emulation.emuaccount import set_account_none_fee


def run_for_code(stock, dropday):
    set_account_none_fee()
    model_bad = EmuModelBad([stock], dropday)
    # model_bad = EmuModelBad(['510900'], 1)
    emu_runner = EmuModelRunner(model_bad)
    ret = emu_runner.run_model()

    name = gdata_pv.name_of(stock, None)
    return [stock, name, dropday, *ret]


def run_bad_for_all_etf_non_fee():
    set_account_none_fee()
    ## index_list = list(etf_code2name.keys())
    index_list = ['510500', '510680', '159935', '510180', '159921', '159915', '159939', '510120',
                  '510270', '510420', '510430', '510190', '159911', '159902', '510290', '159906',
                  '159908', '159928', '510280', '510260', '159952', '510880', '512310']
    index_list = grq_data.all_index_code()
    print(index_list)
    return
    ##
    index_list = index_list[0:1]
    trade_day = [*[1] * len(index_list), *[2] * len(index_list)]
    print(len(index_list))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist = list(executor.map(run_for_code, index_list * 2, trade_day))
    df = pdDF(data=rlist,
              columns=['index', 'name', 'dropdays', 'oyield', 'yield', 'oyearyield', 'yearyield'])
    df = df.set_index('index')
    df.to_csv('~/ModelResult/bad_etf.csv', encoding='utf-8')
    return df


def run_bad_for_all_index_non_fee():
    set_account_none_fee()
    # index_list = ['i000001']
    index_list = list(map(lambda v: 'i' + v, index2name))
    trade_day = [*[1] * len(index_list), *[2] * len(index_list)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        rlist = list(executor.map(run_for_code, index_list * 2, trade_day))
    df = pdDF(data=rlist,
              columns=['index', 'name', 'dropdays', 'oyield', 'yield', 'oyearyield', 'yearyield'])
    df.to_csv('~/ModelResult/bad_index.csv')
    return df


def main():
    df = run_bad_for_all_etf_non_fee()
    # print(df)
    # df = run_bad_for_all_index_non_fee()
    # print(df)


if __name__ == '__main__':
    main()
