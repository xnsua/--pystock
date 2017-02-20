from common.helper import time_exec
from utilities import trade_day_index
from utilities.import_basic import *
from utilities.import_scipy import *


def read_stock(path):
    foo1 = dt.datetime.now()
    df = pd.read_csv(path, encoding='gbk', index_col=0)
    return df


def main():
    time_exec(lambda: trade_day_index.read_date_map())
    pass


if __name__ == '__main__':
    main()
