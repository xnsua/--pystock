import datetime
import os
from unittest import TestCase

from database.table_manager import TableManager
from database.test_config import test_db_path
from include.basic_structure import Account


class TestAccountTable(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove(test_db_path)
        except OSError:
            pass

    @staticmethod
    def get_account1() -> Account:
        account = Account()
        account.total = 5.0
        account.free = 2
        account.drawable = 3
        account.frozen = 2.0
        account.withdraw = 2.0
        account.deposit = 1.0
        account.datetime = datetime.datetime.fromtimestamp(100)
        return account

    @staticmethod
    def get_account2() -> Account:
        account = Account()
        account.total = 5.0
        account.free = 2
        account.drawable = 3
        account.frozen = 2.0
        account.withdraw = 2.0
        account.deposit = 1.0
        account.datetime = datetime.datetime.fromtimestamp(1000)
        return account

    def test_read_save_account(self):
        tm = TableManager(test_db_path)
        account_table = tm.account_table
        account1 = self.get_account1()
        account_table.save_account(account1)
        account2 = account_table.read_last_account()
        self.assertEqual(account1, account2)

    def test_read_save_multple_value(self):
        tm = TableManager(test_db_path)
        account_table = tm.account_table
        # Insert two and query two
        account1 = self.get_account1()
        account2 = self.get_account2()
        account_table.save_account(account1)
        account_table.save_account(account2)
        accounts = account_table.read_all()
        self.assertEqual(set(accounts), {account1, account2})

    def test_read_last_value(self):
        tm = TableManager(test_db_path)
        account_table = tm.account_table
        # Insert two and query two
        account1 = self.get_account1()
        account2 = self.get_account2()
        account_table.save_account(account1)
        account_table.save_account(account2)
        last_account = account_table.read_last_account()
        self.assertEqual(last_account, account2)
