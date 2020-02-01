from __future__ import print_function
import numpy as np

def elbow_cython(sorted_scores):
    sorted_scores = [np.array(i) for i in sorted_scores]
    #traduit de R, du code de l'article original
    if len(sorted_scores)<3:
        elbow_point=1
    else:
         # first point
        first_point = sorted_scores[0]
         # last point
        last_point =sorted_scores[-1]
        first_point-last_point
        
        # compute distance between each point of "sorted_scores" and the "first-last" line
        distances = []
    
        for index,point in enumerate(sorted_scores):
            point= np.array(point)
            #calculate distance between the point and the line drawn between first point and last point
            d=np.cross(last_point-first_point,point-first_point)/np.linalg.norm(last_point-first_point)
            distances.append(abs(d))
            
            
        if np.max(distances)>0:
            x_elbow=sorted_scores[np.argmax(distances)]
        else :
            x_elbow=sorted_scores[0]
            
        return x_elbow
