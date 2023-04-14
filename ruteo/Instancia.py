import numpy as np
from ruteo.DistanceMatrix import get_distances
from ruteo.haversine import haversine


def inst(grupo_k,dist_forma,tipo):
    Numclientes = np.shape(grupo_k)[0]
    Coordenadas = np.zeros((Numclientes,2))
    Coordenadas[:,0] = grupo_k[:,3] #latitud
    Coordenadas[:,1] = grupo_k[:,2] #longitud
    clientes = list(map(str, np.array(range(Numclientes))))

    #Matriz de distancias API google
    if dist_forma == 'Google':
        #convertir coordenadas en lista de tuplas
        coord = list(map(tuple, Coordenadas))
        #Obtener distancias
        dist = get_distances(coord,clientes,tipo,0)
        #print(dist)
    
    #Usando distancias de haversine
    elif dist_forma == 'Haversine':
        dist = np.zeros((Numclientes,Numclientes))
        for i in range(Numclientes):
            for j in range(Numclientes):
                dist[i,j] = haversine(Coordenadas[i,1],Coordenadas[i,0],Coordenadas[j,1],Coordenadas[j,0]) #lon,lat

    #else:
    #    # Calculo de la matriz de distancia
    #    dist = np.zeros((Numclientes,Numclientes))
    #    for i in range(Numclientes):
    #        for j in range(Numclientes):
    #            dist[i,j] = np.sqrt(pow(Coordenadas[i,0]-Coordenadas[j,0],2)+pow(Coordenadas[i,1]-Coordenadas[j,1],2)) 
    
    return dist