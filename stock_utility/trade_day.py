import datetime as dt

import pandas as pd

from config_module import myconfig


class TradeDay:
    def __init__(self):
        self.df = self.read_df()
        self.date_map = self.build_date_map()

    def read_df(self):
        # path = plPath(__file__).parent / 'trade_day.csv'
        path = myconfig.project_root / 'stock_utility/trade_day.csv'
        return pd.read_csv(str(path), index_col='index')

    def build_date_map(self):
        date_map = {}
        for i in range(len(self.df.index)):
            date_map[self.df.iat[i, 0]] = i
        return date_map

    def is_trade_day(self, date_: dt.date):
        row_num = self.date_map[str(date_)]
        return self.df.iat[row_num, 1]

    def last_n_trade_day(self, date_: dt.date, days_num):
        row_num = self.date_map[str(date_)]
        n_trade_days = []
        while 1:
            if len(n_trade_days) == days_num:
                break
            if self.df.iat[row_num, 1]:
                date_str = self.df.iat[row_num, 0]
                n_trade_days.append(dt.date(*map(int, date_str.split('-'))))
            row_num -= 1
        return list(reversed(n_trade_days))


_trade_day = TradeDay()
is_trade_day = _trade_day.is_trade_day
last_n_trade_day = _trade_day.last_n_trade_day
