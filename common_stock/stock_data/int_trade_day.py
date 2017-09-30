import datetime
import pathlib

import numpy  as np

kintdays = np.load(pathlib.Path(__file__).parent / 'intday.pickle')
kintday_to_index = dict(zip(kintdays, range(len(kintdays))))


def int_day_to_date(intday):
    y, m = divmod(intday, 10000)
    m, d = divmod(m, 100)
    date_ = datetime.date(y, m, d)
    return date_


def nearest_int_day(intday, preday=False):
    if intday in kintday_to_index:
        return intday
    search_day = intday
    date_ = int_day_to_date(intday)

    while search_day not in kintday_to_index:
        if preday:
            date_ = date_ + datetime.timedelta(days=-1)
        else:
            date_ = date_ + datetime.timedelta(days=1)
        search_day = date_.year * 10000 + date_.month * 100 + date_.day
    return search_day

def arr_of_intday_range(start_intday, end_intday):
    start_intday = nearest_int_day(start_intday)
    end_intday = nearest_int_day(end_intday)
    i1 = kintday_to_index[start_intday]
    i2 = kintday_to_index[end_intday]
    return kintdays[i1:i2]

def main():
    val = nearest_int_day(20170930, preday=True)
    print(val)
    val = (arr_of_intday_range(20170825,20171003))
    print(val)



if __name__ == '__main__':
    main()
