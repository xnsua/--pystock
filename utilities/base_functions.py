class UtilObjectBase(object):
    def __eq__(self, other) -> bool:
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.__dict__.__str__()

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))
