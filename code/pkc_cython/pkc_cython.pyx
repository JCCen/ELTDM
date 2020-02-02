
import numpy as np
from cython.parallel import parallel, prange,  threadid
from libc.stdlib cimport abort, malloc, free
cimport cython, openmp

cdef int NUM_THREADS = 5
DTYPE = np.intc

def pkc(int[:, :] nodes, int[:, :] neighbors):

    # global variables
    cdef:
        long n = nodes.shape[0]
        long visited = 0
        int * core = <int *> malloc(sizeof(int) * n)
        int i

    # thread local variables
        int * buf
        int level = 0
        long start = 0
        long end = 0

    assert core != NULL

    # start parallelization over thread with released GIL
    with nogil, parallel():

        # define thread local buffer
        buf = <int *> malloc(sizeof(int) * n / NUM_THREADS)
        if buf is NULL:
            abort()

        while visited < n:

            for i in prange(n, schedule='static'):
                visited += 1

        free(buf)

    return True
















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
