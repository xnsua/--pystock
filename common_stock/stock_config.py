import datetime
import pathlib

from common.helper import dt_day_delta
from common.persistent_cache import create_persistent_cache

_cache_path = pathlib.Path(__file__).parent / 'stock_cache_data'
pathlib.Path(_cache_path).mkdir(exist_ok=True)
stock_cache = create_persistent_cache(str(_cache_path / 'stock_cache.sqlite'))
stock_cache_one_day = stock_cache(dt_day_delta(1))
stock_cache_one_month = stock_cache(dt_day_delta(30))
stock_cache_three_month = stock_cache(dt_day_delta(100))
stock_trade_over_cache = stock_cache(day_boundary=datetime.time(17, 0, 0), cache_days=1)
