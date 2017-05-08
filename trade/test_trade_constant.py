import datetime

from trade.trade_constant import ks_before_bid, find_stage, ks_bid_stage1, \
    ks_bid_stage2, ks_bid_over, ks_trade1, ks_midnoon_break, ks_trade2, \
    ks_after_trade


def test_find_time():
    assert ks_before_bid == find_stage(datetime.time(1, 1, 1))
    assert ks_bid_stage1 == find_stage(datetime.time(9, 15, 0))
    assert ks_bid_stage2 == find_stage(datetime.time(9, 24, 0))
    assert ks_bid_over == find_stage(datetime.time(9, 28, 0))
    assert ks_trade1 == find_stage(datetime.time(9, 35, 0))
    assert ks_midnoon_break == find_stage(datetime.time(12, 0, 0))
    assert ks_trade2 == find_stage(datetime.time(13, 3, 0))
    assert ks_after_trade == find_stage(datetime.time(16, 3, 0))
