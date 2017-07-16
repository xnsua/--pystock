from common_stock.trade_day import gtrade_day
from stock_data_updater.data_provider import DataProvider


def calc_date_range(codes, dp: DataProvider):
    first_day = min(dp.ddr(code).first_day() for code in codes)
    last_day = min(dp.ddr(code).last_day() for code in codes)
    return gtrade_day.close_range_list(first_day, last_day)

def fill_none_with_privious(value):
    val = list(value)
    for i, item in enumerate(val):
        if item:
            break
    else:
        return val
    val[0:i] = val[i:i+1] * i
    for i, item in enumerate(val):
        if not item:
            val[i] = val[i-1]
    return val

