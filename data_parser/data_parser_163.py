from common.helper import time_exec
from utilities import stock_time
from utilities.import_basic import *
from utilities.import_scipy import *


def read_stock(path):
    foo1 = dt.datetime.now()
    df = pd.read_csv(path, encoding='gbk', parse_dates=['日期'])
    return df


def main():
    time_exec(lambda: stock_time.read_date_map())
    pass


if __name__ == '__main__':
    main()
