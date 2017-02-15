from utilities.import_basic import *
from utilities.import_scipy import *

def read_stock(path):
    df = pd.read_csv(path, encoding='gbk', parse_dates=['日期'])
    return df


def read_date_map():
    pn = config.get_project_root() / 'data' / '000001.sh.csv'
    df = read_stock(pn)
    datecol = df['日期']
    date_dict = {}
    for v in enumerate(reversed(datecol)):
        date_dict[v[0]] = v[1].to_pydatetime()
        date_dict[v[1].to_pydatetime()] = 0
    return date_dict


def main():
    read_date_map()


if __name__ == '__main__':
    main()
