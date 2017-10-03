import numpy as np

from common_stock.old_things.trade_day import gtrade_day
from stock_data_manager.data_provider import DDRprovider


def calc_date_range(codes, dp: DDRprovider):
    first_day = min(dp.ddr_of(code).first_day() for code in codes)
    last_day = min(dp.ddr_of(code).last_day() for code in codes)
    return gtrade_day.close_range_list(first_day, last_day)


def fill_with_previous_value(arr, value):
    nparr = np.asarray(arr)
    prev = np.arange(len(nparr))
    prev[np.equal(nparr, value)] = 0
    # noinspection PyArgumentList
    prev = np.maximum.accumulate(prev)
    return nparr[prev]

