from common.helper import ndays_ago
from common.my_old.cache_database import cache_db
from common.simple_retry import SimpleRetry
from data_manager.stock_querier import w163_api


def query_etf_info(etf_code):
    key = 'key_etf_' + etf_code
    val = cache_db.query_dict(key, ndays_ago(7))
    if val: return val

    retrier = SimpleRetry(max_retry_times=2, wait_base_time=3)
    info = retrier(w163_api.wget_etf_info)(etf_code)
    cache_db.update(key, str(info))
    return info
