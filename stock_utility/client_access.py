import jsonpickle

from common.web_helper import firefox_quick_get_url
from ip.constants import ClientHttpAccessConstant
from project_helper.phelper import jqd

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
    jqd('VISITSERVER: ', url)
    resp = firefox_quick_get_url(url, headers, timeout=timeout)
    if resp.status_code == 200:
        return True, jsonpickle.loads(resp.text)
    return False, resp.text


def fire_operation(oper):
    """

    :rtype: object
    """
    order_ps = jsonpickle.dumps(oper)
    order_ps = order_ps.strip()
    return _visit_client_server(
        {'operation': type(oper).__name__, **oper.__dict__}, {'object': order_ps})


def is_client_server_running():
    url = stock_server_address + '/test'
    resp = firefox_quick_get_url(url, timeout=0.5)
    return resp.status_code == 200


def main():
    val = is_client_server_running()
    print(val)
    return
    # order = EntrustBuy('510900', 1.1, 100, EntrustType.FIXED_PRICE)
    # success, obj = fire_operation(order)
    # print(success, obj)


if __name__ == '__main__':
    main()
