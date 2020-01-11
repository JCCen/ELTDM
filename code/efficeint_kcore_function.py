import copy

def better_core_dec(g,weighted):
#basé sur https://github.com/networkx/networkx/blob/b8460be7b055dc18e2fdde3b8739d41f0c0064a3/networkx/algorithms/core.py#L138
    
    # work on clone of g to preserve g 
    gg = copy.deepcopy(g)

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