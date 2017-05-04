from config_module import myconfig
from data_server import day_data_manager
from stock_basic import stock_helper


def update_etf():
    """ Return updated etf """
    etf_path = myconfig.stock_day_data_etf_path
    rval = {}
    for val in stock_helper.etf_t1:
        val = val[2:]
        rval[val] = day_data_manager.update_k_data(val, etf_path)
    for val in stock_helper.etf_t0:
        val = val[2:]
        rval[val] = day_data_manager.update_k_data(val, etf_path)
    return rval


def main():
    update_etf()


if __name__ == '__main__':
    main()
