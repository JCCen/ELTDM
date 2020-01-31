
import networkx as nx
import numpy as np
from threading import Thread, Lock
import logging


class Counters():

    def __init__(self, G):
        self.deg = dict(G.degree)
        self.visited = 0
        self.lock = Lock()

    def get_degree(self, node):
        with self.lock:
            return self.deg[node]

    def increment_degree(self, node, value):
        with self.lock:
            self.deg[node] += value

    def get_visited(self):
        with self.lock:
            return self.visited

    def increment_visited(self, value):
        with self.lock:
            self.visited += value


def process_node(nodes_ind, G, counters, level):

    # logging.info(f"Thread {thread_id} starting")

    buff = np.zeros_like(nodes_ind)
    start = 0
    end = 0

    nodes_list = list(G.nodes)

    for i in nodes_ind:
        node = nodes_list[i]
        if G.degree[node] == level:
            buff[end] = i
            end += 1

    while start < end:
        v = buff[start]
        start += 1
        for u in G.neighbors(nodes_list[v]):
            if counters.get_degree(u) > level:
                du = counters.get_degree(u) - 1
                if du == level:
                    buff[end] = u
                    end += 1
                if du <= level:
                    counters.increment_degree(u, 1)

    counters.increment_visited(end)



# Toy graph
G = nx.Graph([])
G.add_edges_from([(1,2), (1,8), (1,9), (5,2), (5,3), (5,4), (5,6), (6,7), (6,8),
                  (6,9), (7,8), (7,9), (8,9), (9,10), (10,11), (11,14), (11,15),
                  (11,12), (14,15), (15,12), (12,14)])
n = len(G.nodes)

# Multithreaded PKC
counters = Counters(G)
n_threads = 2
nodes_split = np.array_split(range(n), n_threads)

visited = counters.get_visited()
level = 0
thread_list = []

while visited < n:
    print(visited, flush=True)
    for t in range(n_threads):
        thread = Thread(target=process_node, args=(nodes_split[t], G, counters, level))
        thread_list.append(thread)
        thread_list[t].start()

    for thread in thread_list:
        thread.join()

    thread_list = []

    level += 1
    visited = counters.get_visited()


assert(nx.core_number(G) == counters.deg)
