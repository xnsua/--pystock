from pathlib import Path


class MyConfig:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent


myconfig = MyConfig()

if __name__ == '__main__':
    pass
