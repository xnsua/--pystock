## Need Update
from common_stock import stock_cache_one_week


# @stock_cache_one_week
# def _code_to_name():
#     from stock_data_manager.rq_data_fetcher import rq_all_instruments
#     val1 = rq_all_instruments('LOF')
#     val2 = rq_all_instruments('ETF')
#     val3 = rq_all_instruments('CS')
#     d1 = dict(zip(val1.order_book_id, val1.symbol))
#     d2 = dict(zip(val2.order_book_id, val2.symbol))
#     d3 = dict(zip(val3.order_book_id, val3.symbol))
#     return {**d1, **d2, **d3}
#
#
# kcode_to_name = _code_to_name()


@stock_cache_one_week
def _etf_codes(type_):
    from stock_data_manager.rq_data_fetcher import rq_all_instruments
    val2 = rq_all_instruments(type_)
    d2 = list(val2.order_book_id)
    return d2


ketf_codes = _etf_codes('ETF')
klof_codes = _etf_codes('LOF')
kcs_codes = _etf_codes('CS')


@stock_cache_one_week
def index_components(index):
    from stock_data_manager.index_info import gindex_pv
    val = gindex_pv.components_of(index)
    return val

# rq data format ******.XSHG
ksz50_com = index_components('000016')
khs300_com = index_components('000300')
kzz500_com = index_components('000905')
