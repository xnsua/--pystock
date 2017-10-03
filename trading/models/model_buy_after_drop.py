import pathlib
from random import choice

from stock_data_manager.day_data_updater import SingleStockUpdater

from common.helper import dt_today, dt_now
from common.key_value_db import KeyValueDb
from common.scipy_helper import pdDF
from ip.st import EntrustType, ClientOperCancel, EntrustWay, ClientOperSell, ClientOperBuy
from project_config.logbook_logger import mylog
from trading.abstract_context import AbstractContext
from trading.models.abstract_model import AbstractModel


class BadData:
    def __init__(self, path):
        self.db = KeyValueDb(path)
        self.opers = []
        self.entrusts = []
        self.key = str(dt_today())

    def add_operation(self, oper):
        self.opers.append((oper, dt_now()))
        self.db[self.key] = (self.opers, self.entrusts)

    def add_entrusts(self, entrust):
        self.opers.append((entrust, dt_now()))
        self.db[self.key] = (self.opers, self.entrusts)

    def query_operation(self):
        return [oper[0] for oper in self.opers]


class ModelBuyAfterDrop(AbstractModel):
    @classmethod
    def name(cls):
        return '__MODEL_BAD'

    def __init__(self):
        super().__init__()
        self.etf_codes = ['510050', '510900']
        self.etf_dict = None
        self.etf_to_buy = None

        self._push_times = 0

        path = pathlib.Path(__file__).parent / 'model_buy_after_drop.sqlite'
        self.db = BadData(str(path))

    def log_account_info(self):
        pass
        # toch
        # try:
        #     log_str = f'ACCOUNT_INFO: ' \
        #               f'Available: {self.account_manager.available}  ' \
        #               f'ShareCount: {len(self.account_manager.share_items)}  ' \
        #               f'EntrustCount: {len(self.account_manager.entrust_items)}  '
        #     mylog.info(log_str)
        # except Exception as e:
        #     # noinspection PyProtectedMember
        #     mylog.info(
        #         f'*** There is NO account info {self.account_manager._account_info}, Exception: {e}')

    def init_model(self, context):
        self.log_account_info()
        mylog.debug('Init model')
        self.etf_to_buy = ['510900', '510050']
        context.set_realtime_stocks(self.etf_to_buy)
        self.etf_dict = read_df_dict(self.etf_codes)
        # toch
        # self.etf_to_buy = query_stock_to_buy(self.etf_dict, datetime.datetime.now())

    def on_bid_over(self, context, rdr: pdDF):
        self.log_account_info()
        mylog.info('On bid over\n' + str(rdr))
        assert all(rdr.open)

    def handle_bar(self, context, rdr):
        #        open    yclose  price  high   low   name
        # 510900  1.152   1.145  1.151  1.157  1.149  H股ETF
        # 510050  2.490   2.490  2.472  2.494  2.466  50ETF
        mylog.info('On handle bar --------')

        self._push_times += 1
        if self._push_times / 2 != 1:
            # toch
            pass
            # return
        mylog.notice('On handle bar operation')
        prices1 = [val / 1000 + rdr.price[0] for val in range(-5, 5)]
        prices2 = [val / 1000 + rdr.price[1] for val in range(-5, 5)]
        stock_price = [(rdr.index[0], prices1), (rdr.index[1], prices2)]

        def select_price_code():
            sp = choice(stock_price)
            price = choice(sp[1])
            return sp[0], float(price)

        def buy_stock():
            mylog.notice('Begin buy operation .........')
            stock_code, price = select_price_code()
            mylog.error(f'-----------{stock_code}, {price}')
            oper_buy = ClientOperBuy(stock_code, price, 100, EntrustType.FIXED_PRICE)
            context.send_oper(oper_buy)
            self.db.add_operation(oper_buy)
            mylog.notice(f'Buy operation result \n {oper_buy.result}')

        def sell_stock():
            mylog.notice('Begin sell operation .........')
            stock_code, price = select_price_code()
            oper_sell = ClientOperSell(stock_code, price, 100, EntrustType.FIXED_PRICE)
            context.send_oper(oper_sell)
            self.db.add_operation(oper_sell)
            mylog.notice(f'Sell operation result \n {oper_sell.result}')

        def cancel_operation():
            mylog.notice('Begin cancel operation .........')
            if not self.db.query_operation(): return
            oper = choice(self.db.query_operation())
            if isinstance(oper, ClientOperBuy) and oper.result.success:
                cancel_oper = ClientOperCancel(oper.result.entrust_id, oper.stock_code,
                                               EntrustWay.way_buy)
            elif isinstance(oper, ClientOperSell) and oper.result.success:
                cancel_oper = ClientOperCancel(oper.result.entrust_id, oper.stock_code,
                                               EntrustWay.way_sell)
            else:
                return
            context.send_oper(cancel_oper)
            mylog.notice(f'Cancel operation result {cancel_oper}')
            self.db.add_operation(cancel_oper)

        func_list = [buy_stock, sell_stock, cancel_operation]
        func = choice(func_list)
        func()

    def on_trade_over(self, context: AbstractContext, rdr: pdDF):
        pass


def read_df_dict(etfs):
    etf_dict = {}
    for etf in etfs:
        etf_dict[etf] = SingleStockUpdater.read_etf_day_data(etf)
    return etf_dict
