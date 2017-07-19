import math

import numpy
import numpy as np

from common.algorithm import calc_drop_percentage
from common.data_structures.geometry import Point
from common.helper import dt_date_from_str
from common.scipy_helper import pdSr
from common_stock.trade_day import gtrade_day


class MddInfo:
    def __init__(self, mdd, left_point, right_point):
        self.mdd = mdd
        self.left_point = left_point  # type: Point
        self.right_point = right_point  # type: Point


def calc_max_drawdown_pos_and_value(array_like):
    array_like = np.asarray(array_like)
    right = np.argmax(np.maximum.accumulate(array_like) - array_like)  # end of the period
    left = np.argmax(array_like[:right]) if right != 0 else 0  # start of period
    return left, right, array_like[right] / array_like[left]


def calc_max_drawdown_info(x_arr, y_arr):
    left, right, mdd = calc_max_drawdown_pos_and_value(y_arr)
    return MddInfo(mdd, Point(x_arr[left], y_arr[left]), Point(x_arr[right], y_arr[right]))


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
    name_to_value['mdd_info'] = calc_max_drawdown_pos_and_value(x, y)
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
              'base_drop_percentage': base_drop_percentage}
    return result


def main():
    ll = [1, 1, 1.1, 0.9, 0.8, 0.7, 3, 3]
    import datetime
    s_time = datetime.datetime.now()
    result = calc_max_drawdown_pos_and_value(ll)
    print(datetime.datetime.now() - s_time)
    print(result)


if __name__ == '__main__':
    main()
