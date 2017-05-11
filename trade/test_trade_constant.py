import datetime

from trade.trade_constant import StockTimeConstant
from trade.trade_utility import find_stage

_stc = StockTimeConstant


def test_find_time():
    assert _stc.before_bid == find_stage(datetime.time(1, 1, 1))
    assert _stc.bid_stage1 == find_stage(datetime.time(9, 15, 0))
    assert _stc.bid_stage2 == find_stage(datetime.time(9, 24, 0))
    assert _stc.bid_over == find_stage(datetime.time(9, 28, 0))
    assert _stc.trade1 == find_stage(datetime.time(9, 35, 0))
    assert _stc.midnoon_break == find_stage(datetime.time(12, 0, 0))
    assert _stc.trade2 == find_stage(datetime.time(13, 3, 0))
    assert _stc.after_trade == find_stage(datetime.time(16, 3, 0))
