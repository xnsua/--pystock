import pathlib
from os.path import expanduser

home = expanduser("~")
_stock_data_root = pathlib.Path(home) / 'StockData'


class DayDataPath:
    def __init__(self, data_root):
        self.root_dir = pathlib.Path(data_root / 'day')

        self.etf = self.root_dir / 'etf'
        self.etf.mkdir(parents=True, exist_ok=True)

        self.index = self.root_dir / 'index'
        self.index.mkdir(parents=True, exist_ok=True)

        self.stock = self.root_dir / 'stock'
        self.stock.mkdir(parents=True, exist_ok=True)


# noinspection PyTypeChecker
day_data_path = DayDataPath(_stock_data_root)


def set_day_data_path(path):
    global day_data_path
    day_data_path = DayDataPath(path)
