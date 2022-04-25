# cython: language_level=3
import cython
from libc.math cimport pow
from libc.stdio cimport printf
cimport numpy as c_np
import numpy as np
from cython.parallel cimport prange


# cython: boundscheck=False
cdef c_np.ndarray[int, ndim = 1] rgb_numpy (int r, c_np.ndarray[int, ndim = 2] dots):
    cdef int i, j, distance
    cdef c_np.ndarray[int, ndim = 1] out
    size = len(dots)
    out = np.empty(size, dtype=np.int32)
    for i in range(size):
        out[i] = -1
        z = dots[i] - dots
        z= z ** 2
        for j in range(size):
            distance = sum(z[j])
            if distance <= r:
                out[i] += 1
    return out


cdef c_np.ndarray[int, ndim = 1] rgb_memview (int r, int [:,:] dots):
    cdef int i, j, distance=0
    cdef int[:] out
    out = np.empty(len(dots), dtype=np.int32)
    size = len(dots)
    for i in range(size):
        out[i] = -1
        for j in range(size):
            distance = (dots[i][0] - dots[j][0]) **2 +  (dots[i][1] - dots[j][1]) **2
            if distance <= r:
                out[i] += 1
    return out


cdef c_np.ndarray[int, ndim = 1] rgb_prange (int r, c_np.ndarray[int, ndim = 2] dots):
    cdef int i, j, distance=0
    cdef int[:] out
    out = np.empty(len(dots), dtype=np.int32)
    size = len(dots)
    with nogil:
        for i in prange(size):
            out[i] = -1
            for j in range(size):
                distance = (dots[i, 0] - dots[j, 0]) **2 +  (dots[i, 1] - dots[j, 1]) **2
                if distance <= r:
                    out[i] += 1
    return out
