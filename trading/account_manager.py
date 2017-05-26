import datetime
import datetime
import threading
from typing import List

from common.datetime_manager import DateTimeManager
from ip.constants import kca_
from ip.st import AccountInfo, OperBuy, OperCancel, OperQuery, EntrustType, BuyResult, \
    EntrustStatus, QueryResult
from ip.st import EntrustItem
from ip.st import OperSell
from ip.st import ShareItem
from project_helper.phelper import jqd
from stock_utility.stock_shelve import myshelve, ShelveKey
from trading.base_structure.trade_constants import trade_bid_time


class AccountManager:
    def __init__(self):
        self._initial_account_info = None  # type: AccountInfo

        self._entrust_items = []  # type: List[EntrustItem]
        self._share_items = []  # type: List[ShareItem]

        self._oper_buys = []  # type: List[OperBuy]
        self._oper_sells = []  # type: List[OperSell]
        self._oper_cancel = []

        self._calc_available = None
        self._query_available = None

        self._lock = threading.RLock()

    def log(self, text, level=None):
        if level:
            level(f'{ACCOU_INFO:: }{text}')
        else:
            jqd(f'{ACCOU_INFO:: }{text}')

    def set_initial_account_info(self, account_info: AccountInfo):
        key = ShelveKey.initial_account_info
        dtnow = datetime.datetime.now()
        if dtnow.time() > trade_bid_time:
            if key in myshelve:
                dt, value = myshelve[key]
                if dt.date() == dtnow.date():
                    self._initial_account_info = value
                    return
            raise Exception('Can not set initial account info')
        else:
            self._initial_account_info = account_info
            myshelve[key] = (dtnow, account_info)
            return

    def _on_oper_query(self, oper_rs: OperQuery):
        if oper_rs.result.success:
            if oper_rs.info_type == kca_.myshare:
                self._share_items.append(oper_rs.result.data)
                self._query_available = oper_rs.result.data
            elif oper_rs.info_type == kca_.dayentrust:
                self._entrust_items.append(oper_rs.result.data)
                self._oper_buys.clear()
                self._oper_sells.clear()
                self._oper_cancel.clear()
                self._update_available()

    def on_operation_result(self, oper_rs):
        with self._lock:
            if isinstance(oper_rs, OperQuery):
                self._on_oper_query(oper_rs)
            else:
                store_place_map = {
                    OperBuy: self._oper_buys,
                    OperSell: self._oper_sells,
                    OperCancel: self._oper_cancel,
                }
                store_place = store_place_map[type(oper_rs)]
                store_place.append(oper_rs)
                self._update_available()

    def _update_available(self):
        with self._lock:
            available = self._initial_account_info.available
            for val in self._entrust_items:
                if val.is_buy:
                    if val.entrust_status in [EntrustStatus.waiting, EntrustStatus.finished,
                                              EntrustStatus.partial_finished]:
                        available -= val.entrust_amount * val.cost_price
                    elif val.entrust_status in [EntrustStatus.partial_cancelled]:
                        available -= val.commit_amount * val.cost_price
                    else:
                        continue
                else:
                    if val.entrust_status == EntrustStatus.finished:
                        available += val.entrust_amount * val.cost_price

            for val in self._oper_buys:
                available -= val.price * val.amount

            self._query_available = None
            self._calc_available = available

    @property
    def available(self):
        print('-----')
        print(self._calc_available)
        print(self._calc_available)
        with self._lock:
            if self._query_available:
                return self._query_available
            else:
                return self._calc_available


from nose.tools import *


@raises(Exception)
def test_set_initial_account_info_no_cache():
    myshelve.clear()
    with DateTimeManager(datetime.datetime(2000, 1, 1, 9, 44, 0)):
        account_info = AccountInfo()
        account_info.balance = 11111
        account_manager = AccountManager()
        account_manager.set_initial_account_info(account_info)


def test_set_initial_account_info_use_cache():
    myshelve.clear()
    with DateTimeManager(datetime.datetime(2000, 1, 1, 9, 14, 0)):
        account_info = AccountInfo()
        account_info.balance = 11111
        account_manager = AccountManager()
        account_manager.set_initial_account_info(account_info)

    with DateTimeManager(datetime.datetime(2000, 1, 1, 9, 44, 0)):
        account_info = AccountInfo()
        account_info.balance = 22222
        account_manager = AccountManager()
        account_manager.set_initial_account_info(account_info)

        assert_equal(account_manager._initial_account_info.balance, 11111)


@raises(Exception)
def test_set_initial_account_info3_cache_too_old():
    myshelve.clear()
    with DateTimeManager(datetime.datetime(2000, 1, 1, 9, 14, 0)):
        account_info = AccountInfo()
        account_info.balance = 11111
        account_manager = AccountManager()
        account_manager.set_initial_account_info(account_info)

    with DateTimeManager(datetime.datetime(2000, 1, 2, 9, 44, 0)):
        account_info = AccountInfo()
        account_info.balance = 22222
        account_manager = AccountManager()
        account_manager.set_initial_account_info(account_info)

        assert_equal(account_manager._initial_account_info.balance, 11111)


def test_add_oper_buy():
    account_manager = AccountManager()
    account_info = AccountInfo()
    account_info.available = 1000
    account_manager._initial_account_info = account_info

    oper_buy = OperBuy('510900', 1, 100, EntrustType.FIXED_PRICE)
    oper_buy.result = BuyResult(True, '510900')
    account_manager.on_operation_result(oper_buy)
    assert_equal(account_manager.available, 900)


def test_add_oper_sell():
    account_manager = AccountManager()
    account_info = AccountInfo()
    account_info.available = 1000
    account_manager._initial_account_info = account_info

    oper_buy = OperSell('510900', 1, 100, EntrustType.FIXED_PRICE)
    oper_buy.result = BuyResult(True, '510900')
    account_manager.on_operation_result(oper_buy)
    assert_equal(account_manager.available, 1000)


def test_add_oper_query_entrust():
    account_manager = AccountManager()
    account_info = AccountInfo()
    account_info.available = 1000
    account_manager._initial_account_info = account_info

    oper_query = OperQuery(kca_.dayentrust)
    entrust_item = EntrustItem()
    entrust_item.cost_price = 1
    entrust_item.entrust_amount = 1
    query_result = QueryResult(True, )
    oper_buy.result = BuyResult(True, '510900')
    account_manager.on_operation_result(oper_buy)
    assert_equal(account_manager.available, 1000)
