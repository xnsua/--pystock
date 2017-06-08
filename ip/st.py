import datetime
import enum
import math
from enum import Enum
from typing import List

from common.alert import message_box_error
from common.base_functions import ObjectWithIndentRepr, ObjectWithRepr
from common.numeric import float_default_zero

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from log_helper import mylog
except Exception:
    pass


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


class ClientOperBase(ObjectWithIndentRepr):
    def __init__(self):
        self.result = None


class ClientOperBuy(ClientOperBase):
    def __init__(self, stock_code: str, price: float, number: int,
                 entrust_type: EntrustType):
        super().__init__()
        self.stock_code = stock_code
        self.price = price
        self.amount = number
        self.entrust_type = entrust_type

        self.result = None  # type: BuyResult


class ClientOperSell(ClientOperBase):
    def __init__(self, stock_code: str, price: float, number: int,
                 entrust_type: EntrustType):
        super().__init__()
        self.stock_code = stock_code
        self.price = price
        self.amount = number
        self.entrust_type = entrust_type

        self.result = None  # type: SellResult


class ClientOperCancel(ClientOperBase):
    def __init__(self, entrust_id, stock_code, way):
        super().__init__()
        self.entrust_id = entrust_id
        self.stock_code = stock_code
        self.way = way

        self.result = None  # type:CancelEntrustResult


class ClientOperQuery(ClientOperBase):
    def __init__(self, info_type):
        super().__init__()
        self.info_type = info_type
        self.result = None  # type: QueryResult


class BasicResult(ObjectWithIndentRepr):
    def __init__(self, success):
        self.success = success


# class BuyResult(BasicResult):
class BuyResultError(enum.Enum):
    not_in_trade_time = 1
    not_enough_money = 2
    not_proper_unit = 3
    not_in_price_range = 4

    @staticmethod
    def from_text(text):
        if text.find('在非正常时间内') != -1:
            return BuyResultError.not_in_trade_time
        elif text.find('该时段不允许撤单') != -1:
            return BuyResultError.not_in_trade_time
        elif text.find('该时段不支持该操作') != -1:
            return BuyResultError.not_in_trade_time
        elif text.find('非整手') != -1:
            return BuyResultError.not_proper_unit
        elif text.find('委托数量超出每笔数量') != -1:
            return BuyResultError.not_proper_unit
        elif text.find('资金不足') != -1:
            return BuyResultError.not_enough_money
        elif text.find('涨跌幅限制') != -1:
            return BuyResultError.not_in_price_range
        else:
            message_box_error('BuyResultError', text)


def test_buy_result_error():
    assert BuyResultError.not_in_trade_time \
           == BuyResultError.from_text('在非正常时间内')


class BuyResult(BasicResult):
    def __init__(self, success, entrust_id=None, err=None):
        super().__init__(success)
        self.entrust_id = entrust_id
        self.error = err


class SellResultError(enum.Enum):
    not_in_trade_time = 1
    not_in_price_range = 2
    not_enough_share = 3

    @staticmethod
    def from_text(text):
        if text.find('该时段不支持该操作') != -1:
            return SellResultError.not_in_trade_time
        elif text.find('在非正常时间内') != -1:
            return SellResultError.not_in_trade_time
        elif text.find('涨跌幅限制') != -1:
            return SellResultError.not_in_price_range
        elif text.find('客户股票不足') != -1:
            return SellResultError.not_enough_share
        elif text.find('持仓数量不足') != -1:
            return SellResultError.not_enough_share
        else:
            message_box_error('SellResultError', text)


class SellResult(BasicResult):
    def __init__(self, success, entrust_id=None, err_msg=None):
        super().__init__(success)
        self.entrust_id = entrust_id
        self.err_msg = err_msg


class CancelEntrustError(enum.Enum):
    entrust_not_find = 0
    cancelling_not_allowed = 1
    already_canceled = 2


class CancelEntrustResult(BasicResult):
    def __init__(self, success, err):
        super().__init__(success)
        self.err = err  # type: CancelEntrustError


class QueryResult(BasicResult):
    def __init__(self, success, data):
        super().__init__(success)
        assert success
        self.data = data


class ErrorResult(ObjectWithIndentRepr):
    def __init__(self, oper, err_msg):
        self.oper = oper
        self.err_msg = err_msg


class AccountInfo(ObjectWithIndentRepr):
    def __init__(self):
        self.balance = None
        self.available = None
        self.withdrawable = None
        self.market_value = None
        self.total_assert = None
        self.profit = None
        self.profit_per = None

        self.myshare_items = []  # type: List[ShareItem]
        self.entrust_items = []  # type: List[EntrustItem]


class ShareItem(ObjectWithRepr):
    # class ShareItem(ObjectWithIndentRepr):
    def __init__(self):
        self.code = None
        self.name = None
        self.amount = None
        self.amount_to_sell = None
        self.cost_price = None
        self.cur_price = None

    @classmethod
    def parse(cls, item_list) -> List['ShareItem']:
        print(item_list)
        assert len(item_list) == 2
        data_list = item_list[1]
        if len(data_list) < 1:
            mylog.info('The item is is empty. should have at lease one item')
            return []
        if len(data_list) == 1:
            text = ''.join(data_list[0])
            if text.find('没有相应的查询信息') != -1:
                return []
        index_dict = {}
        index = item_list[0]
        for idx, name in enumerate(index):
            index_dict[name] = idx
        i_code = index_dict["证券代码"]
        i_name = index_dict["证券名称"]
        i_amount = index_dict["证券数量"]
        i_amount_to_sell = index_dict["可卖数量"]
        i_cur_price = index_dict["当前价"]
        i_cost_price = index_dict["成本价"]
        s_items = []
        for val in item_list[1]:
            s_item = ShareItem()
            s_item.code = val[i_code]
            s_item.name = val[i_name]
            s_item.amount = float_default_zero(val[i_amount])
            s_item.amount_to_sell = float_default_zero(val[i_amount_to_sell])
            s_item.cost_price = float_default_zero(val[i_cost_price])
            s_item.cur_price = float_default_zero(val[i_cur_price])

            s_items.append(s_item)
        return s_items


class EntrustWay:
    way_buy = 'way_buy'
    way_sell = 'way_sell'

    @classmethod
    def from_text(cls, text):
        if text == '买入' or text == '买':
            return EntrustWay.way_buy
        elif text == '卖出' or text == '卖':
            return EntrustWay.way_sell
        message_box_error(f'Not a valid entrust way {text}')


class EntrustStatus:
    no_commit = 'not_finished'
    invalid = 'invalid'
    finished = 'finished'
    cancelled = 'cancelled'
    partial_finished = 'partial_finished'
    partial_cancelled = 'partial_cancelled'

    @classmethod
    def from_string(cls, text):
        text_map = {
            '全部申报': EntrustStatus.no_commit,

            '未成交': EntrustStatus.no_commit,

            '成交': EntrustStatus.finished,
            '已成交': EntrustStatus.finished,
            '全部成交': EntrustStatus.finished,

            '部分成交': EntrustStatus.partial_finished,
            '部成': EntrustStatus.partial_finished,

            '撤单': EntrustStatus.cancelled,
            '已撤单': EntrustStatus.cancelled,
            '场内撤单': EntrustStatus.cancelled,

            '部分撤单': EntrustStatus.partial_cancelled,
            '部撤': EntrustStatus.partial_cancelled,

            '废单': EntrustStatus.invalid,
            '场内废单': EntrustStatus.invalid,
            '系统废单': EntrustStatus.invalid,
        }
        if text not in text_map:
            message_box_error(f'EntrustStatus: {text}')
        return text_map[text]


# class EntrustItem(ObjectWithIndentRepr):
class EntrustItem(ObjectWithRepr):
    def __init__(self):
        self.code = None
        self.name = None
        self.is_buy = None
        self.entrust_id = None
        self.entrust_price = None
        self.cost_price = None
        self.entrust_amount = None
        self.commit_amount = None
        self.cancel_amount = None
        self.entrust_status = None
        self.entrust_dt = None

    @classmethod
    def parse(cls, item_list) -> List['EntrustItem']:
        assert len(item_list) == 2
        data_list = item_list[1]
        if len(data_list) < 1:
            mylog.info('The item is is empty. should have at lease one item')
            return []
        if len(data_list) == 1:
            text = ''.join(data_list[0])
            if text.find('没有相应的查询信息') != -1:
                return []
        index_dict = {}
        index = item_list[0]
        for idx, name in enumerate(index):
            index_dict[name] = idx
        i_code = index_dict["证券代码"]
        i_name = index_dict["证券名称"]
        i_amount_entrust = index_dict["委托数量"]
        i_amount_commit = index_dict["成交数量"]
        i_amount_cancel = index_dict["撤单数量"]
        i_entrust_id = index_dict['委托编号']

        i_entrust_time = index_dict["委托时间"]
        i_entrust_price = index_dict["委托价格"]
        try:
            i_cost_price = index_dict['成交均价']
        except KeyError:
            i_cost_price = index_dict["成交价格"]

        i_is_buy = index_dict["买卖标志"]
        i_entrust_status = index_dict['状态说明']

        s_items = []
        for val in item_list[1]:
            s_item = EntrustItem()
            s_item.entrust_id = val[i_entrust_id]
            s_item.code = val[i_code]
            s_item.name = val[i_name]
            s_item.entrust_amount = float_default_zero(val[i_amount_entrust])
            s_item.commit_amount = float_default_zero(val[i_amount_commit])
            s_item.cancel_amount = float_default_zero(val[i_amount_cancel])

            time_str = val[i_entrust_time]
            if len(time_str) < 6: time_str = '0' + time_str
            time_ = datetime.time(
                *map(int, [time_str[i:i + 2] for i in range(0, len(time_str), 2)]))
            s_item.entrust_dt = datetime.datetime.combine(datetime.date.today(), time_)
            s_item.cost_price = float_default_zero(val[i_cost_price])
            s_item.entrust_price = float_default_zero(val[i_entrust_price])
            s_item.entrust_status = EntrustStatus.from_string(val[i_entrust_status])

            s_item.is_buy = (val[i_is_buy] == '买入' or val[i_is_buy] == '买')
            s_items.append(s_item)
        return s_items

    pass


def test_parse_share_item():
    item_list = [
        ["证券代码", "证券名称", "证券数量", "持仓量", "可卖数量", "当前价", "最新市值", "成本价", "浮动盈亏", "盈亏比例(%)", "资金帐号",
         "股东代码",
         "交易所名称", "买卖标志", "投保标志", "今买数量", "今卖数量", "买持仓", "卖持仓", "昨日结算价", "保证金"],
        [["603900", "通灵珠宝", "4800.00", "4800.00", "4800.00", "30.800", "147840.00", "37.501",
          "-32164.80", "-17.87", "001001001015826", "p001001001015828",
          "上海证券交易所", "", "", "", "", "", "", "30.150", "<null>"]]]
    items = ShareItem.parse(item_list)
    assert len(items) == 1
    item = items[0]
    assert item.code == '603900'
    assert item.name == '通灵珠宝'
    assert math.isclose(item.amount, 4800.0)
    assert item.cost_price == 37.501
    assert item.cur_price == 30.8
    assert item.amount_to_sell == 4800.0

    item_list = [
        ["证券代码", "证券名称", "证券数量", "持仓量", "可卖数量", "当前价", "最新市值", "成本价", "浮动盈亏", "盈亏比例(%)", "资金帐号",
         "股东代码",
         "交易所名称", "买卖标志", "投保标志", "今买数量", "今卖数量", "买持仓", "卖持仓", "昨日结算价", "保证金"],
        [["没有相应的查询信息", "通灵珠宝", "4800.00", "4800.00", "4800.00", "30.800", "147840.00", "37.501",
          "-32164.80", "-17.87", "001001001015826", "p001001001015828",
          "上海证券交易所", "", "", "", "", "", "", "30.150", "<null>"]]]
    items = ShareItem.parse(item_list)
    assert not items


def test_parse_entrust_item():
    item_list = [
        ["证券名称", "买卖标志", "委托价格", "委托数量", "成交价格", "成交数量", "状态说明", "委托时间", "委托编号", "证券代码", "股东代码",
         "撤单数量"],
        [["H股ETF", "卖", "1.130", "200", "7.000", "10", "未成交", "112825", "561", "510900",
          "A533935434", "8"]
            , ["H股ETF", "买入", "", "", "", "", "成交", "", "", "", "", ""]]]

    items = EntrustItem.parse(item_list)
    assert len(items) == 2
    item1 = items[0]
    item2 = items[1]
    assert item1.name == 'H股ETF'
    assert item1.code == '510900'
    assert item1.entrust_id == '561'
    assert item1.entrust_status == EntrustStatus.no_commit
    assert math.isclose(item1.entrust_price, 1.13)
    assert math.isclose(item1.entrust_amount, 200)
    assert math.isclose(item1.cost_price, 7.000)
    assert math.isclose(item1.commit_amount, 10)
    assert math.isclose(item1.cancel_amount, 8)

    assert item2.name == 'H股ETF'
    assert item2.code == ''
    assert item2.entrust_id == ''
    assert math.isclose(item2.entrust_price, 0)
    assert math.isclose(item2.entrust_amount, 0)
    assert math.isclose(item2.cost_price, 0)
    assert math.isclose(item2.commit_amount, 0)
    assert math.isclose(item2.cancel_amount, 0)
    assert item2.entrust_status == EntrustStatus.finished

    item_list = [
        ["证券名称", "买卖标志", "委托价格", "委托数量", "成交价格", "成交数量", "状态说明", "委托时间", "委托编号", "证券代码", "股东代码",
         "撤单数量"],
        [["没有相应的查询信息", "卖", "1.130", "200", "7.000", "10", "未成交", "112825", "561", "510900",
          "A533935434", "8"]]]
    items = EntrustItem.parse(item_list)
    assert not items


def test_parse_entrust_item_emu():
    item_list = [['委托日期', '委托时间', '委托编号', '证券代码', '证券名称', '买卖标志', '委托价格', '委托数量', '成交均价',
                  '成交数量', '成交金额', '撤单数量', '状态说明', '股东代码', '资金帐号', '币种', '备注'],
                 [['20170525', '110311', 'O1705251103110109061', '510900', 'H股ETF', '买入', '1.130',
                   '100.00', '1.333',
                   '5.00', '0.00', '0.00', '全部申报', 'p001001001015828', '001001001015826', '人民币',
                   '']]]

    items = EntrustItem.parse(item_list)
    assert len(items) == 1
    item1 = items[0]
    assert item1.name == 'H股ETF'
    assert item1.code == '510900'
    assert item1.entrust_id == 'O1705251103110109061'
    assert item1.entrust_status == EntrustStatus.no_commit
    assert math.isclose(item1.entrust_price, 1.13)
    assert math.isclose(item1.entrust_amount, 100)
    assert math.isclose(item1.cost_price, 1.333)
    assert math.isclose(item1.commit_amount, 5)
    assert math.isclose(item1.cancel_amount, 0)

    item_list = [['委托日期', '委托时间', '委托编号', '证券代码', '证券名称', '买卖标志', '委托价格', '委托数量', '成交均价',
                  '成交数量', '成交金额', '撤单数量', '状态说明', '股东代码', '资金帐号', '币种', '备注'],
                 [['没有相应的查询信息', '110311', 'O1705251103110109061', '510900', 'H股ETF', '买入', '1.130',
                   '100.00', '1.333',
                   '5.00', '0.00', '0.00', '全部申报', 'p001001001015828', '001001001015826', '人民币',
                   '']]]
    items = EntrustItem.parse(item_list)
    assert not items
