cython数组 --- cdef double arr[10] 指定空间;
numpy数组 --- cython 也存在一个numpy不同以常规方式访问numpy解释器层面执行的操作极大的开销; 采用的buffer syntax , c_np.ndarray[double, ndim=1](数据类型)
类型化内存视图 --- 实现了采用通用接口简化了数据类型的访问(C数组,numpy数组,bytes,bytearray,array.array), cdef int[:] a
维护一个特定内存区域的引用，但是可以读取改变与修改内容inplace ,底层数据视图,可以绑定与复制

cython -a *.pyx --- profile cython --- html文件

@cython.boundscheck(False)
with cython.boundscheck(False):
# cython: boundscheck = False
@cython.cdivision(True)
cython: profile=True
jupter %load_ext cython
%% cython
line_profiler cython: linetrace=True ; cython: binding=True
共享声明 公共接口 --- from * cimport *
# numpy.get_include()
# nogil 里面循环必须确保不实用解释器 --- 无法调用python代码
