from ruteo.haversine import haversine
import numpy as np
	

def distance_matrix(coor):
	NumCustomers = len(coor)
	dist = np.zeros((NumCustomers,NumCustomers))
	for i in range(NumCustomers):
		for j in range(NumCustomers):
			dist[i,j] = haversine(coor[i,1],coor[i,0],coor[j,1],coor[j,0]) #lon,lat
	return dist