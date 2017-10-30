from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

from os.path import expanduser

home = expanduser("~")

STOCK_DATA_PATH = Path(home) / 'StockData'
HAITONG_30_PATH = STOCK_DATA_PATH / 'haitong30'
STOCK_MARGIN_MARGIN_TRADING_PATH = STOCK_DATA_PATH / 'margin_trading'
STOCK_ANALYSE_RESULT = STOCK_DATA_PATH / 'analyse_result'

STOCK_DATA_PATH.mkdir(exist_ok=True)
HAITONG_30_PATH.mkdir(exist_ok=True)
STOCK_MARGIN_MARGIN_TRADING_PATH.mkdir(exist_ok=True)
STOCK_ANALYSE_RESULT.mkdir(exist_ok=True)
