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
    urlargs = {_c.k_operation: _c.k_sell, _c.k_stock_code: stock_code,
               _c.k_price: price,
               _c.k_amount: amount,
               _c.k_entrust_type: entrust_type}
    ret = visit_server(urlargs)
    print(ret)


def buy_stock(stock_code, price, amount, entrust_type):
    urlargs = {_c.k_operation: _c.k_buy, _c.k_stock_code: stock_code, _c.k_price: price,
               _c.k_amount: amount, _c.k_entrust_type: entrust_type}
    ret = visit_server(urlargs)
    print(ret)


def query_account_info(info_type):
    urlargs = {_c.k_operation: _c.k_query, _c.k_query_info_type: info_type}
    ret = visit_server(urlargs)
    print(ret)


def cancel_entrust(entrust_id, stock_code, buyorsell):
    urlargs = {_c.k_operation: _c.k_cancel_entrust, _c.k_entrust_id: entrust_id,
               _c.k_stock_code: stock_code, _c.k_buy_or_sell: buyorsell}
    ret = visit_server(urlargs)
    print(ret)


def main():
    # sell_stock('SH.510900', 1.1, 100)
    # buy_stock('SH.510900', 1.1, 100)
    # query_account_info(_cas.k_myshare)
    cancel_entrust('O1704271039310081771', '510900', 'buy')


if __name__ == '__main__':
    main()
