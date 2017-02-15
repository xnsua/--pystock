import pandas
from    utilities.import_basic import *


class Foo:
    @classmethod
    def test(cls, content):
        return content


def call_after_first(func):
    if call_after_first.first_time:
        call_after_first.first_time = False
        return
    func()


call_after_first.first_time = True


def foo():
    # error : cannot find name
    # print(varhello)
    pass


def foowrapper():
    varhello = 'varhello'
    foo()


import numpy

a = numpy.asarray(['1', '2'])
numpy.savetxt("tpfoo.csv", a, fmt='%s', delimiter=",")


def main():
    df = pandas.DataFrame([1])
    print(df.iloc[0])
    return

if __name__ == '__main__':
    main()
