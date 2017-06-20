from trading.client_access import test_operation_sell, test_operation_query_dayentrust, \
    test_operation_buy, test_operation_query_cancelentrust


def do_operations():
    while 1:
        test_operation_buy()
        test_operation_buy()
        test_operation_sell()
        test_operation_query_dayentrust()
        test_operation_buy()
        test_operation_sell()
        test_operation_query_dayentrust()
        test_operation_query_cancelentrust()
        break


do_operations()
