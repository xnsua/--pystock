import math

import numpy
import numpy as np

from common.algorithm import calc_drop_percentage, calc_rise_percentage
from common.helper import dt_date_from_str
from common.scipy_helper import pdSr
from common_stock.trade_day import gtrade_day


def calc_max_drawdown_infos(xval: np.array, yval: np.array):
    xval = np.array(xval)
    yval = np.array(yval)
    # noinspection PyArgumentList
    right = np.argmax(np.maximum.accumulate(yval) - yval)  # end of the period
    left = np.argmax(yval[:right]) if right != 0 else 0  # start of period

    vals2 = yval[right + 1:]
    # From begin of max drawdown to end of lose
    # noinspection PyTypeChecker
    for i, val in enumerate(vals2):
        if val and not np.isnan(val) is not  val > yval[left]:
            drawdown_duration_end = i + right
            break
    else:
        drawdown_duration_end = len(yval) - 1
    mdd = (yval[left] - yval[right]) / yval[left]
    return mdd, ((xval[left], yval[left]),
                 (xval[right], yval[right]),
                 (xval[drawdown_duration_end], yval[drawdown_duration_end]))


def calc_yield_dropdown(x, y):
    if isinstance(x[0], str):
        x = [dt_date_from_str(item) for item in x]
    if isinstance(x[0], int) or isinstance(x[0], numpy.int64):
        x = [gtrade_day.int_to_date(item) for item in x]
    name_to_value = {}
    front_date = x[0]
    back_date = x[-1]
    year_len = ((back_date - front_date).days + 1) / 365
    yield_ = (y[-1] - y[0]) / y[0]
    name_to_value['yield_'] = yield_
    name_to_value['year_yield'] = pow((1 + yield_), 1 / year_len) - 1
    name_to_value['mdd_info'] = calc_max_drawdown_infos(x, y)
    return name_to_value


def calc_trend_indicator(vals: pdSr, base: pdSr):
    base = base[vals.index]
    l1 = list(vals)

    l2 = list(base)
    ratio = 1
    val1_ratio = 1
    for val1, val2 in zip(l1, l2):
        if not math.isnan(val1) and not math.isnan(val2):
            ratio = val1 / val2
            val1_ratio = val1
            break
    normal_base = (base * ratio)
    # noinspection PyTypeChecker
    df_ratio = vals / normal_base * val1_ratio
    base_drop = base.dropna()

    base_drop_percentage = calc_drop_percentage(base)
    drop_percentage = calc_drop_percentage(vals)
    result = {'values': vals,
              'base_values': base,
              'normal_base_values': normal_base,
              'ratios_values': df_ratio,
              'value_attr': calc_yield_dropdown(vals.index, vals.values),
              'base_attr': calc_yield_dropdown(base_drop.index, base_drop.values),
              'drop_percentage': drop_percentage,
              'base_drop_percentage':base_drop_percentage}
    return result


def main():
    result = calc_max_drawdown_infos(
        ['2001-01-01', '2001-01-02', '2001-01-03', '2001-01-04', '2001-01-05'],
        [1, 1, 1.1, 0.9, 0.8])
    print(result)


if __name__ == '__main__':
    main()
