from common.web_helper import firefox_quick_get_url

k_operation = 'operation'
k_stock_code = 'stock_code'
k_price = 'price'
k_amount = 'amount'
k_entrust_type = 'entrust_type'
k_entrust_id = 'entrust_id'
k_query_info_type = 'query_info_type'
k_buy = 'buy'
k_sell = 'sell'
k_cancel_entrust = 'cancel_entrust'
k_query = 'query'
k_buy_or_sell = 'buy_or_sell'
k_fixed_price = 'fixed_price'
k_query_content = 'query_content'

k_myshare = "myshare"
k_dayentrust = "dayentrust"
k_dayfinentrust = "dayfinentrust"
k_hisentrust = "hisentrust"
k_hisfinentrust = "hisfinentrust"
k_moneymovement = "moneymovement"
k_deliveryentrust = "deliveryentrust"

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
    urlargs = {k_operation: k_sell, k_stock_code: stock_code, k_price: price,
               k_amount: amount}
    ret = visit_server(urlargs)
    print(ret)


def buy_stock(stock_code, price, amount):
    urlargs = {k_operation: k_buy, k_stock_code: stock_code, k_price: price,
               k_amount: amount}
    ret = visit_server(urlargs)
    print(ret)


def query_account_info(info_type):
    urlargs = {k_operation: k_query, k_query_info_type: info_type}
    ret = visit_server(urlargs)
    print(ret)


def cancel_entrust(entrust_id, stock_code, buyorsell):
    urlargs = {k_operation: k_cancel_entrust, k_entrust_id: entrust_id,
               k_stock_code: stock_code, k_buy_or_sell: buyorsell}
    ret = visit_server(urlargs)
    print(ret)


def main():
    # sell_stock('SH.510900', 1.1, 100)
    # buy_stock('SH.510900', 1.1, 100)
    # query_account_info(k_myshare)
    cancel_entrust('O1704271039310081771', '510900', 'buy')


if __name__ == '__main__':
    main()
