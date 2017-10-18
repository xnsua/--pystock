from stock_data_manager import stock_sector
from stock_data_manager.web_querier import sina_api


def crawl_everything():
    codes = stock_sector.kcs_codes
    sina_api.crawl_margin_info(codes, 20120101)

def main():
    crawl_everything()


if __name__ == '__main__':
    main()

