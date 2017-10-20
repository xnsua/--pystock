import pandas
# noinspection PyUnresolvedReferences
def parse_date():
    import datetime
    import timeit
    val = timeit.timeit('date = datetime.date(*map(int, "2011-01-01".split("-")))',
                        globals=globals())
    print(val)
    val = timeit.timeit("date = datetime.datetime.strptime('2011-01-01', '%Y-%m-%d').date()",
                        globals=globals())
    print(val)


def test_function_call():
    print('test function call:\n')
    l = [1] * 10000
    import timeit

    def foo():
        return l[1000]

    def foo2():
        return 1

    val = timeit.timeit('a=1', globals=locals())
    print(val)
    val = timeit.timeit('a=foo2()', globals=locals())
    print(val)
    val = timeit.timeit('a=l[1000]', globals=locals())
    print(val)
    val = timeit.timeit('a = foo()', globals=locals())
    print(val)


def test_pandas():
    import timeit
    import numpy
    df = pandas.DataFrame(index=['2011-01-01', '2011-01-02'], data=[[1, 2], [3, 4]],
                          columns=['open', 'close'])
    nparr = numpy.array([1, 2, 3, 4])
    open_ = df.open
    open_list = list(df.open)
    open_array = df.open.values
    class Foo:
        pass

    def func():
        pass

    foo = Foo()
    statement_list = [
        'a = 1',
        'a = 1 + 2',
        'foo.a = 1',
        'foo.long_name_hello_word = 1',
        'a = 1*2',
        'a = 1 / 2.0',
        'a = 1 / 2.0',
        'a = 1 / 2.0',
        'a = round(1 / 3, 3)',
        'a = func',
        'a = df.open',
        'a = open_list[1]',
        'a = open_array[1]',
        'a = numpy.array(open_array, copy=False)',
        'a = open_.iat[0]',
        'a = df.iat[0,0]',
        'a = nparr[0]',
    ]

    time_origin = timeit.timeit('a=1', globals=globals(), number=10000)

    for item in statement_list:
        print(item)
        print(timeit.timeit(item, globals=locals(), number=10000) / time_origin)
        print('')


