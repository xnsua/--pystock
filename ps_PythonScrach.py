from time import sleep


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


def sleep1():
    sleep(1)


def sleep2():
    sleep(2)


def sleep3():
    sleep(3)


def sleep4():
    sleep(4)


def test():
    a = 1
    b = 2
    huh = locals()
    c = 3
    foo = '{a}'.format(**locals())
    print(foo)


def main():
    test()
    sleep(2)
    sum = 0
    for i in range(1, 1000 * 1000):
        sum += i * i
    print(sum)
    return


if __name__ == '__main__':
    main()
