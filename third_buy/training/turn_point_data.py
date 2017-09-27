import numpy

from common.scipy_helper import pdSr
from common_stock.py_dataframe import DayDataRepr
from stock_data_updater.data_provider import ddr_pv


def calc_is_up_turn_point_arr(sr, window_len):
    assert not isinstance(sr, pdSr)
    sr = pdSr(sr)
    val_r = sr.rolling(window=window_len, center=True).min()
    predicate = (val_r == sr)
    return predicate


def calc_is_down_turn_point_arr(sr, window_len):
    assert not isinstance(sr, pdSr)
    sr = pdSr(sr)
    val_r = sr.rolling(window=window_len, center=True).max()
    predicate = (val_r == sr)
    return predicate

def k_feature_extrator(ddr:DayDataRepr, window_len):
    is_down = calc_is_down_turn_point_arr(ddr.close_nparr, window_len)
    is_up = calc_is_up_turn_point_arr(ddr.close_nparr, window_len)



def get_up_turn_train_data(ddr: DayDataRepr, window_len):
    margin_len = int(window_len / 2)
    train_data_1 = []
    is_up_turn = calc_is_up_turn_point_arr(ddr.close_nparr, window_len)
    # todo


def tfunc():
    ttarr = numpy.array([1, 2, 3, 4, 5, 3, 2, 4, 6])
    get_up_turn_train_data(ddr_pv.ddr_of('510900.XSHG', 100), window_len=5)

def main():
    tfunc()


if __name__ == '__main__':
    main()
