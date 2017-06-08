from enum import Enum


class EntrustType(Enum):
    FIXED_PRICE = 0
    MARKET_PRICE_AND_CANCEL = 1
    MARKET_PRICE_AND_FIXED = 2

    def to_descs(self):
        method_dict = {self.FIXED_PRICE: ['限价委托'],
                       self.MARKET_PRICE_AND_CANCEL: ['五档即时成交剩余撤销',
                                                      '五档即成剩撤'],
                       self.MARKET_PRICE_AND_FIXED: ['五档即时成交剩余转限',
                                                     '五档即成转限价',
                                                     '五档即成剩限']}
        return method_dict[self]

    @classmethod
    def from_desc(cls, param):
        if not param:
            return cls.FIXED_PRICE
        if type(param) == cls:
            return param
        param = param.lower()
        val = {
            '限价委托': cls.FIXED_PRICE,
            '五档即时成交剩余撤销': cls.MARKET_PRICE_AND_CANCEL,
            '五档即成剩撤': cls.MARKET_PRICE_AND_CANCEL,
            '五档即时成交剩余转限': cls.MARKET_PRICE_AND_FIXED,
            '五档即成剩限': cls.MARKET_PRICE_AND_FIXED,
            '五档即成转限价': cls.MARKET_PRICE_AND_FIXED,
            'fixed_price': cls.FIXED_PRICE,
            'market_price_and_cancel': cls.MARKET_PRICE_AND_CANCEL,
            'market_price_and_fixed': cls.MARKET_PRICE_AND_FIXED,
        }
        return val[param]


class EntrustBuy:
    def __init__(self, stock_code: str, price: float, number: int, entrust_type: EntrustType):
        self.stock_code = stock_code
        self.price = price
        self.number = number
        self.entrust_type = entrust_type


class BuyResult:
    def __init__(self, success, result, complex_result):
        self.success = success
        self.result = result
        self.complex_result = complex_result
        # @classmethod
        # def


class SellResult:
    def __init__(self, success, result):
        self.success = success
        self.result = result


class CancelOrderResult:
    def __init__(self, success):
        self.success = success


class QueryResult:
    def __init__(self, success, account_info_type, data):
        self.success = success
        self.account_info_type = account_info_type
        self.data = data


class QueryMyShareResult:
    def __init__(self, success, account_info_type, data, balance_info):
        self.success = success
        self.account_info_type = account_info_type
        self.data = data
        self.balance_info = balance_info
