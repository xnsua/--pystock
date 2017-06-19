# from sortedcontainers.sorteddict import SortedDict
#
# from data_manager.stock_day_bar_manager import DayBar
#
# df = DayBar.read_etf_day_data('510900')
#
# import datetime
# ilist = list(df.index)
# olist = list(df.open)
# s_time = datetime.datetime.now()
# for i in range(100):
#     sd = SortedDict(zip(ilist, olist))
# print(datetime.datetime.now() - s_time)
#
# import datetime
#
# s_time = datetime.datetime.now()
# for i in range(100):
#     dd = dict(zip(ilist, olist))
# print(datetime.datetime.now() - s_time)
#
# import datetime
#
# s_time = datetime.datetime.now()
# for i in range(1000000):
#     a = sd['2015-01-05']
# print(datetime.datetime.now() - s_time)
#
# import datetime
#
# s_time = datetime.datetime.now()
# for i in range(1000000):
#     a = dd['2015-01-05']
# print(datetime.datetime.now() - s_time)
#
# print(sd[1])
def test_function_call():
    l = [1] * 10000
    import timeit
    def foo():
        return l[1000]

    val = timeit.timeit('a=1', globals=globals())
    print(val)
    val = timeit.timeit('a=l[1000]', globals=globals())
    print(val)
    val = timeit.timeit('a = foo()', globals=globals())
    print(val)
