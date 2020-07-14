
import numpy as np  # NumPy package for arrays, random number generation, etc
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon # Librería para dibujar poligonos


class AnimacionTrafico(object):

    # Creación de figura a plotear
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    plt.show()

    def __init__(self):
        self.contorno = RegularPolygon((0, 0), numVertices=4, radius=np.sqrt(50**2+50**2), orientation=np.radians(45), facecolor="blue", alpha=0.1,
                         edgecolor='k')
        self.ax.add_patch(self.contorno)  # se dibuja el contorno
        self.ax.scatter(0, 0, c='k', alpha=0.5, marker='1') # Se dibuja un punto negro representando a la estación base

    def dibujar(self):
        plt.show() # Ploteo de figura

    def actualizar(self):
        # Redibuja a manera de animación
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def dibujarDispositivo(self,posicion,color,marker):
        self.ax.scatter(posicion[0], posicion[1], c=color, alpha=1, marker=marker,s=3)

    def dibujarPaquete(self,posicion,estado):
        if(estado==0):
            self.ax.scatter(posicion[0], posicion[1], c='g', alpha=0.5, marker='s', s=5)
        else:
            self.ax.scatter(posicion[0], posicion[1], c='r', alpha=0.5, marker='p', s=5)