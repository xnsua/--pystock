from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

from os.path import expanduser
home = expanduser("~")
STOCK_DATA_PATH = Path(home) / 'StockData'
