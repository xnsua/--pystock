import datetime as dt

from common import plPath


class Lunar:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.leap_month = 0


solar_lunar_map = {}


# noinspection SpellCheckingInspection
def load_map():
    # noinspection PyTypeChecker
    fcon = (plPath(__file__).parent / 'solar_lunar_map.txt').read_text()
    lines = fcon.split('\n')
    for item in lines:
        if item:
            solu = item.split(' ')
            syear, smonth, sday = solu[0].split('-')
            solar_date = dt.datetime(int(syear), int(smonth), int(sday))
            lunar_date = Lunar()
            lunar_date.year, lunar_date.month, lunar_date.day, lunar_date.leap_month = \
                [int(i) for i in solu[1].split('-')]
            solar_lunar_map[solar_date] = lunar_date
            solar_lunar_map[lunar_date] = solar_date
    return solar_lunar_map


def main():
    global solar_lunar_map
    solar_lunar_map = load_map()
    print(solar_lunar_map)


if __name__ == '__main__':
    main()
