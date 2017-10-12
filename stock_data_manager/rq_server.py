import pickle

import numpy
from flask import Flask, request
from rqalpha.api import *

app = Flask(__name__)
from rqalpha import run_func

config = {
    "base": {
        "start_date": "2016-06-01",
        "end_date": "2019-12-01",
        "benchmark": "000300.XSHG",
        "accounts": {
            "stock": 100000
        }
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True
        }
    }
}
g_context = None


def extract_dict_from_header(headers):
    task = {}
    for k, v in headers:
        remove_list = ['Host', 'User-Agent', 'Accept', 'Accept-Language',
                       'Accept-Encoding', 'Connection', 'Origin',
                       'cache-control', 'upgrade-insecure-requests']
        remove_list = [v.lower() for v in remove_list]
        if k.lower() not in remove_list:
            k = k.lower()
            k = k.replace('-', '_')
            task[k] = v

    return task


def extract_dict_from_url_param(args):
    vd = {}
    for v in args:
        vd[v] = args.get(v)
    return vd


def extract_request_param(request_):
    d1 = extract_dict_from_header(request_.headers)
    d2 = extract_dict_from_url_param(request_.args)
    for k, v in d2.items():
        d1[k] = v
    return d1


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    global g_context
    g_context = context
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False


def before_trading(context):
    app.run(port=9966, debug=False)
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        order_percent(context.s1, 1)
        context.fired = True


@app.route("/history_bars")
def history_bars_wrapper():
    code = request.headers.get('code')
    gv = history_bars(code, 2450, '1d',
                      ['datetime', 'open', 'close', 'high', 'low', 'volume'])
    return pickle.dumps(gv)


@app.route('/all_instruments')
def all_instruments_wrapper():
    type_ = request.headers.get('type')
    val = all_instruments(type_)
    vfunc = numpy.vectorize(is_st_stock)
    bool_index = vfunc(val['order_book_id'])
    print('Length: ', len(val))
    val = val[bool_index == False]
    print('After remove st stock: ', len(val))

    return pickle.dumps(val)


def main():
    # update_bundle()
    config['base']['start_date'] = '2017-09-21'
    run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)


if __name__ == '__main__':
    main()
