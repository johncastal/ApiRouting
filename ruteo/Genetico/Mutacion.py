import numpy as np

def Mutacion(Hijo):


    NumClientes = np.shape(Hijo)[0]-1; #eliminando el retorno a sede

    if NumClientes<=2:
        return Hijo

    #Generación de cortes aleatorios
    while True:
        Corte_1 = np.random.randint(low=1,high=NumClientes)
        Corte_2 = np.random.randint(low=1,high=NumClientes)
        if Corte_1<Corte_2:
            break

    Hijo_mutado = Hijo.copy()
    c=0
    for i in range(Corte_1,Corte_2+1): 
        Hijo_mutado[i] = Hijo[Corte_2-c]
        c += 1
    

    return Hijo_mutado
    