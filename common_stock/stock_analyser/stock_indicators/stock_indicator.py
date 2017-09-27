import numpy

from common.scipy_helper import pdSr


class StockIndicator:
    @staticmethod
    def mdd_info(arr_like):
        arr = numpy.array(arr_like)
        right = numpy.argmax(numpy.maximum.accumulate(arr) - arr)  # end of the period
        left = numpy.argmax(arr[:right]) if right != 0 else 0  # start of period
        return left, right

    @staticmethod
    def min_poses(arr_like, window_len):
        pdsr = pdSr(arr_like)
        val_r = pdsr.rolling(window=window_len, center=True).min()
        predicate = (val_r == pdsr)
        return predicate.values

    @staticmethod
    def max_poses(arr_like, window_len):
        pdsr = pdSr(arr_like)
        val_r = pdsr.rolling(window=window_len, center=True).max()
        predicate = (val_r == pdsr)
        return predicate.values

    @staticmethod
    def trend_len_and_slope(arr_like, window_len):
        min_poses = StockIndicator.min_poses(arr_like, window_len)
        max_poses = StockIndicator.max_poses(arr_like, window_len)
        last_index = None
        trend_len = numpy.empty_like(arr_like, dtype=numpy.int64)
        slope = numpy.empty_like(arr_like, dtype=numpy.float64)
        # If last index is min value, make index minus
        for i in range(len(arr_like)):
            trend_len[i] = 0
            slope[i] = 0
            if min_poses[i]:
                last_index = i
                break
            elif max_poses[i]:
                last_index = -i
                break
        if last_index is None:
            last_index = len(arr_like) - 1
        trend_len[0] = 0
        slope[i] = 0
        for i in range(1, abs(last_index) + 1):
            trend_len[i] = i
            slope[i] = (arr_like[i] - arr_like[0]) / i - 0

        new_start = True
        for i in range(abs(last_index) + 1, len(arr_like)):
            if new_start:
                trend_len[i] = 1
                slope[i] = arr_like[i] - arr_like[i - 1]
                new_start = False
            else:
                abs_last_index = abs(last_index)
                if min_poses[i] and last_index < 0 or max_poses[i] and last_index > 0:
                    new_start = True
                    if min_poses[i]:
                        last_index = i
                    else:
                        last_index = -i
                trend_len[i] = trend_len[i - 1] + 1
                slope[i] = (arr_like[i] - arr_like[abs_last_index]) / (i - abs_last_index)
        return trend_len, slope


def main():
    # ------- Print run time --------------
    import datetime
    s_time = datetime.datetime.now()
    val = StockIndicator.trend_len_and_slope([0,0,0,0,0] , window_len=5)
    print(datetime.datetime.now() - s_time)


    print(val)
    pass


if __name__ == '__main__':
    main()
