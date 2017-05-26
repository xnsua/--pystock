import datetime
import datetime
import threading
from typing import List
from typing import Tuple
from win32pdh import OpenQuery

from common.datetime_mocker import mock_datetime
from ip.constants import kca_
from ip.st import AccountInfo, OperBuy, OperCancel, OperQuery, EntrustType, BuyResult, \
    EntrustStatus
from ip.st import EntrustItem
from ip.st import OperSell
from ip.st import ShareItem
from project_helper.phelper import jqd
from stock_utility.stock_shelve import myshelve, ShelveKey
from trading.base_structure.trade_constants import StockTimeConstant


class AccountManager:
    def __init__(self):
        self._initial_account_info = None  # type: AccountInfo

        self._entrust_items = None  # type: List[EntrustItem]
        self._share_items = None  # type: List[ShareItem]

        self._oper_buys = []  # type: List[OperBuy]
        self._oper_sells = []  # type: List[OperSell]
        self._oper_cancel = []

        self._calc_available = None
        self._query_available = None

        self._lock = threading.Lock()

    def log(self, text, level=None):
        if level:
            level(f'{ACCOU_INFO:: }{text}')
        else:
            jqd(f'{ACCOU_INFO:: }{text}')

    def set_initial_account_info(self, account_info: AccountInfo):
        key = ShelveKey.initial_account_info
        if key in myshelve:
            dt, value = myshelve[key]  # type: Tuple[datetime.datetime, AccountInfo]
            bid_start_time = StockTimeConstant.before_bid_time[1]
            if dt.date() == datetime.date.today() and dt.time() > bid_start_time
                self._initial_account_info = value
                self.log('Use cached account info')
                return

        self._initial_account_info = account_info
        myshelve[key] = account_info
        assert len(self._initial_account_info.get_entrusts()) == 0

    def _on_oper_query(self, oper_rs: OperQuery):
        if oper_rs.result.success:
            if oper_rs.info_type == kca_.myshare:
                self._share_items.append(oper_rs.result.data)
            elif oper_rs.info_type == kca_.dayentrust:
                self._entrust_items.append(oper_rs.result.data)
                self._oper_buys.clear()
                self._oper_sells.clear()
                self._oper_cancel.clear()
            self.update_available()

    def on_operation_result(self, oper_rs):
        with self._lock:
            if isinstance(oper_rs, OperQuery):
                self._on_oper_query(oper_rs)
            else:
                store_place_map = {
                    OperBuy: self._oper_buys,
                    OperSell: self._oper_sells,
                    OperCancel: self._oper_cancel,
                    OpenQuery: self._oper_query
                }
                store_place = store_place_map[type(oper_rs)]
                store_place.append(oper_rs)

    def update_available(self):
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


def test_set_initial_account_info():
    mock_datetime(datetime.datetime(2000, 1, 1, 8, ))
    account_info = AccountInfo()
    account_info.balance = 11111
    account_manager = AccountManager()
    account_manager.set_initial_account_info(account_info)


def test_add_oper_buy():
    account_manager = AccountManager()
    account_info = AccountInfo()
    account_info.available = 1000
    oper_buy = OperBuy('510900', 1, 100, EntrustType.FIXED_PRICE)
    oper_buy.result = BuyResult(True, '510900')
    account_manager.on_operation_result(oper_buy)
