import tushare as tu

from common.helper import sleep_ms, ndays_ago

while 1:
    df = tu.get_k_data('510900', start=str(ndays_ago(5)))
    print(df.tail(1).iloc[0, 0])
    sleep_ms(100000)
