def assign_value_with_name(cls):
    for k in dir(cls):
        if not k.startswith('_'):
            setattr(cls, k, k)


class ClientHttpAccessConstant:
    operation = None
    stock_code = None
    price = None
    amount = None
    entrust_type = None
    entrust_id = None
    account_info_type = None
    buy = None
    sell = None
    cancel_entrust = None
    query = None
    buy_or_sell = None
    query_account_info = None
    query_day_entrust = None

    all = None
    myshare = None
    dayentrust = None
    dayfinentrust = None
    hisentrust = None
    hisfinentrust = None
    moneymovement = None
    deliveryentrust = None


assign_value_with_name(ClientHttpAccessConstant)

kca_ = ClientHttpAccessConstant
