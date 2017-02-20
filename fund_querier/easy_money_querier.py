import datetime
import json
from typing import List, Tuple

import dateutil.parser
from lxml import etree
from pyquery import PyQuery

from common.helper import find_date_substr
from common.log_helper import logger
from common.web_helper import firefox_get_url
from include.fund_info import ManagerInfo, FundInfo


class EasyMoneyQuerier:
    def wget_all_stockfund_code(self) -> List[str]:
        codes, page_count = self.wget_stockfund_code_for_page(1)
        for i in range(2, page_count + 1):
            pcodes, _ = self.wget_stockfund_code_for_page(i)
            codes.extend(pcodes)
        return codes

    def wget_stockfund_code_for_page(self, page_index) -> Tuple[List[str], int]:
        #     http://fundapi.eastmoney.com/fundtradenew.aspx?ft=pg&sc=1n&st=desc&pi=2&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=undefined
        # pi = page index
        urlfmt = 'http://fundapi.eastmoney.com/fundtradenew.aspx?ft=pg&sc=1n&st=desc&pi={}&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=undefined'
        url = urlfmt.format(page_index)
        res = firefox_get_url(url)
        codes = self._parse_stock_fund_code_for_page(res.text)
        page_count = self._parse_stock_fund_page_count(res.text)
        return codes, page_count

    def _parse_stock_fund_code_for_page(self, content: str):
        pos1 = content.index('[')
        pos2 = content.rindex(']')
        content = content[pos1: pos2 + 1]
        code_list = json.loads(content)
        retvalue = []
        for item in code_list:
            retvalue.append(item.split('|')[0])
        return retvalue

    def _parse_stock_fund_page_count(self, content: str):
        pos1 = content.index('allPages')
        pos2 = content.rindex('}')
        content = content[pos1:pos2]
        page_count = content.split(':')[1]
        return int(page_count)

    def wget_fund_info(self, fundcode: str) -> FundInfo:
        fund_info = FundInfo()
        fmt = 'http://fund.eastmoney.com/{}.html'
        url = fmt.format(fundcode)
        logger.info(url)
        response = firefox_get_url(url)
        urltext = response.content.decode('utf-8')
        py = PyQuery(urltext)

        rate_info = py('.jjpj, jjpj1, jjpj2, jjpj3, jjpj4, jjpj5')
        if (rate_info.size() == 1):
            rate_info = rate_info[0]
        rate_map = {'jjpj': 0, 'jjpj1': 1, 'jjpj2': 2, 'jjpj3': 3, 'jjpj4': 4, 'jjpj5': 5}
        fund_info.rate = rate_map[py(rate_info).attr('class')]
        fund_info.netvalue = py(
            '#body > div:nth-child(12) > div > div > div.fundDetail-main > div.fundInfoItem > div.dataOfFund > dl.dataItem03 > dd.dataNums > span').text()
        fund_info.type = py(
            '.infoOfFund > table:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)').text()

        time_html = py(
            'div.infoOfFund > table > tr:nth-child(2) > td:nth-child(1)').text()
        time_str = find_date_substr(time_html)
        fund_info.start_time = dateutil.parser.parse(time_str)

        managers = py('#fundManagerTab > div:nth-child(1) > table ')
        fund_info.managers = self.__parse_managers(managers.outer_html())
        return fund_info

    @staticmethod
    def __parse_managers(htm: str):
        py = PyQuery(htm)
        managers = []
        for idx, item in enumerate(py.children()):  # type: etree.Element
            if idx == 0: continue
            manager = ManagerInfo()
            for idx2, pitem in enumerate(map(PyQuery, item)):
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
    try:
        val = easy_money_querier.wget_fund_info('003954')
    except Exception as e:
        print(str(e))
