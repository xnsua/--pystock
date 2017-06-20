from typing import List

import jsonpickle
import requests

from common.alert import message_box_error
from common.web_helper import firefox_quick_get_url
from ip.constants import ClientConstant
from ip.st import ClientOperBuy, EntrustType, BuyResult, SellResult, ClientOperSell, \
    ClientOperQuery, AccountInfo, QueryResult, ShareItem, EntrustItem, ClientOperCancel, \
    EntrustWay, ErrorResult
from project_helper.logbook_logger import mylog

jsonpickle.load_backend('simplejson')
jsonpickle.set_encoder_options('simplejson', sort_keys=True, ensure_ascii=False)

_c = ClientConstant

stock_server_address = 'http://127.0.0.1:8866'
stock_server_operation_address = 'http://127.0.0.1:8866/operation'


def _visit_client_server(url_args, headers, timeout=5):
    append_str = ''
    for i, k in enumerate(url_args):
        if not i:
            tmp = '?'
        else:
            tmp = '&'
        append_str += tmp + str(k) + '=' + str(url_args[k])
    url = stock_server_operation_address + append_str
    mylog.info(url)
    while 1:
        try:
            resp = firefox_quick_get_url(url, headers, timeout=timeout)
            if resp.status_code == 200:
                return jsonpickle.loads(resp.text)
            message_box_error(f"Serve status_code:", resp.status_code, 'resp.text:', resp.text)
        except requests.exceptions.RequestException as e:
            mylog.error(f'Request Exception: {e}')


def fire_operation(oper):
    order_str = jsonpickle.dumps(oper)
    # mylog.warn(repr(oper))
    order_str = order_str.strip()
    success_cnt = 0
    fail_cnt = 0
    for i in range(3):
        result = _visit_client_server(
            {'operation': type(oper).__name__, **oper.__dict__}, {'object': order_str}, timeout=10)
        if isinstance(result, ErrorResult):
            fail_cnt += 1
            mylog.error(f'Client error: {result}, Retrying {i}, count: {fail_cnt}/{success_cnt}')
        else:
            success_cnt += 1
            return result
    message_box_error(f'Failed eventually {result}')


def is_client_server_running():
    url = stock_server_address + '/test'
    resp = firefox_quick_get_url(url, timeout=0.5)
    return resp.status_code == 200


def test_operation_buy():
    buy = ClientOperBuy('SH.510900', 0.8, 100, EntrustType.FIXED_PRICE)
    result = fire_operation(buy)
    # print(result)
    assert isinstance(result, BuyResult), repr(result)


def test_operation_buy_market_price():
    buy = ClientOperBuy('SH.510900', 0, 100, EntrustType.MARKET_PRICE_AND_CANCEL)
    result = fire_operation(buy)
    print(result)
    assert isinstance(result, BuyResult)


def test_operation_sell():
    sell = ClientOperSell('SH.510900', 2, 100, EntrustType.FIXED_PRICE)
    result = fire_operation(sell)
    # print(result)
    assert isinstance(result, SellResult)
    return result.entrust_id


def test_operation_query_all():
    query = ClientOperQuery(ClientConstant.account_info)
    result = fire_operation(query)
    print(result)
    assert isinstance(result, QueryResult)
    assert isinstance(result.data, AccountInfo)


def test_operation_query_cancelentrust():
    query = ClientOperQuery(ClientConstant.cancelentrust)
    result = fire_operation(query)
    print(result)
    assert isinstance(result, QueryResult)



def test_operation_query_myshare():
    query = ClientOperQuery(ClientConstant.myshare)
    result = fire_operation(query)
    print(result)
    assert isinstance(result, QueryResult)
    assert isinstance(result.data, List)
    if len(result.data):
        assert isinstance(result.data[0], ShareItem)


def test_operation_query_dayentrust():
    query = ClientOperQuery(ClientConstant.dayentrust)
    result = fire_operation(query)
    # print(result)
    assert isinstance(result, QueryResult)
    assert isinstance(result.data, List)
    if len(result.data):
        assert isinstance(result.data[0], EntrustItem)
    return [(item.entrust_id, item.entrust_status) for item in result.data]


def test_cancel_order():
    canceller = ClientOperCancel('O1706021110090094021', 'SH.510900', EntrustWay.way_buy)
    result = fire_operation(canceller)
    print(result)
