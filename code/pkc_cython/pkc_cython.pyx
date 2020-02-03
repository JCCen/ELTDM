
import numpy as np
from cython.parallel import parallel, prange,  threadid
from libc.stdlib cimport abort, malloc, free
cimport cython, openmp

cdef int NUM_THREADS = 5
DTYPE = np.intc

def pkc(int[:] deg, int[:, :] neighbors):

    # global variables
    cdef:
        long n = deg.shape[0]
        long visited = 0

    # thread local variables
    cdef:
        int *buff
        int *start
        int *end
        int *level
        Py_ssize_t i, j, u, v

    # start parallelization over thread with released GIL
    with nogil, parallel():

        # declare thread local variables
        buff = <int *> malloc(sizeof(int) * n / NUM_THREADS)
        if buff is NULL:
            abort()
        end = <int *> malloc(sizeof(int))
        end[0] = 0
        start = <int *> malloc(sizeof(int))
        start[0] = 0
        level = <int *> malloc(sizeof(int))
        level[0] = 0

        while visited < n:

            for i in prange(n, schedule='static'):
                if deg[i] == level[0]:
                    buff[end[0]] = i
                    end[0] += 1

            while start < end:

                buff[start[0]]
                start[0] += 1











        free(buff)

    return np.array(deg)
















#def process_nodes(nodes_ind, G, counters, level):
#    """Process a sequence of nodes on a local thread."""
#    nodes_list = list(G.nodes)
#    buff = np.zeros_like(nodes_list).astype(int)
#    start = 0
#    end = 0
#
#    for i in nodes_ind:
#        deg_i = counters.get_degree(nodes_list[i])
#        if deg_i == level:
#            buff[end] = i
#            end += 1
#
#    while start < end:
#        v = buff[start]
#        start += 1
#        for u in G.neighbors(nodes_list[v]):
#            if counters.get_degree(u) > level:
#                a = counters.increment_degree(u, -1)
#                if a == level:
#                    buff[end] = nodes_list.index(u)
#                    end += 1
#                if a < level:
#                    counters.increment_degree(u, 1)
#
#    counters.increment_visited(end)
#
#
#def pkc(G, n_threads):
#    """Perform multi-threaded K-core decomposition."""
#    G = G.copy()
#    n = len(G.nodes)
#    assert(n_threads < n)
#    counters = Counters(G)
#
#    nodes_split = np.array_split(range(n), n_threads)
#    level = 0
#    visited = 0
#    thread_list = []
#
#    while visited < n:
#        for t in range(n_threads):
#            thread = Thread(target=process_nodes, args=(nodes_split[t],
#                                                       G, counters, level))
#            thread_list.append(thread)
#            thread_list[t].start()
#        for thread in thread_list:
#            thread.join()
#        thread_list = []
#
#        level += 1
#        visited = counters.get_visited()
#
#    deg = counters.deg.copy()
#
#    return deg
