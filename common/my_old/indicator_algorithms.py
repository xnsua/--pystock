import numpy
import talib

from cpp_functions.c_algorithm import cSMA, cCalcSMACrossValues, cCalcEMACrossValues, cEMA


def sMACD(arr, fast_period, slow_period, dea_period):
    fast_vals = cSMA(arr, fast_period)
    slow_vals = cSMA(arr, slow_period)
    diff = fast_vals - slow_vals
    dea_vals = cSMA(diff, dea_period)
    hist = diff - dea_vals
    cross_vals = cCalcSMACrossValues(arr, fast_vals, slow_vals, diff, dea_vals, arr.size,
                                     fast_period, slow_period, dea_period)
    return fast_vals, slow_vals, diff, dea_vals, hist, cross_vals


def tt():
    nparr = numpy.sin(numpy.arange(1, 30, dtype=numpy.float64)) + 10
    val = eMACD(nparr, 3,5,4)
    print(val[-2])

    val = talib.MACD(nparr, 3,5,4)
    print(val[-1])


def eMACD(arr, fast_alpha, slow_alpha, dea_alpha):
    fast_vals = cEMA(arr, fast_alpha)
    slow_vals = cEMA(arr, slow_alpha)
    diff = fast_vals - slow_vals
    dea_vals = cEMA(diff, dea_alpha)
    hist = diff - dea_vals
    cross_vals = cCalcEMACrossValues(fast_vals, slow_vals, dea_vals, fast_alpha, slow_alpha)
    return fast_vals, slow_vals, diff, dea_vals, hist, cross_vals

def main():
    tt()


if __name__ == '__main__':
    main()

