import ctypes

import numpy
import talib
from numpy.ctypeslib import ndpointer

from project_helper.config_module import ppath

"""
All memory is allocated in python. C++ DO NOT allocate any memory.
"""

path = str(ppath.project_root / 'cpp_functions' / 'algorithm.dll')
algorithm_dll = ctypes.cdll.LoadLibrary(path)


def cEMA(indata: numpy.array, alpha):
    assert alpha > 0
    func = algorithm_dll.EMA
    if not func.argtypes:
        func.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int64,
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_double]
        func.restype = ctypes.c_int64
    out_data = numpy.empty_like(indata)
    func(indata, indata.size, out_data, alpha)
    return out_data


cEMA(numpy.arange(1.0, 6, dtype=numpy.float64), 2)
cEMA(numpy.arange(1.0, 6, dtype=numpy.float64), 2)


def cSMA(indata: numpy.array, period):
    assert period > 0
    func = algorithm_dll.SMA
    if not func.argtypes:
        func.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int64,
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_int64]
        func.restype = ctypes.c_int64
    out_data = numpy.empty_like(indata)
    func(indata, indata.size, out_data, period)
    return out_data


def CalcEMACrossValue(fast, slow, dea, fast_period, slow_period):
    alpha_fast = 2 / (fast_period + 1)
    alpha_slow = 2 / (slow_period + 1)
    cross_value = (dea + alpha_fast * fast - alpha_slow * slow - fast + slow) / (
        alpha_fast - alpha_slow)
    return cross_value


def CalcDEACrossValue(fast, slow, dea, fast_period, slow_period, dea_period):
    dea = (1 - dea_period) / 2 *dea
    alpha_fast = 2 / (1 + fast_period)
    alpha_slow = 2 / (1 + slow_period)
    cross_value = (dea + alpha_fast * fast - alpha_slow * slow - fast + slow) / (
        alpha_fast - alpha_slow)
    return cross_value


def CalcSMACrossValue(arr_vals, fast_vals, slow_vals, diff_vals, dea_vals, calc_pos, fast_period,
                      slow_period, dea_period):
    i = calc_pos
    diff_expected = (dea_vals[i - 1] - diff_vals[i - dea_period] / dea_period) / (
        1 - 1 / dea_period)
    print('diff_expected:: \n', diff_expected, dea_vals[i - 1], diff_vals[i - dea_period],
          dea_period)
    cross_val = (
                    (diff_expected + slow_vals[i - 1] - fast_vals[
                        i - 1]) * fast_period * slow_period + \
                    slow_period * arr_vals[i - fast_period] - fast_period * arr_vals[
                        i - slow_period]) / (slow_period - fast_period)
    return cross_val


def cCalcEMACrossValues(fast_vals, slow_vals, dea_vals, fast_alpha, slow_alpha):
    func = algorithm_dll.CalcEMACrossValues
    if not func.argtypes:
        func.restype = ctypes.c_int64
        func.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_int64,
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_double,
                         ctypes.c_double]
    out_vals = numpy.empty_like(fast_vals)
    func(fast_vals, slow_vals, dea_vals, fast_vals.size, out_vals, fast_alpha, slow_alpha)
    return out_vals


def cCalcSMACrossValues(arr_vals, fast_vals, slow_vals, diff_vals, dea_vals, arr_len, fast_period,
                        slow_period, dea_period):
    # DLL_API int CalcSMACrossValues(double* arr_vals, double* fast_vals, double* slow_vals,
    #     double* diff_vals, double*dea_vals, double* out_vals, int64 arr_len,
    #     int64 fast_period, int64 slow_period, int64 dea_period);
    out_vals = numpy.empty_like(arr_vals)
    func = algorithm_dll.CalcSMACrossValues
    if not func.argtypes:
        func.restype = ctypes.c_int64
        func.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                         ctypes.c_int64,
                         ctypes.c_int64,
                         ctypes.c_int64,
                         ctypes.c_int64]
    func(arr_vals, fast_vals, slow_vals, diff_vals, dea_vals, out_vals, arr_len, fast_period,
         slow_period, dea_period)
    return out_vals


def tt():
    fast_period = 5
    slow_period = 10
    dea_period = 7
    arr = [item for item in range(1, 7)] + [item for item in range(5, 0, -1)] * 10
    arr = numpy.asarray(arr, dtype=numpy.float64)
    print(arr.size)

    fast_vals = talib.EMA(arr, fast_period)
    slow_vals = talib.EMA(arr, slow_period)
    # diff_vals = fast_vals - slow_vals
    # print('diff', diff_vals)
    # dea_vals = talib.EMA(diff_vals, dea_period)
    # hist_vals = diff_vals - dea_vals
    # print(hist_vals)
    macd_vals = talib.MACD(arr, 5, 10, 7)
    pos = 50
    print(macd_vals[2][pos])

    value = CalcEMACrossValue(fast_vals[pos - 1], slow_vals[pos - 1], macd_vals[1][pos - 1], 5, 10)
    arr[pos] = value
    macd_vals = talib.MACD(arr, 5, 10, 7)
    print(macd_vals[2][pos])

def tt_dea_cross():
    fast_period = 5
    slow_period = 10
    dea_period = 7
    arr = [item for item in range(1, 7)] + [item for item in range(5, 0, -1)] * 10
    arr = numpy.asarray(arr, dtype=numpy.float64)
    print(arr.size)

    fast_vals = talib.EMA(arr, fast_period)
    slow_vals = talib.EMA(arr, slow_period)
    diff_vals = fast_vals - slow_vals
    # print('diff', diff_vals)
    dea_vals = talib.EMA(diff_vals, dea_period)
    print(dea_vals)
    pos = 30
    cross_value = CalcDEACrossValue(fast_vals, slow_vals, dea_vals, fast_period, slow_period, dea_period)


def main():
    tt_dea_cross()


if __name__ == '__main__':
    main()
