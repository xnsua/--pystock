import numpy

from common_stock.day_data_representation import DayDataRepr
from common_stock.stock_indicators.stock_indicator import StockIndicator


def extract_turn_point_train_data(ddr:DayDataRepr, window):
    trend_lens, slope = StockIndicator.trend_len_and_slope(ddr.close_nparr)
    train_datas = []
    train_labels = []
    omc = ddr.open_nparr - ddr.close_nparr
    hml = ddr.high_nparr - ddr.low_nparr
    maxoc = numpy.maximum(ddr.open_nparr, ddr.close_nparr)
    minoc = numpy.minimum(ddr.open_nparr, ddr.close_nparr)
    # hshadow = ddr.high_nparr -


def main():
    pass


if __name__ == '__main__':
    main()
