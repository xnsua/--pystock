import pandas


def f(x):
    return x ** 2


def g(x):
    return x ** 4


def h(x):
    return x ** 8


import timeit

df = pandas.DataFrame(index=['2011-01-01', '2011-01-02'], data=[[1, 2], [3, 4]],
                      columns=['open', 'close'])
open_ = df.open


class Foo:
    pass


foo = Foo()
l = [] * 1000
statement_list = [
    'a = 1',
    'a = 1 + 2',
    'foo.a = 1',
    'foo.long_name_hello_word = 1',
    'a = 1*2',
    'a = 1 / 2.0',
    'a = 1 / 2.0',
    'l.append(1)',
    'l[10] = 5',
    'a = df.open',
    'a = open_.iat[0]',
    'a = open_[0]',
    'a = df.iat[0,0]',
    'a = df.iloc[0,0]',
    'a = df.index.get_loc("2011-01-02")'
]

time_origin = timeit.timeit('a=1', globals=globals(), number=10000)

for item in statement_list:
    print(item)
    print(timeit.timeit(item, globals=globals(), number=10000) / time_origin)
    print('')
