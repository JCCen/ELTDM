
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()

G = nx.duplication_divergence_graph(10, 0.5, seed=10)
# plot_graph(G)
true_kcore = nx.core_number(G)

n = G.number_of_nodes()
nodes = np.arange(n)
neighbors = [list(G.neighbors(n)) for n in nodes]