from itertools import islice

from common.data_structures.py_dataframe import DayDataRepr
from common.scipy_helper import pdDF


def calc_day_attr(ddr: DayDataRepr):
    index = list(ddr.index)
    open_ = list(ddr.open)
    close = list(ddr.close)

    drop_cnt = [0] * len(index)
    rise_cnt = [0] * len(index)
    for i, day in islice(enumerate(index), 1, None):
        if close[i - 1] > open_[i - 1]:
            rise_cnt[i] = rise_cnt[i - 1] + 1
            drop_cnt[i] = 0
        elif close[i - 1] < open_[i - 1]:
            rise_cnt[i] = 0
            drop_cnt[i] = drop_cnt[i - 1] + 1
        else:
            rise_cnt[i] = rise_cnt[i - 1]
            drop_cnt[i] = drop_cnt[i - 1]

    ddr.rise_cnts, ddr.drop_cnts = rise_cnt, drop_cnt
    return ddr


def test_day_attr_analyser():
    open_ = [1] * 6
    close = [1.1] * 6
    close[2:4] = [0] * 2
    df = pdDF.from_items([('open', open_), ('close', close)])
    df = df.assign(code=['510900'] * 6)
    ddr = DayDataRepr(df)
    import datetime
    s_time = datetime.datetime.now()
    calc_day_attr(ddr)
    print(datetime.datetime.now() - s_time)
    assert ddr.rise_cnts == [0, 1, 2, 0, 0, 1]
    assert ddr.drop_cnts == [0, 0, 0, 1, 2, 0]
