# inspire de https://codereview.stackexchange.com/questions/165245/plot-timings-for-a-range-of-inputs
import pandas as pd
from functools import partial
import timeit
import numpy as np
import matplotlib.pyplot as plt
import naive_algo
import scalable_algo_sequential
import networkx as nx
import psutil
import os

def plot_times(functions, inputs, repeats=3, n_tests=1, file_name=""):
    timings = get_timings(functions, inputs, repeats=3, n_tests=1)
    results = aggregate_results(timings)
    fig, ax = plot_results(results)

    return fig, ax, results

def get_timings(functions, inputs, repeats, n_tests):
    for func in functions:
        result = pd.DataFrame(index = inputs, columns = range(repeats), 
            data=(timeit.Timer(partial(func, i)).repeat(repeat=repeats, number=n_tests) for i in inputs))
        yield func, result

def aggregate_results(timings):
    empty_multiindex = pd.MultiIndex(levels=[[],[]], labels=[[],[]], names=['func', 'result'])
    aggregated_results = pd.DataFrame(columns=empty_multiindex)

    for func, timing in timings:
        for measurement in timing:
            aggregated_results[func.__name__, measurement] = timing[measurement]
        aggregated_results[func.__name__, 'avg'] = timing.mean(axis=1)
        aggregated_results[func.__name__, 'yerr'] = timing.std(axis=1)

    return aggregated_results

def plot_results(results):
    fig, ax = plt.subplots()
    x = [len(i) for i in results.index]
    
    for func in results.columns.levels[0]:
        y = results[func, 'avg']
        yerr = results[func, 'yerr']        
        ax.errorbar(x, y, yerr=yerr, fmt='-o', label=func)

    ax.set_xlabel('number of nodes (nx.duplication_divergence_graph(n,0.5))')
    ax.set_ylabel('Time [s]')
    ax.set_yscale('log')
    ax.legend()    
    return fig, ax

G_5 = nx.duplication_divergence_graph(5,0.5)
G_50 = nx.duplication_divergence_graph(50,0.5)
G_100 = nx.duplication_divergence_graph(100,0.5)
G_500 = nx.duplication_divergence_graph(500,0.5)
G_1000 = nx.duplication_divergence_graph(1000,0.5)
G_2500 = nx.duplication_divergence_graph(4000,0.5)
#
plot_times([scalable_algo_sequential.seq_k_core_decompo,naive_algo.naive_approach],[G_5,G_50,G_100,G_500,G_1000,G_2500])