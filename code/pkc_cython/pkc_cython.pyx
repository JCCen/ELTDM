
import numpy as np
from cython.parallel import prange

DTYPE = np.intc

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
