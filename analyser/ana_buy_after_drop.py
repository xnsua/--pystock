from common_stock.stock_day_bar_manager import DayBar


def analyse_bad(stock_code):
    df = DayBar.read_etf_day_data()
