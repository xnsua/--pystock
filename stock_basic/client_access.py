from common.web_helper import firefox_quick_get_url
from trade.trade_constant import ClientHttpAccessConstant

_c = ClientHttpAccessConstant

stock_server_address = 'http://127.0.0.1:8866'


def visit_server(urlargs):
    appendstr = ''
    for i, k in enumerate(urlargs):
        if not i:
            tmp = '?'
        else:
            tmp = '&'
        appendstr += tmp + str(k) + '=' + str(urlargs[k])
    url = stock_server_address + appendstr
    print(url)
    resp = firefox_quick_get_url(url)
    if resp.status_code == 200:
        return True, resp.text
    return False, resp.text


def sell_stock(stock_code, price, amount, entrust_type):
    urlargs = {_c.operation: _c.sell, _c.stock_code: stock_code,
               _c.price: price,
               _c.amount: amount,
               _c.entrust_type: entrust_type}
    ret = visit_server(urlargs)
    print(ret)


def buy_stock(stock_code, price, amount, entrust_type):
    urlargs = {_c.operation: _c.buy, _c.stock_code: stock_code, _c.price: price,
               _c.amount: amount, _c.entrust_type: entrust_type}
    ret = visit_server(urlargs)
    print(ret)


def query_account_info(info_type):
    urlargs = {_c.operation: _c.query, _c.account_info_type: info_type}
    ret = visit_server(urlargs)
    print(ret)


def cancel_entrust(entrust_id, stock_code, buyorsell):
    urlargs = {_c.operation: _c.cancel_entrust, _c.entrust_id: entrust_id,
               _c.stock_code: stock_code, _c.buy_or_sell: buyorsell}
    ret = visit_server(urlargs)
    print(ret)


def main():
    # sell_stock('SH.510900', 1.1, 100)
    # buy_stock('SH.510900', 1.1, 100)
    # query_account_info(_cas.myshare)
    cancel_entrust('O1704271039310081771', '510900', 'buy')


if __name__ == '__main__':
    main()
