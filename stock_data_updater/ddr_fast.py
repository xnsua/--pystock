import os
import pathlib
import pickle

from common_stock.py_dataframe import DayDataRepr

ddr_fast_dir = os.path.expanduser('~/StockData/ddr_fast/')
pathlib.Path(ddr_fast_dir).mkdir(exist_ok=True)


def write_ddr(code):
    from stock_data_updater.data_provider import ddr_pv
    ddr = ddr_pv.ddr_of(code)
    val = pickle.dumps(ddr)
    path = pathlib.Path(ddr_fast_dir) / code

    path.write_bytes(val)


def _read_ddr_fast(code):
    path = pathlib.Path(ddr_fast_dir) / code

    ddr = pickle.loads(path.read_bytes())
    return ddr


def read_ddr_fast(code)->DayDataRepr:
    try:
        return _read_ddr_fast(code)
    except:
        write_ddr(code)
    return _read_ddr_fast(code)
