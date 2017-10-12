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

ksample80 = ['300202.XSHE', '601766.XSHG', '000627.XSHE', '600383.XSHG', '000021.XSHE',
            '600418.XSHG', '002500.XSHE', '000025.XSHE', '002155.XSHE', '600993.XSHG',
            '002027.XSHE', '300055.XSHE', '001696.XSHE', '600525.XSHG', '600015.XSHG',
            '600729.XSHG', '600143.XSHG', '000488.XSHE', '600570.XSHG', '002123.XSHE',
            '600436.XSHG', '000008.XSHE', '002572.XSHE', '600917.XSHG', '600587.XSHG',
            '000587.XSHE', '002183.XSHE', '600872.XSHG', '600736.XSHG', '000997.XSHE',
             '002019.XSHE', '000725.XSHE', '000848.XSHE', '601928.XSHG', '002120.XSHE',
             '600737.XSHG', '000541.XSHE', '300376.XSHE', '002396.XSHE', '601872.XSHG',
             '600751.XSHG', '600643.XSHG', '002366.XSHE', '600028.XSHG', '300166.XSHE',
             '600809.XSHG', '002479.XSHE', '000157.XSHE', '600880.XSHG', '002342.XSHE',
             '600895.XSHG', '601777.XSHG', '601002.XSHG', '601939.XSHG', '000661.XSHE',
             '601163.XSHG', '600757.XSHG', '600122.XSHG', '000636.XSHE', '000009.XSHE',
             '600160.XSHG', '000540.XSHE', '002665.XSHE', '600466.XSHG', '000028.XSHE',
             '002385.XSHE', '601390.XSHG', '002344.XSHE', '002384.XSHE', '600435.XSHG',
             '603858.XSHG', '600750.XSHG', '002030.XSHE', '000738.XSHE', '603528.XSHG',
             '601608.XSHG', '002460.XSHE', '600151.XSHG', '000425.XSHE', '000761.XSHE']
