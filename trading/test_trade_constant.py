import datetime

from trading.trade_helper import ksti_
from trading.trade_utility import find_stage


def test_find_time():
    assert ksti_.before_bid == find_stage(datetime.time(1, 1, 1))
    assert ksti_.bid_stage1 == find_stage(datetime.time(9, 15, 0))
    assert ksti_.bid_stage2 == find_stage(datetime.time(9, 24, 0))
    assert ksti_.bid_over == find_stage(datetime.time(9, 28, 0))
    assert ksti_.trade1 == find_stage(datetime.time(9, 35, 0))
    assert ksti_.midnoon_break == find_stage(datetime.time(12, 0, 0))
    assert ksti_.trade2 == find_stage(datetime.time(13, 3, 0))
    assert ksti_.after_trade == find_stage(datetime.time(16, 3, 0))
