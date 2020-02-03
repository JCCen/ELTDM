
# python3 code/pkc_cython/setup.py build_ext --inplace

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import pkc_cython

DTYPE = np.intc

def plot_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()

G = nx.duplication_divergence_graph(10, 0.5, seed=10)
# plot_graph(G)
true_kcore = nx.core_number(G)

# Extract nodes and lists of neighbors from G as numpy arrays
n = G.number_of_nodes()
nodes = np.arange(n, dtype=DTYPE)

neighbors = [list(G.neighbors(n)) for n in nodes]
deg_init = np.array([len(x) for x in neighbors], dtype=DTYPE)

max_n_neighbors = max(len(x) for x in neighbors)
neighbors = [x + [-1]*(max_n_neighbors - len(x)) for x in neighbors]
neighbors = np.array(neighbors, dtype=DTYPE)

pkc_out = pkc_cython.pkc(deg_init, deg_init, neighbors)
