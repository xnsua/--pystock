from common import helper as hp, dt
from trading.trade_helper import StockTimeConstant


def find_stage(time_):
    for kv in StockTimeConstant.trade_stage_dict:
        begin, end = StockTimeConstant.trade_stage_dict[kv]
        if begin <= time_ < end:
            return kv
    raise Exception(f'Cannot find time stage for time {time_}')


def is_in_expanded_stage(time_, stage, time_delta_before, time_delta_after):
    dt_ = dt.datetime.combine(hp.dt_today(), time_)
    t1, t2 = StockTimeConstant.trade_stage_dict[stage]
    dt1 = dt.datetime.combine(hp.dt_today(), t1)
    dt2 = dt.datetime.combine(hp.dt_today(), t2)
    dt1a = dt1 - time_delta_before
    dt2a = dt2 + time_delta_after
    # noinspection PyTypeChecker
    val = dt1a <= dt_ <= dt2a
    return val


print(is_in_expanded_stage(dt.time(9, 29, 39), StockTimeConstant.trade1, dt.timedelta(0, 30),
                           dt.timedelta(0, 30)))
