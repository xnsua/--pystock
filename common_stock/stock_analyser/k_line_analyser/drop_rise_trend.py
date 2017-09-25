from common.scipy_helper import pdSr
from common_stock.py_dataframe import DayDataRepr


class DropRiseTrendIndicator:
    def __init__(self, ddr:DayDataRepr):
        self.ddr = ddr
        self.day_to_index = ddr.day_to_index
        self.trend_rise_count_o = []
        self.trend_rise_count_c = []
        self.trend_rise_count_h = []
        self.trend_rise_count_l = []

    def _cal_counts(self):
        open_ = self.ddr.df.open  # type: pdSr
        rise = open_ - open_.shift(1)
        rise = rise < 0

