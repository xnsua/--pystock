from data_parser import data_parser_163
from stock_querier import stock_querier_163
from utilities.import_basic import *

_szzs_163 = '0000001'
_szzs_filename = '000001.sh.csv'
_szzs_filepath = str(config.get_project_root() / 'data' / 'data_163' / _szzs_filename)


def read_date_map():
    df = data_parser_163.read_stock(_szzs_filepath)
    datecol = df['日期']
    lastday = df.loc[0, '日期']
    if lastday.to_pydatetime().date() != dt.datetime.now().date():
        dfmore = stock_querier_163.wget_stock_history(_szzs_163, startdate=lastday.to_pydatetime().date())

    ldate = datecol.iloc(0)

    date_dict = {}
    for v in enumerate(reversed(datecol)):
        date_dict[v[0]] = v[1].to_pydatetime()
        date_dict[v[1].to_pydatetime()] = 0
    return date_dict


def query_date_map():
    stock_querier_163.download_stock_history(_szzs_163, _szzs_filepath)
    # df = read_stock(_szzs_filepath)


def main():
    query_date_map()


if __name__ == '__main__':
    main()
