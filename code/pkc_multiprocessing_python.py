
import networkx as nx
import numpy as np
from multiprocessing import Process, Value, Array, cpu_count, Pool, Event
import time

N_PROCESSES = 1


def process_nodes(nodes_ind, G, deg, visited, level):
    """Process a sequence of nodes on a local process."""
    nodes_list = list(G.nodes)
    buff = np.zeros_like(nodes_list).astype(int)
    start = 0
    end = 0

    for i in nodes_ind:
        deg_i = deg[i]
        if deg_i == level:
            buff[end] = i
            end += 1

    while start < end:
        v = buff[start]
        start += 1
        for u in G.neighbors(nodes_list[v]):
            ind_u = nodes_list.index(u)
            if deg[ind_u] > level:
                deg[ind_u] -= 1
                a = deg[ind_u]
                if a == level:
                    buff[end] = ind_u
                    end += 1
                if a < level:
                    a += 1

    visited.value += end


def pkc(G):
    """Perform multiprocessing K-core decomposition."""
    G = G.copy()
    nodes = list(G.nodes)
    n = len(nodes)
    nodes_split = np.array_split(range(n), N_PROCESSES)

    deg = Array('i', list(dict(G.degree).values()))
    visited = Value('i', 0)
    level = 0

    process_list = []

    while visited.value < n:
        for t in range(N_PROCESSES):
            process = Process(target=process_nodes, args=(nodes_split[t], G,
                                                          deg, visited, level))
            process_list.append(process)
        for process in process_list:
            process.start()

        for process in process_list:
            process.join()
        level += 1
        process_list = []

    kcore = {nodes[i]: deg[i] for i in range(n)}

    return kcore


# Test on bigger graph
G_big = nx.duplication_divergence_graph(10000, 0.5)

a = time.time()
kcore_G_big_pkc = pkc(G_big)
b = time.time() - a



# kcore_G_big_true = nx.core_number(G_big)
# assert(kcore_G_big_true == kcore_G_big_pkc)
# kcore_true = np.array(list(kcore_G_big_true.values()))
# kcore_false = np.array(list(kcore_G_big_pkc.values()))
# diff = kcore_true - kcore_false
# print(diff.sum())
# print(diff.max())
# print(diff)