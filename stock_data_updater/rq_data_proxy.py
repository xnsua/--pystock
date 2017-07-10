import os

from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy

from common.helper import dt_now
from common.scipy_helper import pdDF
from common_stock.py_dataframe import DayDataRepr
from common_stock.stock_helper import to_stdcode, to_num_code
from stock_data_updater.classify import sz50_to_name, hs300_to_name, zz500_to_name


class RqDataProxy:
    def __init__(self):
        self._dp = DataProxy(BaseDataSource(os.path.expanduser('~/.rqalpha/bundle')))
        self._instruments = self._dp.all_instruments('CS')
        self._index = self._dp.all_instruments('INDX')
        """
        Instrument(sector_code_name='金融', symbol='平安银行', listed_date=datetime.datetime(1991, 4, 3, 0, 0),
         special_type='Normal', exchange='XSHE', round_lot=100.0, industry_code='J66', abbrev_symbol='PAYH', 
         board_type='MainBoard', de_listed_date=datetime.datetime(2999, 12, 31, 0, 0), 
         concept_names='基金重仓|深圳本地|外资背景|社保重仓|本月解禁|保险重仓|券商重仓', status='Active', 
         order_book_id='000001.XSHE', sector_code='Financials', industry_name='货币金融服务', type='CS')
        """
        self._stdcode2instrument = {to_stdcode(item.order_book_id): item for item in
                                    self._instruments}
        self._index2instrumment = {
            to_stdcode(to_num_code(item.order_book_id) + '.' + item.exchange): item
            for item in self._index if item.exchange}

        self._stdcode_index2instrument = {**self._stdcode2instrument, self._index2instrumment}

        self._symbol2stdcode = {value.symbol: key for key, value in
                                self._stdcode_index2instrument.items()}
        self._abbre_symbol2stdcode = {value.abbrev_symbol: key for key, value in
                                      self._stdcode_index2instrument.items()}
        self._all_symbol2stdcode = {**self._symbol2stdcode, **self._abbre_symbol2stdcode}

    def instrument_of(self, code):
        return self._stdcode_index2instrument[code]

    def name_of(self, code, default=None):
        try:
            return self.instrument_of(code).symbol
        except:
            return default

    def ddr_of(self, code):
        code = self._stdcode_index2instrument[code].order_book_id
        data = self._dp.history_bars(code, 100000, '1d',
                                     ['datetime', 'open', 'close', 'high', 'low', 'volume'],
                                     dt_now())
        df = pdDF(data)
        df.datetime = df.datetime // 1000000
        df = df.set_index('datetime')
        return DayDataRepr(code, df)

    def index_components(self, code):
        raise Exception('Not implemented')

    def all_index_instrument(self):
        return self._dp.all_instruments('INDX')

    def all_index_code(self):
        return self._index_code2instrumment.keys()

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
        return [to_stdcode(code) for code in codes]

    def hs300_components(self):
        codes = hs300_to_name
        return [to_stdcode(code) for code in codes]

    def zz500_components(self):
        codes = zz500_to_name
        return [to_stdcode(code) for code in codes]

    def symbol2code(self, symbol):
        if symbol in self._abbre_symbol2stdcode:
            return self._abbre_symbol2stdcode[symbol]
        elif symbol in self._symbol2stdcode:
            return self._symbol2stdcode[symbol]
        else:
            raise Exception('Not valid symbol')


grq_data = RqDataProxy()


def main():
    print(grq_data.symbol2code('50GXD'))


if __name__ == '__main__':
    main()
