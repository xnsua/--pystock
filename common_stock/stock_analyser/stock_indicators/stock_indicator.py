
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




def main():
    pass


if __name__ == '__main__':
    main()
