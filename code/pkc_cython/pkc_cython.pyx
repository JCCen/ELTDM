
import numpy as np
from cython.parallel import parallel, prange,  threadid
from libc.stdlib cimport abort, malloc, free
cimport cython, openmp

cdef int NUM_THREADS = 5
DTYPE = np.intc


@cython.boundscheck(False)
def pkc(int[:] deg, int[:] deg_init, int[:, :] neighbors):

    # C externals for sync threads + increment/decrement
    cdef extern int __sync_fetch_and_sub (int *deg_node, int decrement) nogil
    cdef extern int __sync_fetch_and_add (int *deg_node, int increment) nogil

    # global variables
    cdef:
        int n = deg.shape[0]
        int visited = 0
        Py_ssize_t n_neighbors
        int max_neighbors = neighbors.shape[1]

    # declare thread local variables pointers
    cdef:
        int *buff
        int *v
        int *n_neighbors_v
        int *deg_u
        int *start
        int *end
        int *level
        Py_ssize_t i, j, u


    # start parallelization over thread with released GIL
    with nogil, parallel():

        # declare thread local variables
        buff = <int *> malloc(sizeof(int) * n / NUM_THREADS) # Local buffer
        v = <int *> malloc(sizeof(int))
        n_neighbors_v = <int *> malloc(sizeof(int))
        deg_u = <int *> malloc(sizeof(int))
        du = <int *> malloc(sizeof(int))
        end = <int *> malloc(sizeof(int))
        end[0] = 0
        start = <int *> malloc(sizeof(int))
        start[0] = 0
        level = <int *> malloc(sizeof(int))
        level[0] = 0

        while visited < n:

            with gil:
                print(visited)
                visited = visited + 1

            for i in prange(n, schedule='static'):
                if deg[i] == level[0]:
                    buff[end[0]] = i
                    end[0] += 1



            while start < end:

                v[0] = buff[start[0]]
                start[0] += 1
                with gil:
                    n_neighbors_v[0] = deg_init[v[0]]

                for u in range(n_neighbors_v[0]):
                    with gil:
                        deg_u[0] = deg[u]
                    if deg_u[0] > level[0]:
                        du[0] = __sync_fetch_and_sub(&deg[u], 1)
                    if du[0] == (level[0] + 1):
                        buff[end[0]] = u
                        end[0] += 1
                    if du[0] <= level[0]:
                        __sync_fetch_and_add(&deg[u], 1)

            __sync_fetch_and_add(&visited, 1)
            with gil:
                visited = visited + 1

            with gil:
                start[0] = 0
                end[0] = 0
                level[0] += 1

        free(buff)

    return np.array(deg)
