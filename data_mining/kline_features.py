import sys

import numpy
import numpy as np
import pandas as pd

from common.numpy_helper import np_shift
from common_stock.common_indicator import ArrayIndicator
from stock_data_manager.ddr_file_cache import read_ddr_fast


class KlineFeatures:
    @staticmethod
    def up_count_of_previous_days(arr):
        is_up = arr - np_shift(arr, 1, 0) > 0
        count = ArrayIndicator.consecutive_count_of_True(is_up)
        return np_shift(count, 1, 0)

    @staticmethod
    def down_count_of_previous_days(arr):
        is_up = arr - np_shift(arr, 1, 0) < 0
        count = ArrayIndicator.consecutive_count_of_True(is_up)
        return np_shift(count, 1, 0)

    @staticmethod
    def even_count_of_previous_days(arr):
        is_even = (arr == np_shift(arr, 1, 0))
        count = ArrayIndicator.consecutive_count_of_True(is_even)
        return np_shift(count, 1, 0)

    @staticmethod
    def is_up_inday(df):
        open_, close_ = df.open.values, df.close.values
        return open_ < close_

    @staticmethod
    def is_close_up(df):
        close_ = df.close.values
        close_pre = np_shift(close_,1,0)
        return close_ - close_pre > 0


    @staticmethod
    def day_compare_features(df):
        o, c, h, l = KlineFeatures.ochl_features(df)
        po = np_shift(o, 1, 0)
        pc = np_shift(c, 1, 0)
        ph = np_shift(h, 1, 0)
        pl = np_shift(l, 1, 0)

        hh = np.maximum(h, ph)
        ll = np.minimum(l, pl)
        rr = hh - ll + sys.float_info.epsilon

        f1 = (o - ll) / rr
        f2 = (c - ll) / rr
        f3 = (po - ll) / rr
        f4 = (pc - ll) / rr

        f5 = (h - ll) / rr
        f6 = (l - ll) / rr
        f7 = (ph - ll) / rr
        f8 = (pl - ll) / rr

        return f1, f2, f3, f4, f5, f6, f7, f8

    @staticmethod
    def jump_value(df):
        # Return 0, negative value, positive value
        high = df.high.values
        low = df.low.values
        prehigh = np_shift(high, 1, 0)
        prelow = np_shift(low, 1, 0)
        jump_up = (low - prehigh)
        jump_up[jump_up <= 0] = 0
        jump_down = (high - prelow)
        jump_down[jump_down >= 0] = 0
        return jump_up + jump_down

    @staticmethod
    def ochl_features(df):
        o, c, h, l = df.open.values, df.close.values, df.high.values, df.low.values
        return o, c, h, l

    @staticmethod
    def trend_features(df):
        pass

    @staticmethod
    def reverse_features(df):
        pass

    @staticmethod
    def trend_continuation_features(df):
        pass

    @staticmethod
    def support_features(df):
        pass


def extract_kline_pren_feature(df: pd.DataFrame, window):
    df = df.round(4)
    oarr, carr, harr, larr = [df[item].values for item in ['open', 'close', 'high', 'low']]
    trend_lens, slope = ArrayIndicator.trend_len_and_slope(carr, window)

    epsilon = np.finfo(float).eps

    is_up_in_day = oarr < carr
    is_close_up = (carr - (np_shift(carr, 1, fill_value=0))) > 0
    body_height = np.abs(carr - oarr) + epsilon
    total_height = harr - larr + epsilon

    body_top = numpy.maximum(oarr, carr)
    body_bottom = numpy.minimum(oarr, carr)
    high_shadow_height = harr - body_top + epsilon
    low_shadow_height = body_bottom - larr + epsilon

    body_top_shifts = []
    body_bottom_shifts = []
    open_shifts = []
    close_shifts = []
    body_height_shifts = []
    total_height_shifts = []
    high_shadow_height_shifts = []
    low_shadow_height_shifts = []

    for i in reversed(range(0, window // 2 + 1)):
        body_top_shifts.append(np_shift(body_top, i))
        body_bottom_shifts.append(np_shift(body_bottom, i))
        open_shifts.append(np_shift(oarr, i))
        close_shifts.append(np_shift(carr, i))
        body_height_shifts.append(np_shift(body_height, i))
        total_height_shifts.append(np_shift(total_height, i))
        high_shadow_height_shifts.append(np_shift(high_shadow_height, i))
        low_shadow_height_shifts.append(np_shift(low_shadow_height, i))

    body_height_per = []
    h_shadow_height_per = []
    l_shadow_height_per = []
    total_height_per = []
    open_pos_per = []
    close_pos_per = []

    for i in range(1, len(body_top_shifts)):
        body_height_per.append(body_height_shifts[i] / body_height_shifts[i - 1])
        h_shadow_height_per.append(high_shadow_height_shifts[i] / high_shadow_height_shifts[i - 1])
        l_shadow_height_per.append(low_shadow_height_shifts[i] / low_shadow_height_shifts[i - 1])
        total_height_per.append(total_height_shifts[i] / total_height_shifts[i - 1])
        open_pos_per.append(open_shifts[i] - open_shifts[i - 1] / body_height_shifts[i - 1])
        close_pos_per.append(close_shifts[i] - close_shifts[i - 1] / body_height_shifts[i - 1])

        # noinspection PyTypeChecker
        # train_data = list(zip( *open_pos_per, *close_pos_per))
        # import pandas as pd
        # result_df = pd.DataFrame()
        # result_df.open = open_pos_per[0]
        # result_df.open1 = open_pos_per[1]
        # result_df.close = close_pos_per[0]
        # result_df.close1 = close_pos_per[1]
        # todo
        # , *open_pos_per, *close_pos_per))
    features = np.asarray([*total_height_per, *body_height_per, *h_shadow_height_per,
                           *l_shadow_height_per, *open_pos_per, *close_pos_per, is_up_in_day,
                           trend_lens, slope])
    features = features.T

    features = features[window // 2:, :]

    labels = np_shift(is_close_up, -1)[window // 2:]
    return features, labels


def main():
    ddr = read_ddr_fast('510050.XSHG')

    df = ddr.df.tail(6)
    val = extract_kline_pren_feature(df, window=5)
    print(val)


if __name__ == '__main__':
    import datetime

    s_time = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - s_time)
