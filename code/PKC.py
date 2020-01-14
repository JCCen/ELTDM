

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
# plot_graph(G)
print(nx.core_number(G))


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

        while (start < end):
            v = buff[start]
            start += 1
            for u in G.neighbors(nodes_list[v]):
                if deg[nodes_list[u]] > level:
                    a = deg[nodes_list[u]] - 1
                    if a == (level+1):
                        buff[end] <- u
                        end += 1
                    elif a <= level:
                        deg[nodes_list[u]] += 1

        visited += end
        start = end = 0
        level += 1

    return deg

