class EqualityBase(object):
    def __eq__(self, other) -> bool:
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
