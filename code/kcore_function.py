import re 
import itertools
import operator
import copy
import igraph
from library import clean_text_simple, terms_to_graph
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import heapq
import nltk
import cairocffi
import string
from nltk.corpus import stopwords


def core_dec(g,weighted):
    '''(un)weighted k-core decomposition'''
    # work on clone of g to preserve g 
    gg = copy.deepcopy(g)
    if not weighted:
        gg.vs['weight'] = gg.strength() # overwrite the 'weight' vertex attribute with the unweighted degrees
    # initialize dictionary that will contain the core numbers
    cores_g = dict(zip(gg.vs['name'],[0]*len(gg.vs)))
    layout = g.layout("kk")
    igraph.plot(gg, layout = layout)
#    testplot(gg,"initial")
    
    while len(gg.vs) > 0:
        # find index of lowest degree vertex
        min_degree = min(gg.vs['weight'])
        index_top = gg.vs['weight'].index(min_degree)
        name_top = gg.vs[index_top]['name']
        ##print("a9")
        # get names of its neighbors
        neighbors = gg.vs[gg.neighbors(index_top)]['name']
        # exclude self-edges
        neighbors = [elt for elt in neighbors if elt!=name_top]
        # set core number of lowest degree vertex as its degree
        cores_g[name_top] = min_degree
        ### fill the gap (delete top vertex and its incident edges) ###
        gg.delete_vertices(name_top)
#        testplot(gg,"step_"+str(len(gg.vs)))
        if neighbors:
            if weighted: 
                ### fill the gap (compute the new weighted degrees, save results as 'new_degrees')
                new_degrees=gg.strength(weights=gg.es["weight"])
            else:                            
                ### fill the gap (same as above but for the basic degree) ###
                new_degrees=gg.strength()
                
            # iterate over neighbors of top element
            for neigh in neighbors:
                index_n = gg.vs['name'].index(neigh)
                gg.vs[index_n]['weight'] = max(min_degree,new_degrees[index_n])  
        
    return(cores_g)

# =============================================================================
# TO TEST
# =============================================================================

stpwds = stopwords.words('english')
punct = string.punctuation.replace('-', '')

my_doc = 'A method for solution of systems of linear algebraic equations \
with m-dimensional lambda matrices. A system of linear algebraic \
equations with m-dimensional lambda matrices is considered. \
The proposed method of searching for the solution of this system \
lies in reducing it to a numerical system of a special kind.'

my_doc = my_doc.replace('\n', '')

# pre-process document
my_tokens = clean_text_simple(my_doc,my_stopwords=stpwds,punct=punct)

g = terms_to_graph(my_tokens, 4)

# number of edges
print(len(g.es))

# the number of nodes should be equal to the number of unique terms
len(g.vs) == len(set(my_tokens))

edge_weights = []
for edge in g.es:
    source = g.vs[edge.source]['name']
    target = g.vs[edge.target]['name']
    weight = edge['weight']
    edge_weights.append([source, target, weight])


g = terms_to_graph(my_tokens,5)
core_numbers = core_dec(g,False)
#print(core_numbers)
print(core_numbers == {'algebra': 8.0, 'equat': 8.0, 'kind': 3.0, 'lambda': 8.0, 'linear': 8.0, 'm-dimension': 8.0, 'matric': 7.0, 'method': 7.0, 'numer': 5.0, 'solut': 7.0, 'special': 3.0, 'system': 8.0})