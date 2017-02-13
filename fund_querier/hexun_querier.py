from datetime import datetime

import dateutil.parser
import pandas
import requests
from pyquery import PyQuery

from common.log_helper import logger


class HexunQuerier:
    # http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=161831&startdate=2015-11-21&enddate=2018-12-08
    HEXUN_URL = 'http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode={}&startdate={}&enddate={}'

    def get_fund_history(self, fund_code, start_date=datetime.fromtimestamp(0).date(), end_date=datetime.now().date()):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        url = HexunQuerier.HEXUN_URL.format(fund_code, start_date, end_date)
        logger.info(url)
        rep = requests.get(url, timeout=3, headers=headers)
        df = self.__parse_response(rep.content)
        return df

    @staticmethod
    def __parse_response(content) -> pandas.DataFrame:
        pq = PyQuery(content)

        list_end_date = []
        end_dates = pq('fld_enddate')
        for date in end_dates:
            list_end_date.append(dateutil.parser.parse(date.text))

        list_netvalue = []
        netvalues = pq('fld_netvalue')
        for value in netvalues:
            list_netvalue.append(float(value.text))

        df = pandas.DataFrame({'date': list_end_date, 'value': list_netvalue})
        return df


hexun_querier = HexunQuerier()

if __name__ == '__main__':
    fund_history = hexun_querier.get_fund_history('001938')
