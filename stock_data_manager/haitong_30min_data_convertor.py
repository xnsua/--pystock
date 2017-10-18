import os

import numpy

from project_config.config_module import HAITONG_30_PATH

haitong_default_data_path = 'C:\\new_haitong\\T0002\\export'


def full_file_name_under_folder(path):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles


def convert_file(ffile_name):
    # if stop and ffile_name.find('600429') == -1:
    #     stop = False
    #     return
    print(ffile_name)
    file = open(ffile_name, 'r', encoding='gbk')
    vals = [item for item in file]
    vals = vals[4:-1]
    if not vals:
        return
    ll = []
    try:
        for val in vals:
            val = (val.split('\t'))[:-1]
            val = [item.strip() for item in val]
            time_ = val[0]
            time_parts = time_.split('-')
            time1 = map(int, time_parts[0].split('/'))
            time2 = map(int, time_parts[1].split(':'))
            y, m, d = time1
            time1 = y * 10000 + m * 100 + d
            h, m = time2
            time2 = h * 100 + m
            time = time1 * 10000 + time2

            price_info = [time, *map(float, val[1:6])]
            ll.append(price_info)
    except:
        return

    ll = list(zip(*ll))
    import pandas
    df = pandas.DataFrame(
        data={'open': ll[1], 'close': ll[4], 'high': ll[2], 'low': ll[3], 'volume': ll[5]},
        index=ll[0])
    df = df[['open', 'close', 'high', 'low', 'volume']]
    # Only use two year data
    df = df[df.index > 201510100000]
    filename = os.path.basename(ffile_name)
    filename = os.path.splitext(filename)[0]
    save_name = os.path.join(HAITONG_30_PATH, filename) + '.csv'

    # Check the data is valid.
    close1 = df[df.index.values % 10000 == 1500].close
    open1 = df[df.index.values % 10000 == 1000].open
    # 涨跌幅限制
    change = ((open1.values - close1.shift(1).values) / close1.shift(1).values)[1:]
    loc1 = numpy.where(change > 0.11)[0]
    loc2 = numpy.where(change < -0.11)[0]
    if loc1.size > 0:
        val = (open1.iloc[loc1[0]: loc1[0] + 2])
        if val.index[1] - val.index[0] > 20000:
            print('delist:')
            print(val)
            return
    if loc2.size > 0:
        val = (open1.iloc[loc1[0]: loc1[0] + 2])
        if val.index[1] - val.index[0] > 20000:
            print('delist:')
            print(val)
            return
    assert numpy.all(change < 0.11)
    assert numpy.all(change > -0.11)

    try:
        mtime1 = os.path.getmtime(ffile_name)
        mtime2 = os.path.getmtime(save_name)
        if mtime1 - mtime2 < 86400:
            return
    except:
        df.to_csv(save_name)


def main():
    for file in full_file_name_under_folder(haitong_default_data_path):
        convert_file(file)


if __name__ == '__main__':
    main()
