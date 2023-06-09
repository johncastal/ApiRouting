# -*- coding: latin-1 -*-
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from array import array
from ruteo.Instancia import inst
from ruteo.solvers import solvers
from ruteo.Funcion_Obj import Funcion_obj
from ruteo.Get_incum import get_incum
from ruteo.elevation import elevation
#from ruteo.cluster_rest import cluster_rest
#from ruteo.Progress import progress



def routing(grupos,n_clusters,sede_grupos,coor_sedes,seed,dist_forma,algoritmo,objective,ident,emissions,weights,key_googlemaps):
    
    #Instanciar problema

    c = 0 #contador
    coor_ruta = np.zeros((np.shape(grupos)[0]+n_clusters*2,6))
    coor_ruta = np.array(coor_ruta, dtype=object)

    #if dist_forma == 'Haversine':
    #    Resumen_out = np.zeros((n_clusters,4))
    #elif dist_forma =='Google':
    #    Resumen_out = np.zeros((n_clusters,4))

    Resumen_d_out = np.zeros((n_clusters,5))
    Resumen_d_out[:,0] = np.arange(1,n_clusters+1)
    Resumen_t_out = np.zeros((n_clusters,5))
    Resumen_t_out[:,0] = np.arange(1,n_clusters+1)

    Emissions_out = np.zeros((n_clusters,5))
    Emissions_out[:,0] = np.arange(1,n_clusters+1)

    rutas = np.zeros((n_clusters,2),dtype=array)
    rutas[:,0] = np.arange(1,n_clusters+1)


   
    sede_grupos = sede_grupos[np.lexsort((sede_grupos[:, 2], sede_grupos[:, 1]))]
    unique_first_col = np.unique(sede_grupos[:, 1], axis=0)

    # Create a new array with unique first column values
    sede_cluster = np.zeros((unique_first_col.shape[0], sede_grupos.shape[1]))
    
    # Iterate over unique values and add to new array
    for i, val in enumerate(unique_first_col):
        sede_cluster[i,:] = sede_grupos[sede_grupos[:, 1] == val][0,:]

    #print("sedes:\n", sede_cluster, "\n")

    for i in range(n_clusters):

        grupo = i # seleccionar cluster
        sede_grupo_k = sede_cluster[sede_cluster[:,1]==grupo]
        #sede_grupo_k = sede_grupo_k[sede_grupo_k[:, 2].argsort()] # ordena de menor a mayor las distancias de sedes a cluster (grupo) 
        sede_grupo_k = int(sede_grupo_k[0,0]) # selecciona la sede como el primer elemento. 
        coor_sede_k = coor_sedes[sede_grupo_k,:] # se obtienen las coordenadas de la sede
        grupo_k = np.zeros((np.shape(grupos)[0]+1,np.shape(grupos)[1]))
        grupo_k = np.array(grupo_k, dtype=object) # Transformación a datos tipo objeto
        grupo_k[0,0] = grupo # se define la sede del grupo seleccionado
        grupo_k[0,2:4] = coor_sede_k
        grupo_k[1:,:] = grupos
        grupo_k = grupo_k[grupo_k[:,0] == grupo]

        # Datos para instanciar problema
        Numclientes = np.shape(grupo_k)[0]
        Coordenadas = np.zeros((Numclientes,2))
        Coordenadas[:,0] = grupo_k[:,3] #latitud
        Coordenadas[:,1] = grupo_k[:,2] #longitud
        clientes = list(map(str, np.array(range(Numclientes))))

        # To get elevation vector
        elev = np.zeros((Numclientes))
        for k in range(Numclientes):
            elev[k] = elevation(Coordenadas[k,1],Coordenadas[k,0],key_googlemaps) #lon,lat
        
        if dist_forma == 'Haversine':
            dist,time,dist_bi,M_emissions = inst(Numclientes,Coordenadas,clientes,elev,dist_forma,objective,weights,key_googlemaps,1) #tiempo o distancia (haversine, google) - Distancias para solver principal
            dist2 = dist.copy()
            time2 = time.copy()
        else:
            dist,time,dist_bi,M_emissions = inst(Numclientes,Coordenadas,clientes,elev,dist_forma,objective,weights,key_googlemaps,1) #tiempo o distancia (haversine, google) - Distancias para solver principal
            dist2,time2,_,_ = inst(Numclientes,Coordenadas,clientes,elev,'Haversine',objective,weights,key_googlemaps,0) #tiempo o distancia (haversine, google) - Distancias para Solver de comparacion

        if emissions:
            solver = solvers(dist_bi,seed,algoritmo) #This can mix emissions with distance
            VecinoCercano = solvers(dist2,seed,'VecinoCercano') #This can mix emissions with distance
        else:
            if objective == "Distance":
                solver = solvers(dist,seed,algoritmo) #It is used to get solution through the distance in km
                VecinoCercano = solvers(dist2,seed,'VecinoCercano') #It is used to get solution through the distance in km
            elif objective == "Time":
                solver = solvers(time,seed,algoritmo) #It is used to get solution through the time in hours
                VecinoCercano = solvers(time2,seed,'VecinoCercano') #It is used to get solution through the distance in km

        # Solutions

        Sol_Incumbente,_ = solver.s() #Algoritmo de ruteo
        Sol_ref,_ = VecinoCercano.s() #Algoritmo de ruteo de referencia
        
        #if objective == "Distance":
        #    Incum_ref_d = Funcion_obj(Sol_ref,dist) 
        #    Incumbente_d = Funcion_obj(Sol_Incumbente,dist)
        #elif objective == "Time":
        #    Incum_ref_t = Funcion_obj(Sol_ref,time) 
        #    Incumbente_t = Funcion_obj(Sol_Incumbente,time)

        Incum_ref_d = Funcion_obj(Sol_ref,dist) 
        Incumbente_d = Funcion_obj(Sol_Incumbente,dist)

        Incum_ref_t = Funcion_obj(Sol_ref,time) 
        Incumbente_t = Funcion_obj(Sol_Incumbente,time)

        Incum_ref_emissions = Funcion_obj(Sol_ref,M_emissions)
        Incumbent_emissions = Funcion_obj(Sol_Incumbente,M_emissions)

        Emissions_out[i,1] = round(Incum_ref_emissions,2)
        Emissions_out[i,2] = round(Incumbent_emissions,2)
        Emissions_out[i,3] = round(Incum_ref_emissions-Incumbent_emissions,2)
        Emissions_out[i,4] = round((Incum_ref_emissions-Incumbent_emissions)*100/Incumbent_emissions,2)

        Resumen_d_out[i,1] = round(Incum_ref_d,2)
        Resumen_d_out[i,2] = round(Incumbente_d,2)
        Resumen_d_out[i,3] = round((Incum_ref_d - Incumbente_d),2)
        Resumen_d_out[i,4] = round((Incum_ref_d - Incumbente_d)*100/Incumbente_d,2)

        Resumen_t_out[i,1] = round(Incum_ref_t,2)
        Resumen_t_out[i,2] = round(Incumbente_t,2)
        Resumen_t_out[i,3] = round((Incum_ref_t - Incumbente_t),2)
        Resumen_t_out[i,4] = round((Incum_ref_t - Incumbente_t)*100/Incumbente_t,2)
        

        sol_incumbete_real,orden_cuentas = get_incum(Sol_Incumbente,grupo_k)
        #print(rutas)
        #print('Ruta: ', sol_incumbete_real)
        separator = '-'
        rutas[i,1] = separator.join(map(str, sol_incumbete_real.tolist()))


        #Construccion dataframe de salida
        a = c+np.shape(grupo_k)[0]+1
        coor_ruta[c:c+np.shape(grupo_k)[0]+1,0] = Sol_Incumbente.T
        coor_ruta[c:c+np.shape(grupo_k)[0],4] = orden_cuentas[0:-1]
        coor_ruta[c:c+np.shape(grupo_k)[0],5] = sol_incumbete_real[0:-1]
        k=0
        tam_sol = np.shape(grupo_k)[0]
        for j in range(c,c+tam_sol):
            coor_ruta[j,1] = grupo_k[Sol_Incumbente[k],2]
            coor_ruta[j,2] = grupo_k[Sol_Incumbente[k],3]
            k+=1
        coor_ruta[tam_sol+c,1] = grupo_k[Sol_Incumbente[0],2]
        coor_ruta[tam_sol+c,2] = grupo_k[Sol_Incumbente[0],3]
        coor_ruta[c:c+tam_sol+1,3] = grupo
        c = j + 2
    
    # To get highlights
    #if objective == "Distance":
    #    highlights = {"Total_incumbent": "{:.2f}".format(np.sum(Resumen_out[:, 2])) + " km",  
    #                  "Saves_routes" :  "{:.2f}".format(np.sum(Resumen_out[:, 3])) + " km",
    #                  "Total_saves(%)" :  "{:.2f}".format(100*(1-(np.sum(Resumen_out[:, 2])/np.sum(Resumen_out[:, 1])))) + "%",
    #                  "Mean_distance_cluster" : "{:.2f}".format(np.mean(sede_cluster[:,2])) + " km",
    #                  "Total_CO2_emissions" : "{:.2f}".format(np.sum(Emissions_out[:,2])) + " gramsCO2",
    #                  "CO2_saves_routes" : "{:.2f}".format(np.sum(Emissions_out[:,3])) + " gramsCO2",
    #                  "CO2_saves" : "{:.2f}".format(100*(1-(np.sum(Emissions_out[:, 2])/np.sum(Emissions_out[:, 1])))) + "%"
    #                  }
    #elif objective == "Time":
    #    highlights = {"Total_incumbent": "{:.2f}".format(np.sum(Resumen_out[:, 2])) + " Hours",  
    #                  "Saves_routes" :  "{:.2f}".format(np.sum(Resumen_out[:, 3])) + " Hours",
    #                  "Total_saves(%)" :  "{:.2f}".format(100*(1-(np.sum(Resumen_out[:, 2])/np.sum(Resumen_out[:, 1])))) + "%",
    #                  "Mean_distance_cluster" : "{:.2f}".format(np.mean(sede_cluster[:,2])) + " Km",
    #                  "Total_CO2_emissions" : "{:.2f}".format(np.sum(Emissions_out[:,2])) + " gramsCO2",
    #                  "CO2_saves_routes" : "{:.2f}".format(np.sum(Emissions_out[:,3])) + " gramsCO2",
    #                  "CO2_saves" : "{:.2f}".format(100*(1-(np.sum(Emissions_out[:, 2])/np.sum(Emissions_out[:, 1])))) + "%"
    #                  }


    highlights = dict(
                      dist = {
                        "Total_incumbent_d": "{:.2f}".format(np.sum(Resumen_d_out[:, 2])) + " km",  
                        "Saves_routes_d" :  "{:.2f}".format(np.sum(Resumen_d_out[:, 3])) + " km",
                        "Total_saves_d(%)" :  "{:.2f}".format(100*(1-(np.sum(Resumen_d_out[:, 2])/np.sum(Resumen_d_out[:, 1])))) + "%",
                        "Mean_distance_cluster" : "{:.2f}".format(np.mean(sede_cluster[:,2])) + " km",
                      },
                      time = {
                        "Total_incumbent_t": "{:.2f}".format(np.sum(Resumen_t_out[:, 2])) + " Hours",  
                        "Saves_routes_t" :  "{:.2f}".format(np.sum(Resumen_t_out[:, 3])) + " Hours",
                      },
                      emissions = {
                        "Total_CO2_emissions" : "{:.2f}".format(np.sum(Emissions_out[:,2])) + " gramsCO2",
                        "CO2_saves_routes" : "{:.2f}".format(np.sum(Emissions_out[:,3])) + " gramsCO2",
                        "CO2_saves" : "{:.2f}".format(100*(1-(np.sum(Emissions_out[:, 2])/np.sum(Emissions_out[:, 1])))) + "%"
                      })
                      

    #Resumen resultados

    Resumen_d_df = pd.DataFrame(data=Resumen_d_out,columns=[
                'Route','ref_cost(km)','opt_cost(km)','opt_saves(km)','opt_saves(%)'
                ])
    Resumen_t_df = pd.DataFrame(data=Resumen_t_out,columns=[
                'Route','ref_time(H)','opt_time(H)','opt_saves(H)','opt_saves(%)'
                ])
    Emissions_df = pd.DataFrame(data=Emissions_out,columns=[
            'Route','ref_emis(gramsCO2)','opt_emis(gramsCO2)','CO2_saves(gramsCO2)','CO2_saves(%)'
            ])

    #if dist_forma == 'Haversine':
    #    if objective == "Distance":
    #        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
    #            'Route','ref_cost(km)','Haversine_cost(km)','Haversine_saves(km)','Haversine_saves(%)'
    #            ])
    #    elif objective == "Time":
    #        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
    #            'Route','ref_cost(H)','Haversine_cost(H)','Haversine_saves(H)','Haversine_saves(%)'
    #            ])
    #    #print('---Resumen resultados---\n')
    #    #print(Resumen_df.to_markdown())
    #elif dist_forma =='Google':
    #    if objective == "Distance":
    #        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
    #            'Route','ref_cost(km)', 'Google_cost(km)', 'Google_saves(km)',
    #            'Google_saves(%)'
    #            ])
    #    elif objective == "Time":
    #        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
    #            'Route','ref_cost(H)', 'Google_cost(H)', 'Google_saves(H)',
    #            'Google_saves(%)'
    #            ])
    #
    #Emissions_df = pd.DataFrame(data=Emissions_out,columns=[
    #        'Route','ref_emis(gramsCO2)','opt_emis(gramsCO2)','CO2_saves(gramsCO2)','CO2_saves(%)'
    #        ])

        #print('---Resumen resultados---\n')
        #print(Resumen_df.to_markdown())

    #Dataframe rutas
    df_rutas = pd.DataFrame(data=rutas,columns=['No.Route','Route Solution'])
    #print(df_rutas.to_markdown())

    #Limpiar datos en ejecuciones parciales ()
    ind=0
    for i in range(np.shape(coor_ruta)[0]):
        if coor_ruta[i,1] == 0:
            ind = i
            break
    if ind>0:
        coor_ruta = coor_ruta[0:ind,:]

    df_plot = pd.DataFrame(data=coor_ruta,columns=['customer','longitud','latitud','cluster','code','customer No.'])
    df_plot['customer'] = df_plot['customer'].astype(int)
    df_plot['cluster'] = df_plot['cluster']+1
    #df_plot.to_parquet('Datos/df_plot.parquet')
    #print(df_plot.to_markdown())


    #progreso.set_Iteraciones(100)
    #progreso.set_Cantidad_distancias(0)

    return Resumen_d_df,Resumen_t_df,df_plot,df_rutas,highlights,Emissions_df