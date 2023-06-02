import numpy as np

def Funcion_obj(Hijo,dist):
    #Calcula la funcion objetivo de una solucion

    F_obj = 0;
    NumClientes = np.shape(Hijo)[0]
    for i in range(NumClientes-1):
        F_obj = F_obj + dist[Hijo[i],Hijo[i+1]]
    return F_obj
