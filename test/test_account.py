from unittest import TestCase
from include.basic_structure import *


class TestAccount(TestCase):
    def test_equality(self):
        account = Account()
        account.total = 2
        account2 = Account()
        self.assertNotEqual(account, account2)

