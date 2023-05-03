import numpy as np
import math
from sklearn.cluster import KMeans
from ruteo.haversine import haversine
from ruteo.distance_matrix_base import distance_matrix

def cluster_rest(grupo_k,sede_cluster,objective_max):

	# This function corrects the clusters when overcoming the objective_max
	print('grupo_k: \n',grupo_k)

	last_clus = len(sede_cluster)-1
	route =  grupo_k[:,4].astype(int) #it is getting cluster's members
	NumCustomers = len(route)
	route_mask = np.arange(NumCustomers+1) # it is using to get distances in distance matrix
	route_mask[-1] = 0
	coor = grupo_k[:,2:4] 

	# Distance matrix
	dist = distance_matrix(coor)

	dist_route = 0
	#print(route)
	#print(route_mask)
	for i in range(NumCustomers):
		dist_route = dist_route + dist[route_mask[i],route_mask[i+1]]
	print('dist_route:',dist_route)
	if dist_route > objective_max and len(coor[1:,:])>1:
		# split the cluster
		parts =  math.ceil(dist_route/objective_max)
		
		if parts > len(coor[1:,:]):
			parts = len(coor)-1
			kmeans = KMeans(parts,n_init='auto').fit(coor[1:,:]) #Coor don't have start-point
		else: # It is required create subclusters
			kmeans = KMeans(parts,n_init='auto').fit(coor[1:,:]) 
		labels = kmeans.labels_+1
		print("parts",parts)
		#print("labels:",labels)
		size_grupo_k = grupo_k.shape
		subClusters = np.zeros((size_grupo_k[0],size_grupo_k[1]+2),dtype=object)
		for i in kmeans.labels_:
			subClusters[:,0:size_grupo_k[1]] = grupo_k # group data
			subClusters[1:,size_grupo_k[1]] = labels # subcluster
		
		print('subClusters:\n',subClusters)
		array_dist_subCluster = np.zeros((parts,1))
		for i in range(1,parts+1):
			#print('subCluster num:', i)
			subClusterMember = subClusters[subClusters[:,5]==i]
			#print('subClusterMember:\n', subClusterMember)
			subRoute_mask = np.arange(len(subClusterMember)+2) # it is using to get distances in distance matrix
			subRoute_mask[-1] = 0
			#print('subRoute_mask:\n',subRoute_mask)
			coor_sub = np.zeros((len(subClusterMember)+1,2))
			coor_sub[0,:] = subClusters[0,2:4]
			coor_sub[1:,:] = subClusterMember[:,2:4]
			#print('coor_sub:\n', coor_sub)
			dist_subCluster = distance_matrix(coor_sub)
			#print('dist_subCluster:\n',dist_subCluster)
			dist_subRoute = 0
			for j in range(len(coor_sub)):
				dist_subRoute = dist_subRoute + dist_subCluster[subRoute_mask[j],subRoute_mask[j+1]]
			array_dist_subCluster[i-1] = dist_subRoute
		print('array_dist_subCluster:\n',array_dist_subCluster)


	# Distance verification

	#for i in kmeans.labels_:
	#	subRoute = len(route[i,:])
	#	for j in range(subRoute):
	#		dist_route = dist_route + dist[route_mask[i],route_mask[i+1]]
	#		print(dist_route)


