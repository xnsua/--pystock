import datetime
import datetime as dt

import common.helper as hp

# <editor-fold desc="TradeModel">

ks_id_data_server = 'id_data_server'
ks_id_trade_manager = 'id_trade_manager'
ks_model_name = 'model_name'
ks_idm_buy_after_drop = 'idm_buy_after_drop'
ks_model_queue_dict = 'model_queue_dict'

ks_msg_set_monitor_stock = 'msg_set_monitor_stock'
ks_msg_push_realtime_stocks = 'msg_push_realtime_stocks'
ks_msg_wait_result_queue = 'msg_wait_result_queue'
ks_push_realtime_interval = 'push_realtime_interval'

ks_drop_days = 'drop_days'
ks_datetime_manager = 'datetime_manager'
# </editor-fold>

# <editor-fold desc="Stock Time Constant">
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

kd_trade_stage = {ks_before_bid: k_before_bid_time,
                  ks_bid_stage1: k_bid_stage1_time,
                  ks_bid_stage2: k_bid_stage2_time,
                  ks_bid_over: k_bid_over_time,
                  ks_trade1: k_trade1_time,
                  ks_midnoon_break: k_midnoon_break_time,
                  ks_trade2: k_trade2_time,
                  ks_after_trade: k_after_trade_time}

# </editor-fold>

ks_msg_quit_loop = 'msg_quit_loop'
ks_msg_exception_occur = 'msg_exception_occur'


def find_stage(time):
    for kv in kd_trade_stage:
        begin, end = kd_trade_stage[kv]
        if begin <= time < end:
            return kv
    raise Exception(f'Cannot find time stage for time {time}')


def is_in_expanded_stage(time, stage, time_delta=dt.timedelta()):
    t1, t2 = kd_trade_stage[stage]
    dt1 = hp.to_datetime(t1)
    dt2 = hp.to_datetime(t2)
    dt1a = dt1 - time_delta
    dt2a = dt2 + time_delta
    return dt1a <= hp.to_datetime(time) <= dt2a


# <editor-fold desc="Stock Terms">
ks_open = 'open'
ks_close = 'close'
ks_low = 'low'
ks_hight = 'high'

ks_data = 'date'
ks_volumn = 'volumn'
ks_amount = 'amount'


class ClientHttpAccessConstant:
    k_operation = 'operation'
    k_stock_code = 'stock_code'
    k_price = 'price'
    k_amount = 'amount'
    k_entrust_type = 'entrust_type'
    k_entrust_id = 'entrust_id'
    k_query_info_type = 'query_info_type'
    k_buy = 'buy'
    k_sell = 'sell'
    k_cancel_entrust = 'cancel_entrust'
    k_query = 'query'
    k_buy_or_sell = 'buy_or_sell'
    k_fixed_price = 'fixed_price'
    k_query_content = 'query_content'


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


# </editor-fold>


def main():
    pass


if __name__ == '__main__':
    main()
