class RequireException(Exception):
    pass


def require_msg(msg=''):
    raise RequireException(f'Failed :: {msg}')


def require_true(val, msg=''):
    if not val:
        raise RequireException(f'Failed:: {val} :: {msg}')


def require_false(val, msg=''):
    if val:
        raise RequireException(f'Failed:: Not {val} :: {msg}')


def require_len(val1, len_, msg=''):
    if not len_(val1) == len_:
        raise RequireException(f'Failed:: Length of {val1} == {len} :: {msg}')


def require_eq(val1, val2, msg=''):
    if not val1 == val2:
        raise RequireException(f'Failed:: {val1} == {val2} :: {msg}')


def require_noteq(val1, val2, msg=''):
    if val1 == val2:
        raise RequireException(f'Failed:: {val1} != {val2} :: {msg}')


def require_gt(val1, val2, msg=''):
    if not val1 > val2:
        raise RequireException(f'Failed:: {val1} > {val2} :: {msg}')


def require_lt(val1, val2, msg=''):
    if not val1 < val2:
        raise RequireException(f'Failed:: {val1} < {val2} :: {msg}')


def require_ge(val1, val2, msg=''):
    if not val1 >= val2:
        raise RequireException(f'Failed:: {val1} >= {val2} :: {msg}')


def require_le(val1, val2, msg=''):
    if not val1 <= val2:
        raise RequireException(f'Failed:: {val1} <= {val2} :: {msg}')


def require_contain(collection, subset, msg=''):
    if subset not in collection:
        raise RequireException(
            f'Failed:: {collection} contains {subset} :: {msg}')
