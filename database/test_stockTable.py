import os
from datetime import datetime
from unittest import TestCase

from database.table_manager import TableManager
from database.test_config import test_db_path
from include.basic_structure import Stock


class TestStockTable(TestCase):
    def setUp(self):
        if (os.path.exists(test_db_path)):
            os.remove(test_db_path)
        pass

    def tearDown(self):
        try:
            os.remove(test_db_path)
        except OSError:
            pass

    @staticmethod
    def get_stock1():
        stock = Stock()
        stock.datetime = datetime.fromtimestamp(1000)
        stock.name = 'SCI'
        stock.code = '000001'
        stock.amount = '1000'
        return stock

    @staticmethod
    def get_stock2():
        stock = Stock()
        stock.datetime = datetime.fromtimestamp(10000)
        stock.name = 'SCI_2'
        stock.code = '000001_2'
        stock.amount = '1000_2'
        return stock

    def test_read_save_stocks(self):
        tm = TableManager(test_db_path)
        stock_table = tm.stock_table
        stock1 = self.get_stock1()
        stock_table.save_stock(stock1)

        stocks = stock_table.read_stocks()
        self.assertEqual(stock1, stocks[0])

        stock2 = self.get_stock2()
        stock_table.save_stock(stock2)

        stocks = stock_table.read_stocks()
        self.assertEqual(len(stocks), 2)

        self.assertEqual(set(stocks), {stock1, stock2})
