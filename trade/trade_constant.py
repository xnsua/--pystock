import datetime

# Trade Module
ks_id_data_server = 'id_data_server'
ks_id_trade_loop = 'id_trade_loop'
ks_model_name = 'model_name'
ks_idm_buy_after_drop = 'idm_buy_after_drop'
ks_model_queue_dict = 'model_queue_dict'

ks_msg_set_monitor_stock = 'msg_set_monitor_stock'
ks_msg_push_monitor_stocks = 'msg_push_monitor_stocks'

ks_drop_days = 'drop_days'

# Stock constant

ks_open = 'open'
ks_close = 'close'
ks_low = 'low'
ks_hight = 'high'

ks_data = 'date'
ks_volumn = 'volumn'
ks_amount = 'amount'

ks_not_trade_day = 'not_trade_day'
ks_stage_entered = 'stage_entered'

ks_before_bid = 'before_day_trade'
ks_bid_stage1 = 'bid_stage1'
ks_bid_stage2 = 'bid_stage2'
ks_bid_over = 'bid_over'
ks_trade1 = 'trade1'
ks_midnoon_break = 'midnoon_break'
ks_trade2 = 'trade2'
ks_after_trade = 'after_day_trade'

k_before_bid_time = (datetime.time.min, datetime.time(9, 15, 0))
k_bid_stage1_time = (datetime.time(9, 15, 0), datetime.time(9, 20, 0))
k_bid_stage2_time = (datetime.time(9, 20, 0), datetime.time(9, 25, 0))
k_bid_over_time = (datetime.time(9, 25, 0), datetime.time(9, 30, 0))
k_trade1_time = (datetime.time(9, 30, 0), datetime.time(11, 30, 0))
k_midnoon_break_time = (datetime.time(11, 30, 0), datetime.time(13, 00, 0))
k_trade2_time = (datetime.time(13, 0, 0), datetime.time(15, 00, 0))
k_after_trade_time = (datetime.time(15, 0, 0), datetime.time.max)

ks_trade_stage_map = {ks_before_bid: k_before_bid_time,
                      ks_bid_stage1: k_bid_stage1_time,
                      ks_bid_stage2: k_bid_stage2_time,
                      ks_bid_over: k_bid_over_time,
                      ks_trade1: k_trade1_time,
                      ks_midnoon_break: k_midnoon_break_time,
                      ks_trade2: k_trade2_time,
                      ks_after_trade: k_after_trade_time}


def find_stage(time):
    for kv in ks_trade_stage_map:
        begin, end = ks_trade_stage_map[kv]
        if begin <= time < end:
            return kv
    raise Exception(f'Cannot find time stage for time {time}')


def test_find_time():
    assert ks_before_bid == find_stage(datetime.time(1, 1, 1))
    assert ks_bid_stage1 == find_stage(datetime.time(9, 15, 0))
    assert ks_bid_stage2 == find_stage(datetime.time(9, 24, 0))
    assert ks_bid_over == find_stage(datetime.time(9, 28, 0))
    assert ks_trade1 == find_stage(datetime.time(9, 35, 0))
    assert ks_midnoon_break == find_stage(datetime.time(12, 0, 0))
    assert ks_trade2 == find_stage(datetime.time(13, 3, 0))
    assert ks_after_trade == find_stage(datetime.time(16, 3, 0))


# Communication constant
ks_operation = 'operation'
ks_stock_code = 'stock_code'
ks_price = 'price'
ks_entrust_type = 'entrust_type'
ks_entrust_id = 'entrust_id'
ks_query_info_type = 'query_info_type'
ks_buy = 'buy'
ks_sell = 'sell'
ks_sell_or_cancel = 'sell_or_cancel'
ks_cancel_entrust = 'cancel_entrust'
ks_query = 'query'
ks_buy_or_sell = 'buy_or_sell'
ks_fixed_price = 'fixed_price'
ks_query_content = 'query_content'
ks_myshare = "myshare"
ks_dayentrust = "dayentrust"
ks_dayfinentrust = "dayfinentrust"
ks_hisentrust = "hisentrust"
ks_hisfinentrust = "hisfinentrust"
ks_moneymovement = "moneymovement"
ks_deliveryentrust = "deliveryentrust"


def main():
    test_find_time()


if __name__ == '__main__':
    main()
