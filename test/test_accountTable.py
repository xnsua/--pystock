import os
from unittest import TestCase

from database.table_manager import TableManager
from include.basic_structure import Account


class TestAccountTable(TestCase):
    dbfilename = 'test.db'

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove(self.dbfilename)
        except OSError:
            pass

    def get_account1(self) -> Account:
        account = Account()
        account.total = 5.0
        account.free = 2
        account.drawable = 3
        account.frozen = 2.0
        account.withdraw = 2.0
        account.deposit = 1.0
        return account

    def test_read_save_account(self):
        tm = TableManager()
        account_table = tm.account_table
        account1 = self.get_account1()
        account_table.save_account(account1)
        account2 = account_table.read_account()
        self.assertEqual(account1, account2)
