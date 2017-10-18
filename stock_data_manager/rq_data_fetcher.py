import pickle
from io import BytesIO

import jsonpickle
import numpy

from common.scipy_helper import pdDF
from common.web_helper import firefox_quick_get_url

jsonpickle.load_backend('simplejson')
jsonpickle.set_encoder_options('simplejson', sort_keys=True, ensure_ascii=False)

stock_server_address = 'http://127.0.0.1:9966'
def _visit_server(oper_str, headers = None):
    url = stock_server_address + '/' + oper_str
    resp = firefox_quick_get_url(url, timeout=0.5, headers=headers)
    byteio = BytesIO()
    for chunk in resp.iter_content(1024):
        byteio.write(chunk)
    val = pickle.loads(byteio.getvalue())
    assert resp.status_code == 200
    return val

def _np_compound_arr_to_df(arr):
    val = pdDF(arr)
    val['datetime'] = (val['datetime']/1000000).astype(numpy.int64)
    val.set_index('datetime', inplace=True)
    return val

def rq_history_bars(rq_code):
    val = _visit_server('history_bars', headers={'code':rq_code})
    val = _np_compound_arr_to_df(val)
    return val

def rq_all_instruments(type_):
    val = _visit_server('all_instruments', headers={'type':type_})
    return val

def rq_all_A_instruments(type_):
    """ Remove stock in B-share market """
    val = rq_all_instruments(type_)
    index = val.order_book_id.apply(lambda v:not v.startswith('9'))
    val = val[index]
    return val

def rq_all_stock_code():
    val = rq_all_A_instruments('CS')
    return val.order_book_id

def main():
    import datetime
    s_time = datetime.datetime.now()
    val = (rq_all_A_instruments('CS'))

    print(val.order_book_id)
    print(datetime.datetime.now() - s_time)

    pass


if __name__ == '__main__':
    main()


