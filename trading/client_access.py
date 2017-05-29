import jsonpickle

from common.alert import message_box_error
from common.web_helper import firefox_quick_get_url
from ip.constants import ClientHttpAccessConstant
from ip.st import ClientOperBuy, EntrustType
from project_helper.logbook_logger import mylog

jsonpickle.load_backend('simplejson')
jsonpickle.set_encoder_options('simplejson', sort_keys=True, ensure_ascii=False)

_c = ClientHttpAccessConstant

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
    resp = firefox_quick_get_url(url, headers, timeout=timeout)
    if resp.status_code == 200:
        return jsonpickle.loads(resp.text)
    message_box_error(f"Serve status_code:", resp.status_code, 'resp.text:', resp.text)


def fire_operation(oper):
    order_str = jsonpickle.dumps(oper)
    order_str = order_str.strip()
    return _visit_client_server(
        {'operation': type(oper).__name__, **oper.__dict__}, {'object': order_str})


def is_client_server_running():
    url = stock_server_address + '/test'
    resp = firefox_quick_get_url(url, timeout=0.5)
    return resp.status_code == 200


def test_operation():
    buy = ClientOperBuy('SH.510900', 1.2, 100, EntrustType.FIXED_PRICE)
    result = fire_operation(buy)
    print(result)