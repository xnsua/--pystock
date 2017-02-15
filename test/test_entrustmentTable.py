import os
from datetime import datetime
from unittest import TestCase

from database.table_manager import TableManager
from include.basic_structure import Entrustment
from test.config_for_test import test_db_path
from trade.utilities.global_variable import constant


class TestEntrustmentTable(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove(test_db_path)
        except OSError:
            pass

    @staticmethod
    def get_today_entrustment():
        item = Entrustment()
        item.datetime = datetime.now()
        item.id = '123546231'
        item.code = '000001'
        item.name = 'SCI'
        item.operation = constant.oper_buy
        return item

    @staticmethod
    def get_entrustment1():
        item = Entrustment()
        item.datetime = datetime.fromtimestamp(1000)
        item.id = '123546231'
        item.code = '000001'
        item.name = 'SCI'
        item.operation = constant.oper_buy
        return item

    def test_read_today_entrustment(self):
        tm = TableManager(test_db_path)
        entrustment_table = tm.entrustment_table

        entrustment1 = self.get_entrustment1()
        entrustment_table.save_entrustment(entrustment1)
        entrustment_today = self.get_today_entrustment()
        entrustment_table.save_entrustment(entrustment_today)

        entrustments = entrustment_table.read_today_entrusment()
        self.assertEqual(1, len(entrustments))
        self.assertEqual(entrustment_today, entrustments[0])

    def test_read_save_entrustment(self):
        tm = TableManager(test_db_path)
        entrustment_table = tm.entrustment_table
        entrustment1 = self.get_entrustment1()
        entrustment_table.save_entrustment(entrustment1)

        entrustments = entrustment_table.read_entrustment()
        self.assertEqual(1, len(entrustments))
        self.assertEqual(entrustment1, entrustments[0])
