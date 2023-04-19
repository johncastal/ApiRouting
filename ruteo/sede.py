import pandas as pd
import numpy as np
from ruteo.haversine import haversine
import json

#Obtiene las sedes para cada cluster
#Retorna array: col1: municipio, col2:cluster, col3: distancia entre municipio y cluster

def sede(centroids,df_sedes):
    
    sedes = df_sedes

    l = np.shape(centroids)[0]
    p = len(sedes['label'])
    dist_sede = np.zeros((l*p,3))
    #centroids #lon,lat
    k=0
    for i in range(p):
        for j in range(l):
            dist_sede[k,0]=i #sede
            dist_sede[k,1]=j #cluster o centroide
            dist_sede[k,2]=haversine(sedes['longitud'][i],sedes['latitud'][i],centroids[j,0],centroids[j,1])
            k+=1
    
    return dist_sede
