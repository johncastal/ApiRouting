import numpy as np
from ruteo.DistanceMatrix import get_distances
from ruteo.haversine import haversine
from ruteo.elevation import elevation


def inst(grupo_k,dist_forma,weights,key_googlemaps,):
    Numclientes = np.shape(grupo_k)[0]
    Coordenadas = np.zeros((Numclientes,2))
    Coordenadas[:,0] = grupo_k[:,3] #latitud
    Coordenadas[:,1] = grupo_k[:,2] #longitud
    clientes = list(map(str, np.array(range(Numclientes))))

    #Distance Matrix API google
    if dist_forma == 'Google':
        
        coord = list(map(tuple, Coordenadas))
        #To get  distances
        dist,time = get_distances(coord,clientes,key_googlemaps)
    
    #Haversine distances
    elif dist_forma == 'Haversine':
        dist = np.zeros((Numclientes,Numclientes))
        for i in range(Numclientes):
            for j in range(Numclientes):
                dist[i,j] = haversine(Coordenadas[i,1],Coordenadas[i,0],Coordenadas[j,1],Coordenadas[j,0]) #lon,lat
        time = dist / 15 #15km/h as a average speed


    
    # Emissions matrix
    emissions = np.zeros((Numclientes,Numclientes))
    cpg = 28.968 #km/gallon
    epg = 10.180 #grams/gallon
    u = 0.015 # friction coeficient

    if dist_forma == 'Google':
        for i in range(Numclientes):
            elev_1 = elevation(Coordenadas[i,1],Coordenadas[i,0],key_googlemaps) #lon,lat
            for j in range(Numclientes): 
                if dist[i,j] > 0:
                    elev_2 = elevation(Coordenadas[j,1],Coordenadas[j,0],key_googlemaps) #lon,lat
                    delta = (elev_1-elev_2)/1000
                    if delta < 0:
                        delta=0
                    tetha = np.arctan(delta/dist[i,j])
                    alpha = abs(np.sin(tetha) - u * np.cos(tetha))
                    emissions[i,j] = (dist[i,j]/cpg) * epg * (1+alpha) 

    elif dist_forma == 'Haversine':
        for i in range(Numclientes):
            for j in range(Numclientes): 
                if dist[i,j] > 0:
                    alpha = 0.1
                    emissions[i,j] = (dist[i,j]/cpg) * epg * (1+alpha) 
        
    # Generate a unified matrix

    # Find the minimum and maximum values in the matrix
    min_value_dist = np.min(dist)
    max_value_dist = np.max(dist)
    min_value_emissions = np.min(emissions)
    max_value_emissions = np.max(emissions)

    normalized_dist = (dist - min_value_dist) / (max_value_dist - min_value_dist)
    normalized_emissions = (emissions - min_value_emissions) / (max_value_emissions - min_value_emissions)

    dist_bi = (normalized_dist * weights[0]) + (normalized_emissions * weights[1])

    
    return dist,time,dist_bi,emissions