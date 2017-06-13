from numba import jit, int64
from numpy import arange


# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
# noinspection PyPep8Naming,PyShadowingNames
def sum2d2(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i, j]
    return result


@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i, j]
    return result


# @jit(float64(float64, float64))
@jit(nopython=True)
def j_cal(m, p):
    return m / (p - 1.005)


def cal(m, p):
    return m / (p - 1.005)


@jit(int64(int64, int64))
def f(x, y):
    # A somewhat trivial example
    return x + y


def f2(x, y):
    # A somewhat trivial example
    return x + y


import datetime

a = arange(9000000).reshape(30000, 300)
s_time = datetime.datetime.now()
for i in range(1000000):
    j_cal(1, 3)
print(datetime.datetime.now() - s_time)
print(f(1, 2223333333))

s_time = datetime.datetime.now()
for i in range(1000000):
    cal(1, 3)
print(datetime.datetime.now() - s_time)
print(f2(1, 2223333333))
