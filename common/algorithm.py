import numpy


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


