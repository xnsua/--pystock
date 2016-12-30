from sqlalchemy import DateTime
from sqlalchemy import Table, Column, Integer, String, Float, MetaData


class Constant:
    account = 'account'
    stocks = 'stocks'
    entrustment = 'entrustment'
    exchange_list = 'exchange_list'
    code = 'code'
    name = 'name'
    amount = 'amount'
    id = 'id'
    time = 'time'
    code = 'code'
    name = 'name'
    operation = 'operation'
    exchange = 'exchange'
    price = 'price'
    type = 'type'
    withdraw = 'withdraw'
    id = 'id'
    time = 'time'
    code = 'code'
    name = 'name'
    price = 'price'
    tax = 'tax'
    commission = 'commission'
    transfer_fee = 'transfer_fee'
    money_changed = 'money_changed'
    money_remain = 'money_remain'
    stock_remain = 'stock_remain'


meta = MetaData()
stocks = Table(Constant.stocks, meta,
               Column(Constant.code, String, primary_key=True),
               Column(Constant.name, String),
               Column(Constant.amount, Integer))
entrustment = Table(Constant.entrustment, meta,
                    Column(Constant.id, String, primary_key=True),
                    Column(Constant.time, DateTime),
                    Column(Constant.code, String),
                    Column(Constant.name, String),
                    Column(Constant.operation, String),
                    Column(Constant.exchange, Integer),
                    Column(Constant.price, Float),
                    Column(Constant.type, String),
                    Column(Constant.withdraw, Float)
                    )
exchange_list = Table(Constant.exchange_list, meta,
                      Column(Constant.id, String, primary_key=True),
                      Column(Constant.time, DateTime),
                      Column(Constant.code, String),
                      Column(Constant.name, String),
                      Column(Constant.price, Float),
                      Column(Constant.tax, Float),
                      Column(Constant.commission, Float),
                      Column(Constant.transfer_fee, Float),
                      Column(Constant.money_changed, Float),
                      Column(Constant.money_remain, Float),
                      Column(Constant.stock_remain, Float))
