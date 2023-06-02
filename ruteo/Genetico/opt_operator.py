import numpy as np
from ruteo.Funcion_Obj import Funcion_obj


def opt_operator(vector, dist):
    S0 = Funcion_obj(vector,dist)
    Vector0 = vector.copy() 
    size=np.shape(vector)
    for i in range(1,size[0]-1): #index
        for j in range(1,size[0]-1): #position
            swapped_vector = vector.copy() 
            swapped_vector[j] =  vector[i]
            swapped_vector[i] =  vector[j]
            S1 = Funcion_obj(swapped_vector,dist)
            if S1<S0:
                S0=S1.copy()
                vector = swapped_vector.copy()
    return swapped_vector
