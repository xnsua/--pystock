from common.helper import dt_today, dt_day_delta
from common.simple_retry import SimpleRetry
from common_stock.stock_querier import w163_api
from common_stock.stock_shelve import stock_shelve

def query_etf_info(etf_code):
    # Result : {'scale': 8559000000.0}
    key = 'key_etf_' + etf_code
    val = stock_shelve.get(key, None)
    if val and dt_today() - val[0] < dt_day_delta(7):
        return val[1]
    else:
        retrier = SimpleRetry(max_retry_times=2, wait_base_time=3)
        info = retrier(w163_api.wget_etf_info)(etf_code)
        stock_shelve[key] = (dt_today(), info)
        return info
