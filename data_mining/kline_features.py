import sys

import numpy as np

from common.numpy_helper import np_shift
from common_stock.common_indicator import ArrayIndicator
from stock_data_manager.ddr_file_cache import read_ddr_fast


class KlineFeatures:
    @staticmethod
    def up_count_of_previous_days(df):
        arr = df.close.values
        is_up = arr - np_shift(arr, 1, 0) > 0
        count = ArrayIndicator.consecutive_count_of_True(is_up)
        return np_shift(count, 1, 0)

    @staticmethod
    def down_count_of_previous_days(df):
        arr = df.close.values
        is_up = arr - np_shift(arr, 1, 0) < 0
        count = ArrayIndicator.consecutive_count_of_True(is_up)
        return np_shift(count, 1, 0)

    @staticmethod
    def even_count_of_previous_days(df):
        arr = df.close.values
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
        close_pre = np_shift(close_, 1, 0)
        return close_ - close_pre > 0

    @staticmethod
    def volume_percentage(df):
        volume = df.volume.values
        volume = volume / np.max(volume)
        return volume

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

    @classmethod
    def fg_day_compare_features_n(cls, n):
        """ fg is function generator """

        def func(df):
            val = cls.day_compare_features(df)
            return [np_shift(item, n, 0) for item in val]

        return func

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
    def _support_high_low_strength(df, window_len):
        is_max = ArrayIndicator.is_max_poses(df.high, window_len)
        is_min = ArrayIndicator.is_min_poses(df.low, window_len)

        pass







def main():
    ddr = read_ddr_fast('510050.XSHG')

    df = ddr.df.tail(6)
    print(KlineFeatures.volume_percentage(df))
    return
    val = extract_kline_pren_feature(df, window=5)
    print(val)


if __name__ == '__main__':
    import datetime

    s_time = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - s_time)
