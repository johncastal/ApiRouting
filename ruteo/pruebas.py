# -*- coding: utf-8 -*-
import numpy as np
from Funcion_Obj import Funcion_obj
from haversine import haversine


def Cluster(grupo_k):
	n_routes = np.amax(grupo_k, axis=0)[0]
	for i in range(n_routes):
		route_i =  grupo_k[grupo_k[:,0]==i]
		print(route_i)
