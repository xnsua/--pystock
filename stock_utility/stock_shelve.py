import shelve

from config_module import myconfig


# Easy to use by unittest, buy less locality
class ShelveKey:
    day_bar_history_datetime = 'day_bar_history_datetime'
    initial_account_info = 'initial_account_info'


myshelve = shelve.open(str(myconfig.shelve_path / 'shelve_db'))
