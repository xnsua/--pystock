import os

from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy

from common.helper import dt_now
from common.scipy_helper import pdDF
from common_stock.py_dataframe import DayDataRepr
from stock_data_updater.classify import sz50_to_name, hs300_to_name, zz500_to_name


class RqDataProxy:
    def __init__(self):
        self._dp = DataProxy(BaseDataSource(os.path.expanduser('~/.rqalpha/bundle')))
        self._instruments = self._dp.all_instruments('CS')
        """
        Instrument(sector_code_name='金融', symbol='平安银行', listed_date=datetime.datetime(1991, 4, 3, 0, 0),
         special_type='Normal', exchange='XSHE', round_lot=100.0, industry_code='J66', abbrev_symbol='PAYH', 
         board_type='MainBoard', de_listed_date=datetime.datetime(2999, 12, 31, 0, 0), 
         concept_names='基金重仓|深圳本地|外资背景|社保重仓|本月解禁|保险重仓|券商重仓', status='Active', 
         order_book_id='000001.XSHE', sector_code='Financials', industry_name='货币金融服务', type='CS')
        """
        self._pcode2instrument = {item.order_book_id[0:6]: item for item in self._instruments}
        self._rqcode2instrument = {item.order_book_id: item for item in self._instruments}
        self.mix_code2instrument = {**self._pcode2instrument, **self._rqcode2instrument}
        print(len(self._pcode2instrument), len(self._rqcode2instrument),
              len(self.mix_code2instrument))

    def instrument_of(self, code):
        return self.mix_code2instrument[code]

    def ddr_of(self, code):
        data = self._dp.history_bars(code, 100000, '1d',
                                     ['datetime', 'open', 'close', 'high', 'low', 'volume'],
                                     dt_now())
        df = pdDF(data)
        df.datetime = df.datetime // 1000000
        df = df.set_index('datetime')
        return DayDataRepr(code, df)

    def to_rqcode(self, code):
        return self.mix_code2instrument[code].order_book_id

    def index_components(self, code):
        raise Exception('Not implemented')

    def all_indexs(self):
        return self._dp.all_instruments('INDX')

    def all_etfs(self):
        """
        CS	Common Stock, 即股票
        ETF	Exchange Traded Fund, 即交易所交易基金
        LOF	Listed Open-Ended Fund，即上市型开放式基金
        FenjiMu	Fenji Mu Fund, 即分级母基金
        FenjiA	Fenji A Fund, 即分级A类基金
        FenjiB	Fenji B Funds, 即分级B类基金
        INDX	Index, 即指数
        Future	Futures，即期货，包含股指、国债和商品期货
        """
        return self._dp.all_instruments('ETF')

    def all_lof(self):
        return self._dp.all_instruments('LOF')

    def sz50_components(self):
        codes = sz50_to_name
        return [self.to_rqcode(code) for code in codes]

    def hs300_components(self):
        codes = hs300_to_name
        return [self.to_rqcode(code) for code in codes]

    def zz500_components(self):
        codes = zz500_to_name
        return [self.to_rqcode(code) for code in codes]


rq_data = RqDataProxy()

val = rq_data.sz50_components()
for v in val:
    print(v)
