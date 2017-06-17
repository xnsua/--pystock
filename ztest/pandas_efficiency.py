import pandas

from data_manager.stock_day_bar_manager import DayBar

df = DayBar.read_etf_day_data('510900')
open_ = df.open


class value:
    def __init__(self):
        self.a = {'dict': 1}


df = pandas.DataFrame(index=['2011-01-01', '2011-01-02'], data=[[1, 2], [3, 4]],
                      columns=['open', 'close'])

val = dict(zip(df.index, zip(df.open, df.close)))
print(val)

# val = df.columns
# print(val)
# print(val.get_loc('open'))
# open_ = df.open
# val = value()
# s_time = datetime.datetime.now()
# for i in range(1000):
#     v = open_.iat[1]
# print(datetime.datetime.now() - s_time)
#
# val = value()
# s_time = datetime.datetime.now()
# for i in range(1000):
#     v = df.iat[1, 1]
# print(datetime.datetime.now() - s_time)
#
# val = value()
# s_time = datetime.datetime.now()
# for i in range(1000):
#     v = df.iat[1, 1]
# print(datetime.datetime.now() - s_time)
#
# print(len(df.open))
# s_time = datetime.datetime.now()
# for i in range(1000):
#     for i in df.open:
#         v = i
# print(datetime.datetime.now() - s_time)
#
# l = [i for i in range(len(df.open))]
# s_time = datetime.datetime.now()
# for i in range(1000):
#     for i in l:
#         v = i
# print(datetime.datetime.now() - s_time)
