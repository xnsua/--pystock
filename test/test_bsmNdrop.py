from unittest import TestCase

from nose.tools import *

from trade.bsm_ndrop import *


class TestBsmNdrop(TestCase):
    def test_calc_buy_array(self):
        drdata = [0, 1, 0, 0, 1, 1, 0, 1]
        obj = BsmNdrop(drdata, 1)
        arr = obj.calc_buy_array()
        self.assertEqual(list(arr), [0, 1, 0, 1, 1, 0, 0, 1])

        obj = BsmNdrop(drdata, 2)
        arr = obj.calc_buy_array()
        self.assertEqual(list(arr), [0, 0, 0, 0, 1, 0, 0, 0])

    def test_isbuy(self):
        drdata = [0]
        bsm = BsmNdrop(drdata, 1)
        self.assertEqual(False, bsm.isbuy(0))
        drdata = [0, 0]
        bsm = BsmNdrop(drdata, 2)
        self.assertEqual(False, bsm.isbuy(1))

    @raises(ParamCheckException)
    def test_isbuy_exception(self):
        drdata = [0, 1, 0]
        bsm = BsmNdrop(drdata, 1)
        bsm.isbuy(-1)

    @raises(ParamCheckException)
    def test_construct(self):
        bsm = BsmNdrop([], 0)
        del bsm

    @raises(ParamCheckException)
    def test_isbuy_exception(self):
        drdata = [0, 1, 0]
        bsm = BsmNdrop(drdata, 1)
        bsm.isbuy(3)
