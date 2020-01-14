

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

def plot_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()

# Toy graph
G = nx.Graph([])
G.add_edges_from([(1,2),(1,8),(1,9),
                  (5,2),
                  (5,3),
                  (5,4),
                  (5,6),
                  (6,7),
                  (6,8),
                  (6,9),
                  (7,8),
                  (7,9),
                  (8,9),
                  (9,10),
                  (10,11),
                  (11,14),
                  (11,15),
                  (11,12),
                  (14,15),
                  (15,12),
                  (12,14)
                 ])


# Sequential PKC
def seq_pkc(G):

    nodes_list = list(G.nodes)
    n = len(nodes_list)
    visited = level = start = end = 0
    buff = np.empty(n).astype(int)
    deg = dict(G.degree)

    while (visited < n):

        for i in range(n):
            if deg[nodes_list[i]] == level:
                buff[end] = i
                end += 1

        while start < end:
            v = buff[start]
            start += 1
            for u in G.neighbors(nodes_list[v]):
                if deg[u] > level:
                    deg[u] -= 1
                    if deg[u] == level:
                        buff[end] = u
                        end += 1

        visited += end
        start = end = 0
        level += 1

    return deg

plot_graph(G)
seq_pkc_kcore = seq_pkc(G)
assert(nx.core_number(G) == seq_pkc_kcore)


# Parallel PKC
def parallel_pkc(G):

    nodes_array = np.array(G.nodes)
    deg_array = np.array(list(dict(G.degree).values()))
    # For each node, create neighbours array
    # To make a ndarray, we need lists of same size => padding with -1
    neighbors = [list(G.neighbors(n)) for n in nodes_array]
    max_n_neighbors = max(len(x) for x in neighbors)
    neighbors = [x + [-1]*(max_n_neighbors - len(x)) for x in neighbors]
    neighbors_array = np.array(neighbors)
    assert(nodes_array.shape[0] == deg_array.shape[0])
    assert (nodes_array.shape[0] == neighbors_array.shape[0])





