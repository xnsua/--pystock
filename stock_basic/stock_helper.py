import datetime as dt

import tushare

from common import cache_util
from common.helper import ndays_later

stock_startday = dt.date(1990, 12, 19)
str_stock_startday = str(stock_startday)

stock_starttime = dt.datetime(1990, 12, 19)
stock_in_etf50 = ['600000', '600016', '600028', '600029',
                  '600030', '600036', '600048', '600050',
                  '600100', '600104', '600109', '600111',
                  '600485', '600518', '600519', '600547',
                  '600637', '600837', '600887', '600893',
                  '600958', '600999', '601006', '601088',
                  '601166', '601169', '601186', '601198',
                  '601211', '601288', '601318', '601328',
                  '601336', '601377', '601390', '601398',
                  '601601', '601628', '601668', '601688',
                  '601766', '601788', '601800', '601818',
                  '601857', '601901', '601985', '601988',
                  '601989', '601998']

etf_t0 = ['sh510900', 'sh513030', 'sh513050', 'sh513100', 'sh513500',
          'sh513600', 'sh513660']

etf_t1 = ['sh510010', 'sh510020', 'sh510030', 'sh510050', 'sh510060',
          'sh510070', 'sh510090', 'sh510110', 'sh510120', 'sh510130',
          'sh510150', 'sh510160', 'sh510170', 'sh510180', 'sh510190',
          'sh510210', 'sh510220', 'sh510230', 'sh510260', 'sh510270',
          'sh510280', 'sh510290', 'sh510410', 'sh510420', 'sh510430',
          'sh510300', 'sh510310', 'sh510330', 'sh510360', 'sh510500',
          'sh510510', 'sh510520', 'sh510560', 'sh510580', 'sh512000',
          'sh512010', 'sh512070', 'sh512100', 'sh512120', 'sh512210',
          'sh512220', 'sh512230', 'sh512300', 'sh512310', 'sh512330',
          'sh512340', 'sh512500', 'sh512510', 'sh512580', 'sh512600']


@cache_util.cache(cache_time_delta=dt.timedelta(days=1))
def is_trade_day(day=dt.date.today()):
    df = tushare.trade_cal()
    val = df[df.calendarDate == str(day)].iloc[0, 1]
    return val


def main():
    val = is_trade_day(ndays_later(2))
    print(val)


if __name__ == '__main__':
    main()
