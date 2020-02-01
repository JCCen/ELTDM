
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G):
    nx.draw(G, with_labels=True)
    plt.show()

## Toy graph
#G = nx.Graph([])
#G.add_edges_from([(1,2),(1,8),(1,9),
#                  (5,2),
#                  (5,3),
#                  (5,4),
#                  (5,6),
#                  (6,7),
#                  (6,8),
#                  (6,9),
#                  (7,8),
#                  (7,9),
#                  (8,9),
#                  (9,10),
#                  (10,11),
#                  (11,14),
#                  (11,15),
#                  (11,12),
#                  (14,15),
#                  (15,12),
#                  (12,14)
#                 ])
## plot_graph(G)
#print(nx.core_number(G))
#
# Sequential algorithm

def seq_max_k_core(G):

    peel = 1
    Q = []
    num_active = G.number_of_nodes()
    G_nodes = tuple(G.nodes)
    flag = {v: 0 for v in G_nodes}
    deg = dict(G.degree())

    while num_active > 0:
        Vb = []
        not_flagged = {n for n in G_nodes if flag[n] == 0}

        # This loop can be parallelized
        for n in not_flagged:
            if deg[n] <= peel:
                flag[n] = 1
                Vb.append(n)
        Q = set(Q) | set(Vb)
        num_active -= len(Vb)

        if Vb:
            # This loop can be parallelized
            for u in Vb:
                for v in G.neighbors(u):
                    deg[u] -= 1
                    deg[v] -= 1
        else:
            peel += 1
            Q = []

    return G.subgraph(Q), peel

def seq_k_core_decompo(G):

    G = G.copy()
    peels = {}

    while list(G.nodes):
        K, k_num = seq_max_k_core(G)
        # plot_graph(K)
        # This loop can be parallelized
        for e in K.edges:
            peels[e] = k_num

        G.remove_edges_from(list(K.edges))
        G.remove_nodes_from(list(K.nodes))
        # plot_graph(G)

    return peels
#
#plot_graph(G)