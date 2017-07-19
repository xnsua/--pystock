import datetime
import os

s_time = datetime.datetime.now()
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy


from common.helper import dt_now
from common.scipy_helper import pdDF
from common_stock.py_dataframe import DayDataRepr
from common_stock.stock_helper import to_stdcode



class RqDataProxy:
    def __init__(self):
        self._dp = DataProxy(BaseDataSource(os.path.expanduser('~/.rqalpha/bundle')))
        self._stock_to_instruments = self._dp.all_instruments('CS')
        self._index_to_instrument = self._dp.all_instruments('INDX')
        self._etf_stdcode_to_instrument = self._dp.all_instruments('ETF')
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
        """
        Instrument(sector_code_name='金融', symbol='平安银行', listed_date=datetime.datetime(1991, 4, 3, 0, 0),
         special_type='Normal', exchange='XSHE', round_lot=100.0, industry_code='J66', abbrev_symbol='PAYH', 
         board_type='MainBoard', de_listed_date=datetime.datetime(2999, 12, 31, 0, 0), 
         concept_names='基金重仓|深圳本地|外资背景|社保重仓|本月解禁|保险重仓|券商重仓', status='Active', 
         order_book_id='000001.XSHE', sector_code='Financials', industry_name='货币金融服务', type='CS')
        """
        self._stockcode_to_instrument = {to_stdcode(item.order_book_id):
                                             item for item in self._stock_to_instruments}
        self._etf_stdcode_to_instrument = {to_stdcode(item.order_book_id): item
                                           for item in self._etf_stdcode_to_instrument}

        self._index_to_instrumment = {}
        for val in self._index_to_instrument:
            if val.order_book_id.endswith('.INDX'): continue
            self._index_to_instrumment[to_stdcode(val.order_book_id)] = val
        self._all_code_to_instrument = {**self._stockcode_to_instrument,
                                        **self._etf_stdcode_to_instrument,
                                        **self._index_to_instrumment}

        self._symbol_to_stdcode = {value.symbol: key for key, value in
                                   self._all_code_to_instrument.items()}
        self._abbre_symbol_to_stdcode = {value.abbrev_symbol: key for key, value in
                                         self._all_code_to_instrument.items()}
        self._all_symbol_to_stdcode = {**self._symbol_to_stdcode, **self._abbre_symbol_to_stdcode}
        self._all_symbol_to_stdcode['中证500'] = self._all_symbol_to_stdcode['中证500(沪)']

    def instrument_of(self, code):
        return self._all_code_to_instrument[code]

    def name_of(self, code, default=None):
        try:
            return self.instrument_of(code).symbol
        except:
            return default

    def ddr_of(self, code):
        code = self._all_code_to_instrument[code].order_book_id
        data = self._dp.history_bars(code, 100000, '1d',
                                     ['datetime', 'open', 'close', 'high', 'low', 'volume'],
                                     dt_now())
        df = pdDF(data)
        df.datetime = df.datetime // 1000000
        df = df.set_index('datetime')
        return DayDataRepr(code, df)

    def is_etf(self, std_code):
        return std_code in self._etf_stdcode_to_instrument

    # def sz50_component_stdcodes(self):
    #     codes = sz50_to_name
    #     return [to_stdcode(code) for code in codes]
    #
    # def hs300_component_stdcodes(self):
    #     codes = hs300_to_name
    #     return [to_stdcode(code) for code in codes]
    #
    # def zz500_component_stdcodes(self):
    #     codes = zz500_to_name
    #     return [to_stdcode(code) for code in codes]

    def symbol_to_code(self, symbol):
        return self._all_symbol_to_stdcode[symbol]


grq_data = RqDataProxy()


def main():
    # noinspection PyProtectedMember
    data = grq_data._dp.all_instruments('CS')
    cl = [item.order_book_id for item in data]
    val = grq_data.ddr_of('sh000001').df
    print(val)
    print(len(cl))
    # print(cl)
    # print(grq_data._dp.history_bars('000001.XSHG', 10, '1d', None, dt_now()))
    # print(grq_data._index_to_instrumment)
    # print(grq_data.symbol_to_code('50GXD'))
    pass


if __name__ == '__main__':
    main()
