class ObjectWithRepr(object):
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._indent_repr()

    def _indent_repr(self):
        strs = [str(key) + ':' + str(value) for key, value in self.__dict__.items()]
        text = '\n'.join(strs)
        return type(self).__name__ + '{\n' + text + '}'

    def _repr(self):
        return type(self).__name__ + str(self.__dict__)

    def _str(self):
        return str(self.__dict__)
