import numpy as np
from ruteo.Funcion_Obj import Funcion_obj



def VecinoCercano(dist):
    Numclientes = np.shape(dist)[0]
    Solucion = np.zeros((Numclientes+1)).astype(int)
    Distancias = np.zeros((Numclientes,2))
    j=0 # comienzo en la sede
    p=0
    for i in range(Numclientes-1):
        Distancias[:,0] = range(Numclientes)
        Distancias[:,1] = dist[0:,j]
        Distancias = Distancias[Distancias[:, 1].argsort()]
        for p in range(len(Distancias)):
            flag = 0
            index = int(Distancias[p,0])
            for k in range(Numclientes-1):
                if index == Solucion[k]:
                    flag = 1
                    break
            if flag ==0:
                Solucion[i+1] = index
                j = index
                break

    Incum_ref = Funcion_obj(Solucion,dist)
    return Solucion, Incum_ref


    
