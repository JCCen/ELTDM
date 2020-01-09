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
import timeit

def naive_core_dec(g,weighted):
    '''(un)weighted k-core decomposition'''
    # work on clone of g to preserve g 
    gg = copy.deepcopy(g)
    if not weighted:
        gg.vs['weight'] = gg.strength() # overwrite the 'weight' vertex attribute with the unweighted degrees
    # initialize dictionary that will contain the core numbers
    cores_g = dict(zip(gg.vs['name'],[0]*len(gg.vs)))
#    layout = g.layout("kk")
#    igraph.plot(gg, layout = layout)
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

my_doc = "We  operate  a  change  of  paradigm  and  hy-pothesize that keywords are more likely to befound amonginfluentialnodes of a graph-of-words  rather  than  among  its  nodes  high  oneigenvector-related  centrality  measures.    Totest  this  hypothesis,  we  introduce  unsuper-vised techniques that capitalize ongraph de-generacy.Our  methods  strongly  and  sig-nificantly  outperform  all  baselines  on  twodatasets (short and medium size documents),and reach best performance on the third one(long documents). Keyword extraction is a central task in NLP. It findsapplications from information retrieval (notably websearch) to text classification, summarization, and vi-sualization.   In this study,  we focus on the task ofunsupervised  single-document  keyword  extraction.Following (Mihalcea and Tarau, 2004), we concen-trate onkeywordsonly, letting the task ofkeyphrasereconstruction as a post-processing step.More  precisely,  while  we  capitalize  on  a  graphrepresentation   of   text   like   several   previous   ap-proaches, we deviate from them by making the as-sumption that keywords are not found amongpres-tigiousnodes  (or  more  generally,  nodes  high  oneigenvector-related  centrality  metrics),  but  ratheramonginfluentialnodes. Those nodes may not havemany important  connections (like  their prestigiouscounterparts), but they are ideally placed at the core∗This research is supported in part by the OpenPaaS::NGproject.of  the  network.   In  other  words,  this  switches  theobjective from capturing thequalityandquantityofsingle node connections, to taking into account thedensityandcohesivenessof groups of nodes. To op-erate this change of paradigm,  we propose severalalgorithms that leverage the concept ofgraph degen-eracy"

my_doc = my_doc.replace('\n', '')

# pre-process document
my_tokens = clean_text_simple(my_doc,my_stopwords=stpwds,punct=punct)

g = terms_to_graph(my_tokens, 4)

## number of edges
#print(len(g.es))
#
## the number of nodes should be equal to the number of unique terms
#len(g.vs) == len(set(my_tokens))

#edge_weights = []
#
#for edge in g.es:
#    source = g.vs[edge.source]['name']
#    target = g.vs[edge.target]['name']
#    weight = edge['weight']
#    edge_weights.append([source, target, weight])

g = terms_to_graph(my_tokens,5)


#naive_core_dec(g,False)
#core_numbers = naive_core_dec(g,False)
#print(core_numbers)

#to test :
#print(core_numbers == {'account': 7.0, 'amonginfluentialnod': 7.0, 'amongpres-tigiousnod': 8.0, 'ap-proach': 8.0, 'as-sumpt': 8.0, 'baselin': 8.0, 'best': 8.0, 'central': 8.0, 'chang': 7.0, 'classif': 8.0, 'concept': 4.0, 'connect': 7.0, 'core∗thi': 7.0, 'de-generacyour': 8.0, 'degen-eraci': 4.0, 'document': 8.0, 'documentsand': 8.0, 'extract': 8.0, 'graph-of-word': 7.0, 'graphrepresent': 8.0, 'group': 7.0, 'high': 8.0, 'hy-pothes': 6.0, 'hypothesi': 8.0, 'import': 7.0, 'inform': 8.0, 'keyword': 8.0, 'like': 7.0, 'medium': 8.0, 'method': 8.0, 'metric': 7.0, 'mihalcea': 8.0, 'network': 7.0, 'nlp': 8.0, 'node': 8.0, 'ofkeyphrasereconstruct': 8.0, 'oneigenvector-rel': 8.0, 'onelong': 8.0, 'ongraph': 8.0, 'openpaasngprojectof': 7.0, 'paradigm': 7.0, 'part': 7.0, 'perform': 8.0, 'post-process': 8.0, 'prestigiouscounterpart': 7.0, 'previou': 8.0, 'ratheramonginfluentialnod': 7.0, 'reach': 8.0, 'research': 7.0, 'retriev': 8.0, 'sever': 8.0, 'severalalgorithm': 4.0, 'short': 8.0, 'single-docu': 8.0, 'size': 8.0, 'stepmor': 8.0, 'studi': 8.0, 'summar': 8.0, 'switch': 7.0, 'tarau': 8.0, 'task': 8.0, 'techniqu': 8.0, 'text': 8.0, 'thedensityandcohesivenessof': 7.0, 'thequalityandquantityofsingl': 7.0, 'third': 8.0, 'totest': 8.0, 'twodataset': 8.0, 'unsuper-vis': 8.0, 'vi-sual': 8.0, 'word': 7.0})