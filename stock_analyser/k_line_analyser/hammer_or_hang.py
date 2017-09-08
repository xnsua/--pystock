import numpy
import talib

from common.helper import EnterExit
from common_stock.py_dataframe import DayDataRepr
from stock_data_updater.data_provider import gdp


@EnterExit(lambda: numpy.seterr(all='ignore'), lambda v: numpy.seterr(**v))
def calc_hammer_or_hang(ddr: DayDataRepr):
    numpy.seterr(all='ignore')
    open_ = numpy.asarray(ddr.opens)
    close = numpy.asarray(ddr.closes)
    high = numpy.asarray(ddr.highs)
    low = numpy.asarray(ddr.lows)
    days = numpy.asarray(ddr.days)
    body_height = close - open_
    body_height = numpy.absolute(body_height)
    body_height_moving_average = talib.SMA(body_height, timeperiod=40)
    body_height_filter = (body_height / body_height_moving_average) < 1.7

    low_shadow = numpy.minimum(open_, close) - low
    high_shadow = high - numpy.maximum(open_, close)
    low_shadow_filter = (low_shadow / body_height) > 2
    high_shadow_filter = (high_shadow / body_height) < 0.5

    filter_ = numpy.logical_and(low_shadow_filter, high_shadow_filter)
    filter_ = numpy.logical_and(body_height_filter, filter_)
    return days[filter_]


def is_hammer_or_hang(ddr: DayDataRepr, day):
    dayk = ddr.dayk_of(day)
    return dayk.low_shadow / dayk.body_height > 2 \
           and dayk.high_shadow / dayk.body_height < 0.2


def plot_hammer_or_hang(ddr: DayDataRepr):
    marker = [item for item in ddr.days
              if is_hammer_or_hang(ddr, item)]
    print(len(ddr.days))
    print(len(marker))
    print(marker)


def main():
    ddr = gdp.ddr_of('sh510900')
    # ddr = ddr.tail(200)
    # ------- Print run time --------------
    import datetime
    s_time = datetime.datetime.now()
    marker = calc_hammer_or_hang(ddr)
    print(datetime.datetime.now() - s_time)


if __name__ == '__main__':
    main()
