def query_etf_info(etf_code):
    # toch
    key = 'key_etf_' + etf_code
    # val = cache_db.query_dict(key, ndays_ago(7))
    # if val: return val
    #
    # retrier = SimpleRetry(max_retry_times=2, wait_base_time=3)
    # info = retrier(w163_api.wget_etf_info)(etf_code)
    # cache_db.update(key, str(info))
    # return info
