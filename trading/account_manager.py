import threading

from common.alert import message_box_error, message_box_error_if
from ip.st import AccountInfo, ClientOperBase, QueryResult, BuyResult, SellResult, \
    CancelEntrustResult
from project_helper.logbook_logger import mylog


class AccountManager:
    # imp Check all function use the lock
    def __init__(self):
        self._account_info = None  # type: AccountInfo
        self._lock = threading.RLock()
        self.need_push = None

    def set_account_info(self, account_info: AccountInfo):
        with self._lock:
            self._account_info = account_info

    def _on_oper_query(self, result_data):
        if isinstance(result_data, AccountInfo):
            self._account_info = result_data
            self.need_push = False
        message_box_error('Invalid result', repr(result_data))

    def on_operation_result(self, oper_with_result: ClientOperBase):
        with self._lock:
            result = oper_with_result.result
            if isinstance(result, QueryResult):
                message_box_error_if(not result.success, 'Result is not success', result)
                self._on_oper_query(result.data)
            elif type(result) in [BuyResult, SellResult, CancelEntrustResult]:
                self.need_push = True
            else:
                message_box_error('Invalid result', result)

    @property
    def available(self):
        with self._lock:
            return self._account_info.available

    def get_entrust_item(self, entrust_id):
        with self._lock:
            item = [val for val in self._account_info.entrust_items
                    if val.entrust_id == entrust_id]
            if item: mylog.info(f'Can not find entrust for id:{entrust_id}')
            return item[0]

    @property
    def entrust_items(self):
        with self._lock:
            return self._account_info.entrust_items

    @property
    def share_items(self):
        with self._lock:
            return self.share_items
