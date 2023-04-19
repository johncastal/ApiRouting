from ruteo.Genetico.Genetico import genetico
from ruteo.VecinoCercano.VecinoCercano import VecinoCercano

class solvers:
    def __init__(self, dist,seed,algoritmo):
        self.dist = dist
        self.seed = seed
        self.algoritmo = algoritmo
    
    def s(self):
        if self.algoritmo == 'Genetic':
            return genetico(self.dist,self.seed)
        elif self.algoritmo == 'VecinoCercano':
            return VecinoCercano(self.dist)
  





