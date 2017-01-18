from datetime import datetime

from fund_querier.easy_money_querier import easy_money_querier
from include.fund_info import FundInfo


class FundQuerier:
    def query_all(self):
        fcodes = easy_money_querier.query_all_fund_code()
        for fcode in fcodes:
            fcode = '000001'
            fundinfo = easy_money_querier.query_fund_info(fcode)
            fundinfo.query_date = datetime.now()
            fundinfo.to_file('jtt.txt')
            ss = fundinfo.to_json()
            fundinfo2 = FundInfo.from_string(ss)
            print(fundinfo2)
            print((fundinfo2.managers[1].names))
            break


fund_querier = FundQuerier()
if __name__ == '__main__':
    fund_querier.query_all()
