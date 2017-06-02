import threading
from typing import List

from common.alert import message_box_error
from ip.constants import kca_
from ip.st import AccountInfo, ClientOperBase, QueryResult, BuyResult, SellResult, \
    EntrustStatus, ClientOperCancel, ClientOperQuery, EntrustItem, EntrustType
from ip.st import ClientOperBuy
from ip.st import ClientOperSell
from project_helper.logbook_logger import mylog


class AccountManager:
    # imp Check all function use the lock
    def __init__(self):
        self._account_info = None  # type: AccountInfo
        self._lock = threading.RLock()
        self._need_push = False

        self._buy_oper = []  # type: List[ClientOperBuy]
        self._sell_oper = []  # type: List[ClientOperSell]

    def _on_oper_query(self, oper_with_result):
        assert oper_with_result.result.success
        result_data = oper_with_result.result.data
        # mylog.info(f'On oper query result data: {result_data}')
        if isinstance(result_data, AccountInfo):
            self._account_info = result_data
        else:
            message_box_error('Result data type not account info', repr(result_data))

    def _calc_need_push(self):
        buy_item_code = [item.result.entrust_id for item in self._buy_oper
                         if item.result.success]
        sell_item_code = [item.result.entrust_id for item in self._sell_oper
                          if item.result.success]
        check_items = [item for item in self._account_info.entrust_items
                       if item.entrust_id in [*buy_item_code, *sell_item_code]]
        # The result is not refreshed
        if len(check_items) != (len(buy_item_code) + len(sell_item_code)):
            mylog.notice(f'CheckItem len {len(check_items)} '
                         f'do not equal {len(buy_item_code)} + {len(sell_item_code)}')
            return True
        else:
            # The result is refreshed, find the unfinished item
            unfinished_item = [item for item in check_items
                               if item.entrust_status in [EntrustStatus.no_commit,
                                                          EntrustStatus.partial_finished]]
            if not len(unfinished_item):
                self._buy_oper.clear()
                self._sell_oper.clear()

            return len(unfinished_item)

    def on_operation_result(self, oper_with_result: ClientOperBase):
        with self._lock:
            # mylog.info(f'On operation result: {oper_with_result}')
            if isinstance(oper_with_result, ClientOperQuery):
                self._on_oper_query(oper_with_result)

            elif isinstance(oper_with_result, ClientOperBuy):
                self._buy_oper.append(oper_with_result)

            elif isinstance(oper_with_result, ClientOperSell):
                self._sell_oper.append(oper_with_result)

            elif isinstance(oper_with_result, ClientOperCancel):
                pass
            else:
                message_box_error('Invalid oper with result', oper_with_result)
            self._need_push = self._calc_need_push()
            mylog.notice(
                'Need client push....' if self._need_push else '** NOT ** need client push ...')

    @property
    def available(self):
        with self._lock:
            return self._account_info.available

    @property
    def entrust_items(self):
        with self._lock:
            return self._account_info.entrust_items

    @property
    def share_items(self):
        with self._lock:
            return self._account_info.myshare_items

    @property
    def need_client_push(self):
        with self._lock:
            return self._need_push


# noinspection PyProtectedMember
def test_cal_push():
    account_manager = AccountManager()
    assert account_manager.need_client_push == False
    account_info = AccountInfo()
    account_manager._account_info = account_info
    # Add ClientOperBuy
    client_oper_buy1 = ClientOperBuy('510900', 1.1, 100, EntrustType.FIXED_PRICE)
    client_oper_buy1.result = BuyResult(True, 'buy_id1')
    account_manager.on_operation_result(client_oper_buy1)

    # Add ClientQuery
    account_info.myshare_items = []
    entrust_item1 = EntrustItem()
    entrust_item1.entrust_id = 'buy_id1'
    entrust_item1.entrust_status = EntrustStatus.no_commit
    account_info.entrust_items = [entrust_item1]
    client_oper_query_all = ClientOperQuery(info_type=kca_.account_info)
    client_oper_query_all.result = QueryResult(True, account_info)
    account_manager.on_operation_result(client_oper_query_all)
    assert account_manager.need_client_push

    # Change status
    entrust_item1.entrust_status = EntrustStatus.partial_finished
    account_manager.on_operation_result(client_oper_query_all)
    assert account_manager.need_client_push

    entrust_item1.entrust_status = EntrustStatus.finished
    account_manager.on_operation_result(client_oper_query_all)
    assert not account_manager.need_client_push
    assert not account_manager._buy_oper

    client_oper_sell1 = ClientOperBuy('510900', 1.1, 100, EntrustType.FIXED_PRICE)
    client_oper_sell1.result = SellResult(True, 'sell_id1')
    account_manager.on_operation_result(client_oper_sell1)
    assert account_manager.need_client_push

    entrust_item2 = EntrustItem()
    entrust_item2.entrust_id = 'sell_id1'
    entrust_item2.entrust_status = EntrustStatus.partial_finished
    account_info.entrust_items.append(entrust_item2)
    client_oper_query_all.result.data = account_info
    account_manager.on_operation_result(client_oper_query_all)
    assert account_manager.need_client_push

    entrust_item2.entrust_status = EntrustStatus.cancelled
    account_manager.on_operation_result(client_oper_query_all)
    assert not account_manager.need_client_push
    assert not account_manager._sell_oper
