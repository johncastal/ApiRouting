import numpy as np

def get_incum(Sol_Incumbente,grupo_k):
    
    sol_incumbete_real=np.zeros((np.shape(Sol_Incumbente)),dtype=int)
    orden_cuentas = np.zeros((np.shape(Sol_Incumbente)),dtype=int)
    
    for i in Sol_Incumbente:
        sol_incumbete_real[i] = int(grupo_k[Sol_Incumbente[i],4])
        orden_cuentas[i] = int(grupo_k[Sol_Incumbente[i],1])
    
    return sol_incumbete_real,orden_cuentas