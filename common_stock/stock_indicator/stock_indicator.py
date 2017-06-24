import numpy as np


def calc_max_drawdown_and_drawdown_end(xval, yval):
    # noinspection PyArgumentList
    right = np.argmax(np.maximum.accumulate(yval) - yval)  # end of the period
    left = np.argmax(yval[:right])  # start of period

    vals2 = yval[right + 1:]
    # From begin of max drawdown to end of lose
    # noinspection PyTypeChecker
    poses = np.flatnonzero(vals2 >= yval[left])
    if poses:
        drawdown_duration_end = poses[0] + right
    else:
        drawdown_duration_end = len(yval) - 1
    mdd = (yval[left] - yval[right]) / yval[left]
    return mdd, ((xval[left], yval[left]),
                 (xval[right], yval[right]),
                 (xval[drawdown_duration_end], yval[drawdown_duration_end]))


def calc_trend_indicator(x, y):
    name2value = {}
    front_date = x[0]
    back_date = x[-1]
    year_len = ((back_date - front_date).days + 1) / 365
    yield_ = (y[-1] - y[0]) / y[0]
    name2value['yield_'] = yield_
    name2value['year_yield'] = pow((1 + yield_), 1 / year_len) - 1
    name2value['mdd_info'] = calc_max_drawdown_and_drawdown_end(x, y)
    print(name2value)
    return name2value
