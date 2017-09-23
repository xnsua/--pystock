import datetime
import pathlib

from common.helper import n_days, n_seconds
from common.persistent_cache import create_persistent_cache

_cache_path = pathlib.Path(__file__).parent
stock_cache = create_persistent_cache(str(_cache_path / 'stock_cache.sqlite'))
stock_cache_one_sec = stock_cache(n_seconds(1))

stock_cache_one_day = stock_cache(n_days(1))
stock_cache_one_week = stock_cache(n_days(7))
stock_cache_one_month = stock_cache(n_days(30))

stock_cache_three_month = stock_cache(n_days(100))

stock_trade_over_cache = stock_cache(day_boundary=datetime.time(17, 0, 0), cache_days=1)
