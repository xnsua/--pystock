from pathlib import Path

class MyConfig:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.home
        self.stock_data_path = Path

class ProjectPath:
    def __init__(self):
        import os
        self.project_root = Path(__file__).parent.parent
        self.home = Path(os.path.expanduser('~/'))
        self.stock_data = self.home / 'StockData'

        self.announcement = self.stock_data / 'announcement'

ppath = ProjectPath()


myconfig = MyConfig()

if __name__ == '__main__':
    pass
