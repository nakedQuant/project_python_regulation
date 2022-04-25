# cython: language_level=3
cimport numpy as c_np
from .rgb cimport rgb_numpy, rgb_memview, rgb_prange


def rgb_numpy(int r, c_np.ndarray[int, ndim=2] dots):
    return rgb_numpy(r, dots)


def rgb_memview(int r, int [:,:] dots):
    return rgb_memview(r, dots)


def rgb_prange(int r, c_np.ndarray[int, ndim=2] dots):
    return rgb_numpy(r, dots)
