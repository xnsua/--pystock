import numpy

from common.scipy_helper import pdSr, npasarr


def max_peak_info(arr, window_len=5):
    arr_sr = pdSr(arr)
    arr_roll_max = arr_sr.rolling(window=window_len, center=True).max()
    is_max_arr = (arr_roll_max == arr_sr)
    return is_max_arr.values


def min_peak_info(arr, window_len=5):
    arr_sr = pdSr(arr)
    arr_roll_min = arr_sr.rolling(window=window_len, center=True).min()
    is_min_arr = (arr_roll_min == arr_sr)
    return is_min_arr.values


def calc_up_turn_points(arr):
    peak_info = min_peak_info(arr)
    where_peak = numpy.flatnonzero(peak_info)
    invalid_peak = []
    len_ = len(arr)
    for pos in where_peak:
        if 2 <= pos <= len_ - 3:
            if arr[pos - 1] >= arr[pos - 2] or arr[pos + 1] >= arr[pos + 2]:
                invalid_peak.append(pos)
    turn_points = numpy.setdiff1d(npasarr(where_peak), npasarr(invalid_peak))
    return turn_points

def

def main():
    arr = [5, 4, 3, 2, 1, 3, 3, 4]
    val = calc_up_turn_points(npasarr(arr))
    print(val)


if __name__ == '__main__':
    main()
