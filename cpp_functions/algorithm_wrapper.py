import ctypes

import numpy

from project_helper.config_module import ppath

"""
All memory is allocated in python. C++ DO NOT allocate any memory.
"""
from ctypes import *
path = str(ppath.project_root/'cpp_functions'/'algorithm.dll')
algorithm_dll = ctypes.cdll.LoadLibrary(path)


"""
    Interface of the dll
	DLL_API int handle_doubles(double* vals, int len, double*out, int outlen);
"""

float64_p_t = ctypes.POINTER(ctypes.c_double)
int32_p_t = ctypes.POINTER(ctypes.c_int32)
int64_p_t = ctypes.POINTER(ctypes.c_int64)



def _to_float64_p(arr:numpy.array):
    assert arr.dtype == numpy.float64
    return arr.ctypes.data_as(float64_p_t)

def _to_int_64_p(arr:numpy.array):
    assert arr.dtype == numpy.int64
    return arr.ctypes.data_as(int64_p_t)

def cEMA(arrin:numpy.array, alpha):
    in_data_p = _to_float64_p(arrin)
    len_in = len(arrin)

    out_data = numpy.empty_like(arrin)
    out_data_p = _to_float64_p(out_data)
    len_out = ctypes.c_int64(len(out_data))
    alpha = ctypes.c_double(alpha)
    algorithm_dll.EMA(in_data_p, len_in, out_data_p, byref(len_out), alpha)

cEMA(numpy.asarray([1.0,2,3,4,5,6]), 0.2)

# def test_double_multiply(arrin:numpy.array, arr_out):
#     assert arrin.dtype == numpy.float64
#
#     data = arrin.astype(numpy.float64)
#     c_float64_p = ctypes.POINTER(ctypes.c_double)
#     data_p = data.ctypes.data_as(c_float64_p)
#
#     out_data = numpy.empty_like(data)
#     out_data_p = out_data.ctypes.data_as(c_float64_p)
#
#     out_len = c_int64(0)
#     out_len_p = pointer(out_len)
#
#     val = algorithm_dll.TestDoubleMultiply(data_p, 2, out_data_p, out_len_p)
#     # Another way
#     # val = algorithm_dll.TestDoubleMultiply(data_p, 2, out_data_p, ctypes.byref(out_len))
#     print(arrin)
#     print(out_data)
#     print('out_len_p:: ',
#           out_len_p.contents)

