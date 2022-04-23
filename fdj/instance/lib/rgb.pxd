cimport numpy as c_np
cdef c_np.ndarray[int, ndim=1] rgb_numpy (int r, c_np.ndarray[int, ndim=2] dots)
cdef c_np.ndarray[int, ndim=1] rgb_memview(int r,  int [:, :] dots)
cdef c_np.ndarray[int, ndim=1] rgb_prange(int r,  c_np.ndarray[int, ndim=2] dots)
