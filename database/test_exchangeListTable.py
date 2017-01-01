import os
from datetime import datetime
from unittest import TestCase

from database.table_manager import TableManager
from database.test_config import test_db_path
from include.basic_structure import ExchangeList


class TestExchangeListTable(TestCase):
    def setUp(self):
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def tearDown(self):
        try:
            os.remove(test_db_path)
        except OSError:
            pass

    def get_exchange_list1(self):
        item = ExchangeList()
        item.time = datetime.fromtimestamp(10000)
        item.id = '64453431'
        item.code = '000001'
        item.name = 'SCI'
        item.commission = 10
        item.tax = .0
        item.money_changed = 200000.0
        item.money_remain = 10000.0
        item.price = 1.
        item.transfer_fee = .0
        return item

    def test_read_save_exchange_list(self):
        tm = TableManager(test_db_path)
        table = tm.exchange_list_table
        exchange_list1 = self.get_exchange_list1()
        table.save_exchange_list(exchange_list1)
        exchange_lists = table.read_exchange_list()
        print(exchange_list1)
        print(exchange_lists)
        self.assertEqual(len(exchange_lists), 1)
        self.assertEqual(exchange_list1, exchange_lists[0])
