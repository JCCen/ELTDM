
import networkx as nx
import numpy as np
from threading import Thread, Lock


class Counters():
    """Encapsulate counters in a class with threadlocks to avoid race conditions."""

    def __init__(self, G):
        G = G.copy()
        self.deg = dict(G.degree)
        self.visited = 0
        self.lock = Lock()

    def get_degree(self, node):
        # with self.lock:
            return self.deg[node]

    def increment_degree(self, node, value):
        # with self.lock:
            self.deg[node] += value
            return self.deg[node]

    def get_visited(self):
        # with self.lock:
            return self.visited

    def increment_visited(self, value):
        # with self.lock:
            self.visited += value

    def reinitialize(self, G):
        self.visited = 0
        self.deg = dict(G.degree)


def process_nodes(nodes_ind, G, counters, level):
    """Process a sequence of nodes on a local thread."""
    nodes_list = list(G.nodes)
    buff = np.zeros_like(nodes_list).astype(int)
    start = 0
    end = 0

    for i in nodes_ind:
        deg_i = counters.get_degree(nodes_list[i])
        if deg_i == level:
            buff[end] = i
            end += 1

    while start < end:
        v = buff[start]
        start += 1
        for u in G.neighbors(nodes_list[v]):
            if counters.get_degree(u) > level:
                a = counters.increment_degree(u, -1)
                if a == level:
                    buff[end] = nodes_list.index(u)
                    end += 1
                if a < level:
                    counters.increment_degree(u, 1)

    counters.increment_visited(end)


def pkc(G, n_threads):
    """Perform multi-threaded K-core decomposition."""
    G = G.copy()
    n = len(G.nodes)
    assert(n_threads < n)
    counters = Counters(G)

    nodes_split = np.array_split(range(n), n_threads)
    level = 0
    visited = 0
    thread_list = []

    while visited < n:
        for t in range(n_threads):
            thread = Thread(target=process_nodes, args=(nodes_split[t],
                                                       G, counters, level))
            thread_list.append(thread)
            thread_list[t].start()
        for thread in thread_list:
            thread.join()
        thread_list = []

        level += 1
        visited = counters.get_visited()

    deg = counters.deg.copy()

    return deg



# Test on toy graph
# G_toy = nx.Graph([])
# G_toy.add_edges_from([(1,2), (1,8), (1,9), (5,2), (5,3), (5,4), (5,6), (6,7), (6,8),
#                   (6,9), (7,8), (7,9), (8,9), (9,10), (10,11), (11,14), (11,15),
#                   (11,12), (14,15), (15,12), (12,14)])
#
# kcore_G_toy = pkc(G_toy, 7)
# assert(nx.core_number(G_toy) == kcore_G_toy)
# print(kcore_G_toy)

# Test on bigger graph
G_big = nx.duplication_divergence_graph(100, 0.5)
kcore_G_big_true = nx.core_number(G_big)
kcore_G_big_pkc = pkc(G_big, 2)

kcore_true = np.array(list(kcore_G_big_true.values()))
kcore_false = np.array(list(kcore_G_big_pkc.values()))
diff = kcore_true - kcore_false
print(diff.sum())
print(diff.max())
print(diff)
print(kcore_true[diff != 0])
print(kcore_false[diff != 0])