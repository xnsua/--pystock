from itertools import islice

import numpy
from nose.tools import assert_equal


def calc_rise_percentage(iterable):
    v = numpy.array(iterable)
    result = numpy.empty_like(v)
    result[1:] = v[0:-1]
    vs = result
    vm = v - vs
    vm[0] = 0
    vm = vm[vm > 0]
    vlen = (len(vm))
    return vlen / len(v)


def calc_drop_percentage(iterable):
    v = numpy.array(iterable)
    result = numpy.empty_like(v)
    result[1:] = v[0:-1]
    vs = result
    vm = v - vs
    vm[0] = 0
    vm = vm[vm < 0]
    vlen = (len(vm))
    return vlen / len(v)


def group_consecutive_count(vals, match_val):
    count = [0] * len(vals)
    count[0] = int(vals[0] == match_val)
    for i, val in islice(enumerate(vals), 1, None):
        # print(i,val)
        if val == match_val:
            count[i] = count[i - 1] + 1
        else:
            count[i] = 0
    return count


def test_consective_group_count():
    val = group_consecutive_count([1, 1, 0, 1, 1, 0, 0, 1], 1)
    assert_equal(val, [1, 2, 0, 1, 2, 0, 0, 1])

    val = group_consecutive_count([0, 0, 1, 0, 0, 1, 1, 0], 0)
    assert_equal(val, [1, 2, 0, 1, 2, 0, 0, 1])
