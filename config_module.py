from pathlib import Path

class Config:
    project_root = Path(__file__).parent

    stock_data_dir = project_root.parent / 'py_stock_data'

    etf_day_data_dir = stock_data_dir / 'day/etf_data'
    stock_day_data__dir = stock_data_dir / 'day'


myconfig = Config()

if __name__ == '__main__':
    print(myconfig.project_root)
    print(myconfig.stock_data_dir)
    pass
