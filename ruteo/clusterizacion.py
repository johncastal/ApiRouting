from sklearn.cluster import KMeans
import numpy as np
from ruteo.sede import sede


def clusterizacion(Datos,n_clusters,seed):

    #split headquarters y customers
    pat = '^\d'  #starts with a number
    df_clientes = Datos[Datos.label.str.contains(pat)]
    df_sedes = Datos[~Datos.label.str.contains(pat)]

    df_clientes = df_clientes.to_numpy()
    coor = df_clientes[:,1:3] #lon,lat
    kmeans = KMeans(n_clusters,n_init='auto',random_state=seed).fit(coor)
    centroids = kmeans.cluster_centers_
    #To get headquarters
    sede_grupos = sede(centroids,df_sedes)

    Numclientes = np.shape(coor)[0]
    grupos = np.zeros((Numclientes,5))


    grupos[:,0] = kmeans.labels_
    grupos[:,1] = df_clientes[:,0]
    grupos[:,2:4] = coor
    grupos[:,4] = np.arange(1,Numclientes+1)

    return grupos,sede_grupos,df_sedes