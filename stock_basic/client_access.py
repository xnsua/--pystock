from common.web_helper import firefox_quick_get_url
from trade.trade_constant import ks_operation, ks_stock_code, ks_price, \
    ks_entrust_id, ks_query_info_type, ks_buy, ks_sell, ks_cancel_entrust, \
    ks_query, \
    ks_buy_or_sell, ks_amount

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


def sell_stock(stock_code, price, amount):
    urlargs = {ks_operation: ks_sell, ks_stock_code: stock_code,
               ks_price: price,
               ks_amount: amount}
    ret = visit_server(urlargs)
    print(ret)


def buy_stock(stock_code, price, amount):
    urlargs = {ks_operation: ks_buy, ks_stock_code: stock_code, ks_price: price,
               ks_amount: amount}
    ret = visit_server(urlargs)
    print(ret)


def query_account_info(info_type):
    urlargs = {ks_operation: ks_query, ks_query_info_type: info_type}
    ret = visit_server(urlargs)
    print(ret)


def cancel_entrust(entrust_id, stock_code, buyorsell):
    urlargs = {ks_operation: ks_cancel_entrust, ks_entrust_id: entrust_id,
               ks_stock_code: stock_code, ks_buy_or_sell: buyorsell}
    ret = visit_server(urlargs)
    print(ret)


def main():
    # sell_stock('SH.510900', 1.1, 100)
    # buy_stock('SH.510900', 1.1, 100)
    # query_account_info(ks_myshare)
    cancel_entrust('O1704271039310081771', '510900', 'buy')


if __name__ == '__main__':
    main()
