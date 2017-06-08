import threading
from typing import List

from common.alert import message_box_error
from ip.constants import ClientConstant
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
        entrusts = self._account_info.entrust_items
        entrusts_ids = {item.entrust_id for item in entrusts}
        buy_entrust_ids = {item.result.entrust_id for item in self._buy_oper}
        sell_entrust_ids = {item.result.entrust_id for item in self._sell_oper}

        if (buy_entrust_ids | sell_entrust_ids) > entrusts_ids:
            mylog.error(f'Id missing in entrust items. buyids:{buy_entrust_ids}'
                        f'sellids: {sell_entrust_ids}, entrust_ids: {entrusts_ids}')

        status_unfinished = [EntrustStatus.no_commit, EntrustStatus.partial_finished]

        unfinished_ids = {item.entrust_id for item in entrusts
                          if item.entrust_status in status_unfinished}

        if not unfinished_ids > (buy_entrust_ids | sell_entrust_ids):
            mylog.warn(f'Untracted entrust')

        # Remove finished items from buy oper and sell oper
        self._buy_oper = [item for item in self._buy_oper if
                          item.result.entrust_id in unfinished_ids]
        self._sell_oper = [item for item in self._sell_oper if
                           item.result.entrust_id in unfinished_ids]

        return self._buy_oper or self._sell_oper

    def on_operation_result(self, oper_with_result: ClientOperBase):
        with self._lock:
            # mylog.info(f'On operation result: {oper_with_result}')
            if isinstance(oper_with_result, ClientOperQuery):
                self._on_oper_query(oper_with_result)
                self._need_push = self._calc_need_push()

            elif isinstance(oper_with_result, ClientOperBuy):
                if oper_with_result.result.success:
                    self._buy_oper.append(oper_with_result)
                self._need_push = True

            elif isinstance(oper_with_result, ClientOperSell):
                if oper_with_result.result.success:
                    self._sell_oper.append(oper_with_result)
                self._need_push = True

            elif isinstance(oper_with_result, ClientOperCancel):
                if oper_with_result.result.success:
                    self._need_push = True

            else:
                message_box_error('Invalid oper with result', oper_with_result)

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
    client_oper_query_all = ClientOperQuery(info_type=ClientConstant.account_info)
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
