from datetime import datetime
from unittest import TestCase

from nose.tools import *

from include.basic_structure import *


class TestStock(TestCase):
    def test_amount(self):
        stock = Stock()
        self.assertEqual(stock.amount, 0)
        stock.amount = 1
        self.assertEqual(stock.amount, 1)

    @raises(AssertionError)
    def test_buy_time_assert(self):
        stock = Stock()
        stock.datetime = '1'

    @raises(AssertionError)
    def test_name_assert(self):
        stock = Stock()
        stock.name = 1

    @raises(AssertionError)
    def test_amount_assert(self):
        stock = Stock()
        stock.amount = '1'

    def test_buy_time(self):
        stock = Stock()
        self.assertEqual(stock.datetime, datetime.fromtimestamp(0))
        now = datetime.now()
        stock.datetime = now
        self.assertEqual(stock.datetime, now)

    def test_name(self):
        stock = Stock()
        self.assertEqual(stock.name, '')
        stock.name = 'sci'
        self.assertEqual(stock.name, 'sci')
