class ObjectWithIndentRepr(object):
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._indent_repr()

    def _indent_repr(self):
        texts = ['    ' + str(key) + ':' + str(value) for key, value in self.__dict__.items()]
        text = '\n'.join(texts)
        return type(self).__name__ + '{\n' + text + '}'


class ObjectWithRepr(object):
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._repr()

    def _repr(self):
        return type(self).__name__ + str(self.__dict__)


def test():
    class Foo(ObjectWithIndentRepr):
        def __init__(self):
            self.a = 1
            self.b = 'hello'

    print(repr(Foo()))


