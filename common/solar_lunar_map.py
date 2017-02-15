import pathlib as pl
import datetime as dt
from utilities.config import config
from common.helper import read_string_from_file
class Lunar:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.leap_month = 0


solumap = {}


def load_map():
    # noinspection PyTypeChecker
    fcon = read_string_from_file((pl.Path(config.get_project_root()) / 'data' / 'solar_lunar_map.txt'))
    lines = fcon.split('\n')
    for item in lines:
        if item:
            solu = item.split(' ')
            syear, smonth, sday = solu[0].split('-')
            solar_date = dt.datetime(int(syear), int(smonth), int(sday))
            lunar_date = Lunar()
            lunar_date.year, lunar_date.month, lunar_date.day, lunar_date.leap_month = \
                [int(i) for i in solu[1].split('-')]
            solumap[solar_date] = lunar_date
            solumap[lunar_date] = solar_date
    return solumap


def main():
    global solumap
    solumap = load_map()
    # print(solumap)


if __name__ == '__main__':
    main()
