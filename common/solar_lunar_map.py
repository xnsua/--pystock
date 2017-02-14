from utilities.import_basic import *


class Lunar:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.leap_month = 0


solumap = {}


def load_map():
    # noinspection PyTypeChecker
    fcon = hp.read_string_from_file((pl.Path(config.get_project_root()) / 'data' / 'solar_lunar_map.txt'))
    lines = fcon.split('\n')
    for item in lines:
        if item:
            solu = item.split(' ')
            solar_date = du.parser.parse(solu[0])
            lunar_date = Lunar()
            lunar_date.year, lunar_date.month, lunar_date.day, lunar_date.leap_month = solu[1].split('-')
            solumap[solar_date] = lunar_date
            solumap[lunar_date] = solar_date
    return solumap


def main():
    global solumap
    solumap = load_map()
    # print(solumap)


if __name__ == '__main__':
    main()
