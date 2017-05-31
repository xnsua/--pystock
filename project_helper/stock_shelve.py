import atexit
import shelve

from project_helper.config_module import myconfig


# Easy to use by unittest, but less locality
class ShelveKey:
    day_bar_history_datetime = 'day_bar_history_datetime'
    initial_account_info = 'initial_account_info'


myshelve = shelve.open(str(myconfig.shelve_path / 'shelve_db'))

atexit.register(lambda: myshelve.close())
