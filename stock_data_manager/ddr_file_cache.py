import os
import pathlib
import pickle

from common.scipy_helper import pdDF
from common_stock.day_data_representation import DayDataRepr
from common_stock.stock_helper import CodeTools
from project_config.config_module import HAITONG_30_PATH, STOCK_MARGIN_MARGIN_TRADING_PATH

ddr_fast_dir = os.path.expanduser('~/StockData/ddr_file_cache/')
pathlib.Path(ddr_fast_dir).mkdir(exist_ok=True)


def write_ddr(code):
    from stock_data_manager.data_provider import ddr_pv
    ddr = ddr_pv.ddr_of(code)
    val = pickle.dumps(ddr)
    path = pathlib.Path(ddr_fast_dir) / code

    path.write_bytes(val)


def _read_ddr_fast(code):
    path = pathlib.Path(ddr_fast_dir) / code

    ddr = pickle.loads(path.read_bytes())
    return ddr


def read_ddr_fast(code) -> DayDataRepr:
    try:
        return _read_ddr_fast(code)
    except:
        write_ddr(code)
    return _read_ddr_fast(code)


def read_30min_df(code) -> pdDF:
    code = CodeTools.to_pcode(code)
    filename = HAITONG_30_PATH / (code + '.csv')
    import pandas
    df = pandas.read_csv(filename, index_col=0)
    return df


def read_margin_info(code) -> pdDF:
    code = CodeTools.to_pcode(code)
    filename = STOCK_MARGIN_MARGIN_TRADING_PATH / (code + '.csv')
    import pandas
    df = pandas.read_csv(filename)
    return df
