import pandas


def test_function_call():
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
    df = pandas.DataFrame(index=['2011-01-01', '2011-01-02'], data=[[1, 2], [3, 4]],
                          columns=['open', 'close'])
    open_ = df.open
    open_list = list(df.open)

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
        'a = open_.iat[0]',
        'a = df.iat[0,0]',
    ]

    time_origin = timeit.timeit('a=1', globals=globals(), number=10000)

    for item in statement_list:
        print(item)
        print(timeit.timeit(item, globals=locals(), number=10000) / time_origin)
        print('')


def test_pandas_test_iterator():
    pass
    # df = DayBar.read_etf_day_data('510900')
    # index = df.index
    # dl = list(index)
    # import datetime
    # s_time = datetime.datetime.now()
    # About two times slow
    # for j in range(1000):
    #     for _ in index:
    #         pass
    # print(datetime.datetime.now() - s_time)
    #
    # s_time = datetime.datetime.now()
    # for j in range(1000):
    #     for _ in dl:
    #         pass
    # print(datetime.datetime.now() - s_time)
