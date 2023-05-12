# -*- coding: latin-1 -*-
import numpy as np
from ruteo.Funcion_Obj import Funcion_obj
from ruteo.Genetico.SeleccionPadres import SeleccionPadres
from ruteo.Genetico.Cruzamiento import Cruzamiento
from ruteo.Genetico.Mutacion  import Mutacion

def genetico(dist,seed):
    #Definición de parámetros del algoritmo
    np.random.seed(seed)
    
    print(dist)
    Numclientes = np.shape(dist)[0]
    
    # definición de parámetros de algoritmo
    Tam_pob = 50    # tamaño de la población
    k = 3          # Tamaño de las muestra para la selección
    #Tc = 0.9       # Tasa de cruzamiento
    Tm = 0.9        # Tasa de mutación
    MaxGen = (Numclientes**2)*100  # Máximo de iteraciones
    Reinicio = 1000 # Número de iteraciones para reiniciar población
    # contadores
    Contador_incumbentes = 0
    
    
    #Paso 1a: generar la población inicial
    Pob = np.zeros((Tam_pob,Numclientes+1)).astype(int)
    F_obj = np.zeros((Tam_pob,1));
    for i in range(Tam_pob):
        Pob[i,1:Numclientes] = np.random.permutation(np.array(range(1,Numclientes)))
        #print(Pob[i], ' - ',np.shape(np.unique(Pob[i]))[0],' - ', np.shape(np.unique(Pob[i]))[0]==Numclientes)
        F_obj[i,0] =  Funcion_obj(Pob[i,:],dist)
    
    
    #Paso 1c: Obtener la incumbente: individuo con mejor solución
    Incumbente = np.min(F_obj)
    pos_incum = np.argmin(F_obj)
    Sol_Incumbente = Pob[pos_incum,:]
    Incum_acumulado = np.zeros((int(MaxGen*0.3),2))


    #Inicio de evolución
    for q in range(MaxGen):
        #Paso 2: Selección de padres
        Padre1,Padre2 = SeleccionPadres(k,Pob,F_obj,Tam_pob,Numclientes)

        #Pase 3: Cruzamiento
        Hijo1,Hijo2 = Cruzamiento(Padre1,Padre2)

        if not np.shape(np.unique(Hijo1))[0]==Numclientes or not np.shape(np.unique(Hijo2))[0]==Numclientes:
            print('Error: cruzamiento')
            print('hijo1:', Hijo1, '---', 'hijo2:', Hijo2)
            #print(Hijo_final,' - ',np.shape(np.unique(Hijo1))[0],' - ', np.shape(np.unique(Hijo2))[0]==Numclientes)
            return 0,0,0

        #Paso 4: Seleccionar el mejor hijo
        F_obj_hijo1 = Funcion_obj(Hijo1,dist)
        F_obj_hijo2 = Funcion_obj(Hijo2,dist)

        if F_obj_hijo1 < F_obj_hijo2: #hijo1 mejor que hijo2
            Hijo = Hijo1
        else: #hijo2 mejor que el hijo1
            Hijo = Hijo2

        #Paso5 : Mutación
        if np.random.rand(1) < Tm:
            #print(Hijo)
            Hijo_final = Mutacion(Hijo)
            
            if not np.shape(np.unique(Hijo_final))[0]==Numclientes:
                print('Error mutacion:')
                print('Hijo_final:', Hijo_final)
                #print(Hijo_final,' - ',np.shape(np.unique(Hijo_final))[0],' - ', np.shape(np.unique(Hijo_final))[0]==Numclientes)
                return 0,0,0
        else:
            Hijo_final = Hijo;
   
        F_obj_hijo_final = Funcion_obj(Hijo_final,dist)

        #Paso 6: Ingreso a la población

        #Verificar si ya existe
        flag = 0
        for i in range(Tam_pob):
            if np.array_equal(Pob[i],Hijo_final):
                flag = 1
                break

        if flag == 0: #Lo puedo ingresar a la población
            #Encontrar individuo que sale
            F_obj_sale = np.max(F_obj)
            Pos_sale = np.argmax(F_obj)
            if F_obj_hijo_final < F_obj_sale: #Puedo ingresarlo a la población
                Pob[Pos_sale]=Hijo_final
                F_obj[Pos_sale] = F_obj_hijo_final
            
            if F_obj_hijo_final<Incumbente:
                Incum_acumulado[Contador_incumbentes,1]=F_obj_hijo_final
                Incum_acumulado[Contador_incumbentes,0]=q
                Contador_incumbentes = Contador_incumbentes + 1
                Incumbente = F_obj_hijo_final
                Sol_Incumbente = Hijo_final
            
        
    #Eliminacion de ceros de Incum_acumulado
    ind=0
    for i in range(np.shape(Incum_acumulado)[0]):
        if Incum_acumulado[i,0] == 0:
            ind = i-1
            break
    Incum_acumulado = Incum_acumulado[0:ind,:]
    

    return Sol_Incumbente,Incumbente,Incum_acumulado
    



