import pandas

from fund_querier.fund_query_manager import fund_querier
from include.fund_info import FundInfo


def read_fund_value(fund_code: str):
    fvpath = fund_querier.get_fund_value_pathname(fund_code)
    df = pandas.read_csv(fvpath, index_col=0)
    print(df)


def read_fund_info(fund_code: str):
    fpn = fund_querier.get_fund_info_pathname(fund_code)
    fi = FundInfo.from_file(fpn)
    print(fi)


def main():
    read_fund_value('000017')
    read_fund_info('000017')


if __name__ == '__main__':
    main()
