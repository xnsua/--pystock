from pathlib import Path
class Config:
    def __init__(self):
        self.project_root = Path(__file__).parent

        self.stock_data_dir = self.project_root.parent / 'py_stock_data'

        self.etf_day_data_dir = self.stock_data_dir / 'day/etf_data'
        self.stock_day_data__dir = self.stock_data_dir / 'day'

        self.shelve_path = self.project_root / 'shelve'  # type: Path
        self.shelve_path.mkdir(parents=True, exist_ok=True)


myconfig = Config()

if __name__ == '__main__':
    pass
