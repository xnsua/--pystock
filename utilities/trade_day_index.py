import pandas as pd

from stock_querier import stock_querier_163
from utilities.import_basic import *
from utilities.stock_helper import stock_startday

_szzs_163 = '0000001'
_szzs_filename = '000001.sh.csv'
_szzs_filepath = str(config.get_project_root() / 'data' / 'data_163' / _szzs_filename)


def read_date_map():
    try:
        df = pd.read_csv(_szzs_filepath, encoding='gbk', index_col=0)
        lastday = dt.datetime.strptime(df['日期'].iloc[0], '%Y-%m-%d').date()
    except FileNotFoundError:
        df = None
        lastday = stock_startday
    dfmore = []
    if lastday != dt.date.today():
        dfmore = stock_querier_163.wget_stock_history(_szzs_163, startdate=hp.ndays_later(1, lastday))
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
    stock_querier_163.download_stock_history(_szzs_163, _szzs_filepath, hp.ndays_ago(12), hp.ndays_ago(6))


def main():
    date_dict = read_date_map()
    for val in date_dict.items():
        print(val)


if __name__ == '__main__':
    main()
