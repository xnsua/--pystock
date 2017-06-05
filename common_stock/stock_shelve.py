import atexit
import pathlib
import shelve


# Easy to use by unittest, but less locality
class ShelveKey:
    day_bar_history_datetime = 'day_bar_history_datetime'


# Do not use config. Config is not share by different project
path = pathlib.Path(__file__).parent / 'data_shelve'
path.mkdir()
stock_shelve = shelve.open(str(path / 'stock_shelve'))

atexit.register(lambda: stock_shelve.close())
