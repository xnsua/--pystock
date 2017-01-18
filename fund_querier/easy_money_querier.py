# todo
import datetime

import dateutil.parser
import requests_cache
from lxml import etree
from pyquery import PyQuery

from common.string_helper import find_date_substr
from include.fund_info import ManagerInfo, FundInfo

requests_cache.install_cache('demo_cache', expire_after=datetime.timedelta(days=1))

from typing import List

from common.web_helper import url_to_pyquery, firefox_get_url


class EasyMoneyQuerier:
    @staticmethod
    def query_all_fund_code() -> List[str]:
        py = url_to_pyquery('http://fund.eastmoney.com/allfund.html')
        elems = py('ul.num_right>li>div>a:first')
        fund_codes = []
        for elem in elems.items():
            # From 'http://fund.eastmoney.com/100016.html
            # To 100016
            href = elem.attr('href')
            code = href.replace('http://fund.eastmoney.com/', '')
            code = code.replace('.html', '')
            fund_codes.append(code)
        return fund_codes

    def query_fund_info(self, fundcode: str) -> FundInfo:
        fund_info = FundInfo()
        fmt = 'http://fund.eastmoney.com/{}.html'
        url = fmt.format(fundcode)
        response = firefox_get_url(url)
        urltext = response.content.decode('utf-8')
        py = PyQuery(urltext)

        rate_info = py(
            '#body > div:nth-child(12) > div > div > div.fundDetail-main > div.fundInfoItem > div.infoOfFund > table  > tr:nth-child(2) > td:nth-child(3) > div')
        rate_map = {'jjpj': 0, 'jjpj1': 1, 'jjpj2': 2, 'jjpj3': 3, 'jjpj4': 4, 'jjpj5': 5}
        fund_info.rate = rate_map[rate_info.attr('class')]
        # print(fund_info.rate)
        fund_info.netvalue = py(
            '#body > div:nth-child(12) > div > div > div.fundDetail-main > div.fundInfoItem > div.dataOfFund > dl.dataItem03 > dd.dataNums > span').text()
        # print(fund_info.netvalue)
        fund_info.type = py(
            '.infoOfFund > table:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)').text()
        # print(fund_info.type)

        time_html = py(
            '#body > div:nth-child(12) > div > div > div.fundDetail-main > div.fundInfoItem > div.infoOfFund > table  > tr:nth-child(2) > td:nth-child(1)').text()
        time_str = find_date_substr(time_html)
        fund_info.start_time = dateutil.parser.parse(time_str)
        # print(fund_info.start_time)

        managers = py('#fundManagerTab > div:nth-child(1) > table ')
        # print(managers.outer_html())
        fund_info.managers = self.__parse_managers(managers.outer_html())
        # print(managers)
        return fund_info

    @staticmethod
    def __parse_managers(htm: str):
        py = PyQuery(htm)
        managers = []
        for idx, item in enumerate(py.children()):  # type: etree.Element
            if idx == 0: continue
            manager = ManagerInfo()
            for idx2, pitem in enumerate(map(PyQuery, item)):
                # print(pitem.text())
                htm = pitem.text()  # type:str
                if idx2 == 0:
                    se = htm.split(sep='~')
                    manager.start_time = dateutil.parser.parse(se[0])
                    if se[1] == '至今':
                        manager.end_time = datetime.datetime.max
                    else:
                        manager.start_time = dateutil.parser.parse(se[1])
                if idx2 == 1:
                    manager.names = htm.split(' ')
            managers.append(manager)
        return managers


easy_money_querier = EasyMoneyQuerier()

if __name__ == '__main__':
    val = easy_money_querier.query_fund_info('519983')
    print(val)
    allfc = easy_money_querier.query_all_fund_code()
    print(allfc)
