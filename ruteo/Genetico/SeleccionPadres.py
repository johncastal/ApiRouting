import numpy as np

def SeleccionPadres(k,Pob,F_obj,Tam_pob,Numclientes):
    #Función para obtener 2 individuos que serán padres en la pob
    #De la población, extraigo k individuos, de estos selecciono los
    #2 mejores y los asigno como padres.


    Indices_Candidatos = np.random.permutation(np.array(range(Tam_pob)))
    Candidatos = np.zeros((Tam_pob,2))
    Candidatos[:,0] = Indices_Candidatos
    Candidatos[:,1] = F_obj[Indices_Candidatos][:,0]

    Muestras = Candidatos[0:k,:]
    Muestras = Muestras[Muestras[:, 1].argsort()] #Se ordena por F_obj

    Padre1 = Pob[int(Muestras[0,0]),:]
    Padre2 = Pob[int(Muestras[1,0]),:]

    if not np.shape(np.unique(Padre1))[0]==Numclientes or not np.shape(np.unique(Padre2))[0]==Numclientes:
        print('error')
    if not np.all(Padre1[1:-1]) or not np.all(Padre2[1:-1]):
        print('Error')

    return Padre1,Padre2