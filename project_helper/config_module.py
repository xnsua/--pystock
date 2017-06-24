from pathlib import Path


class MyConfig:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent

        self.stock_data_dir = self.project_root.parent / 'py_stock_data'

        self.etf_day_data_dir = self.stock_data_dir / 'day/etf_data'
        self.etf_day_data_dir.mkdir(parents=True, exist_ok=True)

        self.index_day_data_dir = self.stock_data_dir / 'day/index_data'
        self.index_day_data_dir.mkdir(parents=True, exist_ok=True)

        self.stock_day_data__dir = self.stock_data_dir / 'day/stock_data'
        self.stock_day_data__dir.mkdir(parents=True, exist_ok=True)


myconfig = MyConfig()

if __name__ == '__main__':
    pass
