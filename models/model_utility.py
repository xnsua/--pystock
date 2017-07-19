from common_stock.trade_day import gtrade_day
from stock_data_updater.data_provider import DataProvider


def calc_date_range(codes, dp: DataProvider):
    first_day = min(dp.ddr(code).first_day() for code in codes)
    last_day = min(dp.ddr(code).last_day() for code in codes)
    return gtrade_day.close_range_list(first_day, last_day)


def fill_with_previous_value(arr, value):
    import numpy as np
    nparr = np.asarray(arr)
    prev = np.arange(len(nparr))
    prev[np.equal(nparr, value)] = 0
    prev = np.maximum.accumulate(prev)
    return nparr[prev]

