import datetime as dt

from common import helper as hp
from trade.trade_constant import StockTimeConstant


def find_stage(time_):
    for kv in StockTimeConstant.trade_stage_dict:
        begin, end = StockTimeConstant.trade_stage_dict[kv]
        if begin <= time_ < end:
            return kv
    raise Exception(f'Cannot find time stage for time {time_}')


def is_in_expanded_stage(time_, stage, time_delta=dt.timedelta()):
    t1, t2 = StockTimeConstant.trade_stage_dict[stage]
    dt1 = hp.to_datetime(t1)
    dt2 = hp.to_datetime(t2)
    dt1a = dt1 - time_delta
    dt2a = dt2 + time_delta
    # noinspection PyTypeChecker
    return dt1a <= hp.to_datetime(time_) <= dt2a
