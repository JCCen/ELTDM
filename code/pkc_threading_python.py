
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread, Lock
import logging


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

    def increment_visited(self, value):
        with self.lock:
            self.visited += value


def process_node(thread_id, buff, node_ind, G, deg):

    logging.info(f"Thread {thread_id} starting")

    buff = buff.copy()
    level = 0
    start = 0
    end = 0

    node = list(G.nodes)[node_ind]
    if G.degree[node] == level:
        buff[end] = node_ind
        end += 1

    while start < end:
        v = buff[start]
        start += 1
        for u in G.neighbors(v):
            if deg.get_degree(u) > level:
                du = deg.get_degree(u) - 1
                if du == level:
                    buff[end] = u
                    end += 1
                if du <= level:
                    deg.increment_degree(u, 1)
        deg.increment_visited(end)

    logging.info(f"Thread {thread_id} finishing")


counters = Counters(G)


def python_threading_pkc(G, n_threads):

    G = G.copy()
    n = len(G.nodes)

    visited = 0
    buff = np.empty(n // n_threads).astype(int)

    while visited < n:
        thread = ThreadPKC(buff)
        thread.start()


    return deg


# class ThreadPKC(Thread):
#
#     def __init__(self, id, buff):
#         Thread.__init__(self)
#         self.id = id
#         self.buff = buff.copy()
#         self.level = 0
#         self.start = 0
#         self.end = 0
#
#     def run(self, node_ind, G, deg, visited):
#         global _lock
#         logging.info(f"Thread {self.id} starting")
#
#         node = list(G.nodes)[node_ind]
#         if G.degree[node] == self.level:
#             self.buff[self.end] = node_ind
#             self.end += 1
#
#         while self.start < self.end:
#             v = self.buff[self.start]
#             self.start += 1
#
#             for u in G.neighbors(v):
#                 if deg[u] > self.level:
#                     with _lock:
#                         du = deg[u] - 1
#
#                     if du == self.level:
#                         self.buff[self.end] = u
#                         self.end += 1
#
#                     if du <= self.level:
#                         with _lock:
#                             deg[u] += 1
#
#         with _lock:
#             visited += self.end
#
#         logging.info(f"Thread {self.id} finishing")