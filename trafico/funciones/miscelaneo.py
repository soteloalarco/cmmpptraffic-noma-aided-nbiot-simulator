
import numpy as np  # NumPy package for arrays, random number generation

def distanciaList(posicion1,posicion2):
    return np.sqrt(np.sum((np.array(posicion1) - np.array(posicion2)) ** 2))