import re

# noinspection PyProtectedMember
from tushare.stock.cons import _code_to_symbol


def stock_code_to_symbol(code):
    return _code_to_symbol(code)


def stock_to_sina_symbol(code):
    code = symbol_to_stock_code(code)
    return _code_to_symbol(code)


def symbol_to_stock_code(code):
    # noinspection PyUnresolvedReferences
    val = re.search('\d+', code)[0]
    return val

def stock_to_tdxserver_symbol(code):
    code = symbol_to_stock_code(code)
    symbol = _code_to_symbol(code)
    symbol = symbol.replace('sh', 'SH.')
    symbol = symbol.replace('sz', 'SZ.')
    return symbol

