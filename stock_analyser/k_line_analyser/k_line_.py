from common_stock.py_dataframe import DayDataRepr


def is_hammer_or_hang(ddr:DayDataRepr, day):
    dayk = ddr.dayk_of(day)
    return dayk.low_shadow / dayk.body_height > 2 \
           and dayk.high_shadow / dayk.body_height < 0.2



