class ClaimException(Exception):
    pass


def claim_msg(msg=''):
    raise ClaimException(f'Failed :: {msg}')


def claim_true(val, msg=''):
    if not val:
        raise ClaimException(f'Failed:: {val} :: {msg}')


def claim_false(val, msg=''):
    if val:
        raise ClaimException(f'Failed:: Not {val} :: {msg}')


def claim_len(val1, val2, msg=''):
    if not len(val1) == val2:
        raise ClaimException(f'Failed:: Length of {val1} == {val2} :: {msg}')


def claim_eq(val1, val2, msg=''):
    if not val1 == val2:
        raise ClaimException(f'Failed:: {val1} == {val2} :: {msg}')


def claim_noteq(val1, val2, msg=''):
    if val1 == val2:
        raise ClaimException(f'Failed:: {val1} != {val2} :: {msg}')


def claim_gt(val1, val2, msg=''):
    if not val1 > val2:
        raise ClaimException(f'Failed:: {val1} > {val2} :: {msg}')


def claim_lt(val1, val2, msg=''):
    if not val1 < val2:
        raise ClaimException(f'Failed:: {val1} < {val2} :: {msg}')


def claim_ge(val1, val2, msg=''):
    if not val1 >= val2:
        raise ClaimException(f'Failed:: {val1} >= {val2} :: {msg}')


def claim_le(val1, val2, msg=''):
    if not val1 <= val2:
        raise ClaimException(f'Failed:: {val1} <= {val2} :: {msg}')


def claim_contain(collection, val, msg=''):
    if val not in collection:
        raise ClaimException(
            f'Failed:: {collection} contains {val} :: {msg}')
