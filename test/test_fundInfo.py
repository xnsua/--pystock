from unittest import TestCase

from include import fund_info
from include.fund_info import ManagerInfo


class TestFundInfo(TestCase):
    def test_json_functions(self):
        finfo = fund_info.FundInfo()
        finfo.name = 'name1'
        finfo.managers = []
        finfo.managers.append(ManagerInfo())
        finfo.to_file('fmanager.test')
        finfo2 = fund_info.FundInfo.from_file('fmanager.test')

        assert finfo == finfo2
