import string
from nltk.corpus import stopwords
#import nltk
#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')

#import os
#os.chdir() # to change working directory to where functions live
# import custom functions
from library import clean_text_simple, terms_to_graph, core_dec
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


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


for w in range(2,10):
    g = terms_to_graph(my_tokens, w)
    ### fill the gap (print density of g) ###
    print("for a window size of {win_size} the density of g is {density}.".format(win_size=w,density=g.density()))

# =============================================================================
 # Plotting impact of window size on density
t = range(2,20)
graph_densities=[terms_to_graph(my_tokens, i).density() for i in range(2,20)]

fig, ax = plt.subplots()
ax.plot(t,graph_densities)

ax.set(xlabel='window size', ylabel='graph density',
        title='Impact of window size on the density of the graph')
ax.grid()
 
fig.savefig("density_wind_size.png")
plt.show() 
# =============================================================================

# decompose g
core_numbers = core_dec(g,False)


### fill the gap (compare 'core_numbers' with the output of the .coreness() igraph method) ###
cores_g = dict(zip(g.vs["name"],g.coreness()))
shared_items = {k: cores_g[k] for k in cores_g if k in core_numbers and cores_g[k] == core_numbers[k]}
print("Our results and the .coreness method of igraph have {} discrepancies".format(abs(len(core_numbers)-(len(shared_items)))))


# retain main core as keywords
max_c_n = max(core_numbers.values())
keywords = [kwd for kwd, c_n in core_numbers.items() if c_n == max_c_n]
