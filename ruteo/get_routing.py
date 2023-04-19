# -*- coding: latin-1 -*-
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from array import array
from ruteo.Instancia import inst
from ruteo.solvers import solvers
from ruteo.Funcion_Obj import Funcion_obj
from ruteo.Get_incum import get_incum
#from ruteo.Progress import progress



def routing(grupos,n_clusters,sede_grupos,coor_sedes,seed,dist_forma,algoritmo,ident,key_googlemaps):
    #Instanciar problema
    #print('iniciando...')
    c = 0 #contador
    coor_ruta = np.zeros((np.shape(grupos)[0]+n_clusters*2,6))
    coor_ruta = np.array(coor_ruta, dtype=object)

    if dist_forma == 'Haversine':
        Resumen_out = np.zeros((n_clusters,4))
    elif dist_forma =='Google':
        Resumen_out = np.zeros((n_clusters,6))
    Resumen_out[:,0] = np.arange(1,n_clusters+1)

    rutas = np.zeros((n_clusters,2),dtype=array)
    rutas[:,0] = np.arange(1,n_clusters+1)

    #progreso = progress(ident) #se inicializa datos de progreso
    #progreso.set_Iteraciones(0)
    #progreso.set_Cantidad_distancias(0)

    for i in range(n_clusters):

        grupo = i # seleccionar cluster
        sede_grupo_k = sede_grupos[sede_grupos[:,1]==grupo]
        sede_grupo_k = sede_grupo_k[sede_grupo_k[:, 2].argsort()] # ordena de menor a mayor las distancias de sedes a cluster (grupo) 
        sede_grupo_k = int(sede_grupo_k[0,0]) # selecciona la sede como el primer elemento. 
        coor_sede_k = coor_sedes[sede_grupo_k,:] # se obtienen las coordenadas de la sede
        grupo_k = np.zeros((np.shape(grupos)[0]+1,np.shape(grupos)[1]))
        grupo_k = np.array(grupo_k, dtype=object) # Transformación a datos tipo objeto
        grupo_k[0,0] = grupo # se define la sede del grupo seleccionado
        grupo_k[0,2:4] = coor_sede_k
        grupo_k[1:,:] = grupos
        grupo_k = grupo_k[grupo_k[:,0] == grupo]
    
        #progreso.set_Iteraciones((i)*100/n_clusters)
        #progreso.set_Cantidad_distancias((np.shape(grupo_k)[0])**2)

        #print('---cluster número: ',i, ' ---')
        #print('numero de distancias a obtener: ', (np.shape(grupo_k)[0])**2)

        
        #dist_forma='haversine'
        dist = inst(grupo_k,dist_forma,key_googlemaps,tipo='distance') #tiempo o distancia (haversine, google) - Distancias para solver principal
        genetico_main = solvers(dist,seed,algoritmo) #se instancia la clase para el solver principal #################
        

        if dist_forma == 'Haversine':
            dist2 = dist.copy()
            VecinoCercano = solvers(dist2,seed,'VecinoCercano') # Solver para referencia
            Sol_Incumbente,Incumbente,Incum_acumulado = genetico_main.s() #Algoritmo de ruteo
            
            Sol_ref,Incum_ref = VecinoCercano.s() #Algoritmo de ruteo de referencia
            
            Incum_ref = Funcion_obj(Sol_ref,dist) #Se recalcula para comparaciones
            Resumen_out[i,1] = round(Incum_ref,2)
            Resumen_out[i,2] = round(Incumbente,2)
            Resumen_out[i,3] = round((Incum_ref - Incumbente)*100/Incumbente,2)

        elif dist_forma =='Google':

            dist2 = inst(grupo_k,'Haversine',key_googlemaps,tipo='distance') #tiempo o distancia (haversine, google) - Distancias para Solver de comparacion
            
            genetico_ref = solvers(dist2,seed,algoritmo) # Solver para referencia
            Sol_Incumbente,Incumbente,Incum_acumulado = genetico_main.s() #Algoritmo de ruteo
            Sol_Incumbente2,Incumbente2,Incum_acumulado2 = genetico_ref.s() #Algoritmo de ruteo - Referencia
            
            VecinoCercano = solvers(dist2,seed,'VecinoCercano') # Solver para referencia
            Sol_ref,Incum_ref = VecinoCercano.s() #Algoritmo de ruteo de referencia
            
            Incum_ref = Funcion_obj(Sol_ref,dist) #Se recalcula para comparaciones
            Incumbente2 = Funcion_obj(Sol_Incumbente2,dist) #Se recalcula para comparaciones
            Resumen_out[i,1] = round(Incum_ref,2)
            Resumen_out[i,2] = round(Incumbente,2)
            Resumen_out[i,3] = round(Incumbente2,2)
            Resumen_out[i,4] = round((Incum_ref - Incumbente)*100/Incumbente,2)
            Resumen_out[i,5] = round((Incum_ref - Incumbente2)*100/Incumbente2,2)
       
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
    

    #Resumen resultados
    if dist_forma == 'Haversine':
        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
            'Route','ref_cost','Haversine_cost','Haversine_saves(%)'
            ])
        #print('---Resumen resultados---\n')
        #print(Resumen_df.to_markdown())
    elif dist_forma =='Google':
        Resumen_df = pd.DataFrame(data=Resumen_out,columns=[
            'Route','ref_cost', 'Dist_google_cost','Haversine_cost',
            'Google_saves(%)', 'Haversine_saves(%)'
            ])
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

    return Resumen_df,df_plot,df_rutas