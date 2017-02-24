from time import *

from utilities.import_basic import *


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
    foo()


def sleep1():
    sleep(1)


def sleep2():
    sleep(2)


def sleep3():
    sleep(3)


def sleep4():
    sleep(4)


# noinspection PyShadowingNames
def test():
    a = 1
    b = 2
    huh = locals()
    c = 3
    foo = '{a}'.format(**locals())
    print(foo)


def main():
    lsum = 0
    for i in range(1, 1000 * 1000):
        lsum += i * i
    print(lsum)
    print(dt.date.today().strftime('%Y%m%d'))
    print(dt.datetime.now().strftime('%Y%m%d'))
    print(dt.datetime('2015-2-1h'))
    return


if __name__ == '__main__':
    main()
