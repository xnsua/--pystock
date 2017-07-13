from collections import OrderedDict
from typing import Dict

import tushare

from common_stock import stock_cache_three_month
from common_stock.stock_helper import to_stdcodes
from stock_data_updater.web_querier import sina_api


# @stock_cache_one_sec
@stock_cache_three_month
def get_stock_index_2_name():
    df = tushare.get_index()
    return OrderedDict(zip(to_stdcodes(df.code), df.name))


@stock_cache_three_month
def query_sz50s() -> Dict[str, str]:
    df = tushare.get_sz50s()
    code_dict = dict(zip(to_stdcodes(df.code), df.name))
    return code_dict


@stock_cache_three_month
def query_hs300s() -> Dict[str, str]:
    df2 = tushare.get_hs300s()
    code_dict = dict(zip(to_stdcodes(df2.code), df2.name))
    return code_dict


@stock_cache_three_month
def query_zz500s() -> Dict[str, str]:
    df3 = tushare.get_zz500s()
    code_dict = dict(zip(to_stdcodes(df3.code), df3.name))
    return code_dict


etf_sinacode_to_name = sina_api.get_etf_sina_symbols()
etf_stdcode_to_name = etf_sinacode_to_name

sz50_to_name = query_sz50s()
hs300_to_name = query_hs300s()
zz500_to_name = query_zz500s()

# code_to_name = {**etf_stdcode_to_name, **sz50_to_name, **hs300_to_name, **zz500_to_name}
# index_to_name = get_stock_index_2_name()
# index_to_name = {**index_to_name, **{'i' + key: val for key, val in index_to_name.items()}}

etf_with_amount = ['sh510900', 'sh510050', 'sh518880', 'sh511010', 'sh510300', 'sh510500',
                   'sz159915', 'sz159919', 'sh510180', 'sz159902', 'sz159934', 'sz159901',
                   'sh513050', 'sh510330', 'sh512660', 'sh510880', 'sz159920', 'sh512000',
                   'sh513100', 'sh510360', 'sh510510']
etf_t0 = ['sh510900', 'sh513030', 'sh513050', 'sh513100', 'sh513500',
          'sh513600', 'sh513660']
