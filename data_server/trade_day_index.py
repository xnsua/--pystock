import datetime as dt

import pandas as pd

import common.helper as hp
from config_module import myconfig
from data_server.stock_querier import _163_api
from stock_basic.stock_constant import stock_startday

_szzs_163 = '0000001'
_szzs_filename = '000001.sh.csv'
_szzs_filepath = str(
    myconfig.project_root / 'data_server' / 'data_163' / _szzs_filename)


def update__date_map():
    try:
        df = pd.read_csv(_szzs_filepath, encoding='gbk', index_col=0)
        lastday = dt.datetime.strptime(df['日期'].iloc[0], '%Y-%m-%d').date()
    except FileNotFoundError:
        df = None
        lastday = stock_startday
    dfmore = []
    if lastday != dt.date.today():
        dfmore = _163_api.wget_stock_history(_szzs_163,
                                             startdate=hp.ndays_later(1,
                                                                      lastday))
    dfall = pd.concat([dfmore, df], ignore_index=True)  # type: pd.DataFrame
    dfall.to_csv(_szzs_filepath, encoding='gbk')

    datecol = dfall['日期']
    datecol = [dt.datetime.strptime(val, '%Y-%m-%d').date() for val in datecol]
    date_dict = {}
    for v in enumerate(reversed(datecol)):
        date_dict[v[0]] = v[1]
        date_dict[v[1]] = v[0]
    return date_dict


def query_date_map():
    _163_api.download_stock_history(_szzs_163, _szzs_filepath, hp.ndays_ago(12),
                                    hp.ndays_ago(6))


def main():
    date_dict = update__date_map()
    for val in date_dict.items():
        print(val)


if __name__ == '__main__':
    main()
