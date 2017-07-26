import ctypes

import numpy

"""
All memory is allocated in python. C++ DO NOT allocate any memory.
"""
from project_helper.config_module import myconfig
from ctypes import *
path = str(myconfig.project_root/'cpp_functions'/'algorithm.dll')
algorithm_dll = ctypes.cdll.LoadLibrary(path)


"""
    Interface of the dll
	DLL_API int handle_doubles(double* vals, int len, double*out, int outlen);
"""

float64_p_t = ctypes.POINTER(ctypes.c_double)
int32_p_t = ctypes.POINTER(ctypes.c_int32)
int64_p_t = ctypes.POINTER(ctypes.c_int64)


def _to_float64(arr:numpy.array):
    assert arr.dtype == numpy.float64
    return arr.ctypes.data_as(float64_p_t)

def _to_int_64(arr:numpy.array):
    assert arr.dtype == numpy.int64
    return arr.ctypes.data_as(int64_p_t)










def test_double_multiply(arr:numpy.array, arr_out):
    assert arr.dtype == numpy.float64

    data = arr.astype(numpy.float64)
    c_float64_p = ctypes.POINTER(ctypes.c_double)
    data_p = data.ctypes.data_as(c_float64_p)

    out_data = numpy.empty_like(data)
    out_data_p = out_data.ctypes.data_as(c_float64_p)

    out_len = c_int64(0)
    out_len_p = pointer(out_len)

    val = algorithm_dll.TestDoubleMultiply(data_p, 2, out_data_p, out_len_p)
    # Another way
    # val = algorithm_dll.TestDoubleMultiply(data_p, 2, out_data_p, ctypes.byref(out_len))
    print(arr)
    print(out_data)
    print('out_len_p:: ',
          out_len_p.contents)

def snippet_function():
    val = c_long(2)
    # print(type(val.value))
    val_p = pointer(val)
    # print(val_p.contents)
