import numpy as np
import time


def Cruzamiento(Padre1,Padre2):

    
    NumClientes = np.shape(Padre1)[0]-1;

    if NumClientes<=2:
        return Padre1,Padre2

    #Generación de cortes aleatorios
    while True:
        Corte_1 = np.random.randint(low=1,high=NumClientes) #entre 1 y NumClientes-1
        Corte_2 = np.random.randint(low=1,high=NumClientes)
        if Corte_1<Corte_2:
            break

    #Creación de hijos en memoria (ceros)
    Hijo1 = np.zeros((NumClientes+1),dtype=int)
    Hijo2 = np.zeros((NumClientes+1),dtype=int)

    #Llenado de exteriores
    Hijo1[0:Corte_1] = Padre1[0:Corte_1] #Izquierda
    Hijo1[Corte_2:-1] = Padre1[Corte_2:-1] #Derecha
    Hijo1_verf = Hijo1.copy()

    Hijo2[0:Corte_1] = Padre2[0:Corte_1] #Izquierda
    Hijo2[Corte_2:-1] = Padre2[Corte_2:-1] #Derecha
    Hijo2_verf = Hijo2.copy()

    #Llenado de hijos
    Posicion_llenado1=Corte_1
    Posicion_llenado2=Corte_1
    for i in range(NumClientes): #Recorre el Padre2
        flag1 = 0 #Bandera que indica que encontro gen de padre2 en hijo1
        flag2 = 0
        for j in range(NumClientes): #j=1:NumClientes #Recorre el hijo1
            if Padre2[i] == Hijo1[j]: #se encontró elemento
                flag1 = 1 #se levanta la bandera
            if Padre1[i] == Hijo2[j]: #se encontró elemento
                flag2 = 1 #se levanta la bandera
            if flag1 == 1 and flag2 == 1:
                break
            
        if flag1 == 0: #Realizo el llenado
            Hijo1[Posicion_llenado1]=Padre2[i]
            Posicion_llenado1 += 1
        if flag2 == 0: #Realizo el llenado
            Hijo2[Posicion_llenado2]=Padre1[i]
            Posicion_llenado2 += 1
   
    
    return Hijo1,Hijo2
        
    