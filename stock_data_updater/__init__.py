import pathlib
from os.path import expanduser

home = expanduser("~")
_stock_data_root = pathlib.Path(home) / 'StockData'
_stock_data_root.mkdir(exist_ok=True, parents=True)


class DayDataPath:
    def __init__(self):
        self.root_dir = _stock_data_root / 'day'

        self.etf = self.root_dir / 'etf'
        self.etf.mkdir(parents=True, exist_ok=True)

        self.index = self.root_dir / 'index'
        self.index.mkdir(parents=True, exist_ok=True)

        self.stock = self.root_dir / 'stock'
        self.stock.mkdir(parents=True, exist_ok=True)


day_data_path = DayDataPath()
