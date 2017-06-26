from typing import Dict

import tushare
from common_stock import stock_cache_three_month
from stock_data_updater.web_querier import sina_api


@stock_cache_three_month
def get_stock_index_list():
    df = tushare.get_index()
    return list(df.code)


@stock_cache_three_month
def query_sz50s() -> Dict[str, str]:
    df = tushare.get_sz50s()
    code_dict = dict(zip(df.code, df.name))
    return code_dict


@stock_cache_three_month
def query_hs300s() -> Dict[str, str]:
    df2 = tushare.get_hs300s()
    code_dict = dict(zip(df2.code, df2.name))
    return code_dict


@stock_cache_three_month
def query_zz500s() -> Dict[str, str]:
    df3 = tushare.get_zz500s()
    code_dict = dict(zip(df3.code, df3.name))
    return code_dict


all_etf_sinacode_list = sina_api.get_etf_sina_symbols()
all_etf_code_list = [val[2:] for val in all_etf_sinacode_list]

sz50m = query_sz50s()
hs300m = query_hs300s()
zz500m = query_zz500s()

all_stock_index_list = get_stock_index_list()

etf_with_amount = ['sh510900', 'sh510050', 'sh518880', 'sh511010', 'sh510300', 'sh510500',
                   'sz159915', 'sz159919', 'sh510180', 'sz159902', 'sz159934', 'sz159901',
                   'sh513050', 'sh510330', 'sh512660', 'sh510880', 'sz159920', 'sh512000',
                   'sh513100', 'sh510360', 'sh510510']
etf_t0 = ['sh510900', 'sh513030', 'sh513050', 'sh513100', 'sh513500',
          'sh513600', 'sh513660']
etf_sz50 = '510050'
etf_example = [etf_sz50, '510900']
