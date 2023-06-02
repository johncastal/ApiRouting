import numpy as np
from ruteo.DistanceMatrix import get_distances
from ruteo.haversine import haversine


def inst(Numclientes,Coordenadas,clientes,elev,dist_forma,objective,weights,key_googlemaps,ems):

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


    if ems:
        # Emissions matrix
        emissions = np.zeros((Numclientes,Numclientes))
        cpg = 28.968 #km/gallon
        epg = 10.180 #grams/gallon
        u = 0.015 # friction coeficient

        if dist_forma == 'Google':
            for i in range(Numclientes):
                elev_1 = elev[i] #lon,lat
                for j in range(Numclientes): 
                    if dist[i,j] > 0:
                        elev_2 =elev[j] #lon,lat
                        delta = (elev_1-elev_2)/1000
                        if delta>0:
                            tetha = np.arctan(delta/dist[i,j])
                        else:
                            tetha = 0
                        alpha = abs(np.sin(tetha) - u * np.cos(tetha))
                        emissions[i,j] = (dist[i,j]/cpg) * epg * (1+(alpha*dist[i,j]/0.1))

        elif dist_forma == 'Haversine':
            for i in range(Numclientes):
                elev_1 = elev[i] #lon,lat
                for j in range(Numclientes): 
                    if dist[i,j] > 0:
                        elev_2 =elev[j] #lon,lat
                        delta = (elev_1-elev_2)/1000
                        if delta>0:
                            tetha = np.arctan(delta/dist[i,j])
                        else:
                            tetha = 0
                        alpha = abs(np.sin(tetha) - u * np.cos(tetha))
                        emissions[i,j] = (dist[i,j]/cpg) * epg * (1+(alpha*dist[i,j]/0.1)) * 1.2
            
        # Generate a unified matrix

        # Find the minimum and maximum values in the matrix
        if objective == "Distance":
            M_obj = dist
        elif objective == "Time":
            M_obj = time

        min_value_dist = np.min(M_obj)
        max_value_dist = np.max(M_obj)
        min_value_emissions = np.min(emissions)
        max_value_emissions = np.max(emissions)

        normalized_dist = (M_obj - min_value_dist)*1000 / (max_value_dist - min_value_dist)
        normalized_emissions = (emissions - min_value_emissions)*1000  / (max_value_emissions - min_value_emissions)
        
        dist_bi = (normalized_dist * weights[0]) + (normalized_emissions * weights[1])

        #dist_bi = (dist * weights[0]) + (emissions * weights[1])
    else:
        dist_bi=0
        emissions=0
    
    return dist,time,dist_bi,emissions