# from http://fa.bianp.net/blog/2014/plot-memory-usage-as-a-function-of-time/
# run mprof run test1.py
# run mprof plot

import time
import scalable_algo_sequential
import naive_algo
import networkx as nx
import time

@profile
def create_graph(n):
    G = nx.duplication_divergence_graph(n,0.5)
    return G

@profile
def seq_k_core_decompo(g):
    scalable_algo_sequential.seq_k_core_decompo(g)
    return None


@profile
def naive_approach(g):
    naive_algo.naive_approach(g)
    return None

if __name__ == "__main__":
    G = create_graph(15000)
    time.sleep(1)
    seq_k_core_decompo(G)
    time.sleep(1)
    naive_approach(G)