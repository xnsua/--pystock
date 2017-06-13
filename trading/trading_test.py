from trading.client_access import test_operation_sell, test_operation_query_dayentrust, \
    test_operation_buy


def do_operations():
    while 1:
        # is_client_server_running()
        # continue
        test_operation_buy()
        id1 = test_operation_sell()
        # print(id1)
        val = test_operation_query_dayentrust()
        # print(val)
        # cancel = ClientOperCancel(id1, '510900', EntrustWay.way_sell)
        # result = fire_operation(cancel)
        # print(result)
        # val = test_operation_query_dayentrust()
        # print(val)
        # print(result)
        # break


do_operations()
