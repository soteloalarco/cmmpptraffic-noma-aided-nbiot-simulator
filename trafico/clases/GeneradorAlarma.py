import numpy as np  # NumPy package for arrays, random number generation, etc


class GeneradorAlarmas(object):

    # Definición de constructor
    def __init__(self, modelotrafico,lambdaEvento,velocidad,tiempoInicial, modeloEspacial,constanteEspacial1,constanteEspacial2,posicion):
        self.lambdaEvento=lambdaEvento # tasa de generacion de eventos de alarma
        self.velocidad=velocidad #velocidad de propagación de los eventos de alarma
        self.siguienteArribo=tiempoInicial #debe ser inicializado al tiempo inicial de la simulación
        self.modeloEspacial=modeloEspacial # 0 para modelo decaying exponential,  1 para raised-cosine window
        self.constanteEspacial1=constanteEspacial1 # alpha para modelo decaying exponential, W para raised-cosine window
        self.constanteEspacial2=constanteEspacial2 # dth para raised-cosine window, nada para dacaying exponential
        self.posicion = posicion  # la posición espacial dentro de la celula
        self.idAlarma=0
        self.totalAlarmas=[]
        self.modeloTrafico=modelotrafico


    def calcularSiguienteAlarma(self,radio): #Calcular en qué momento sucederá la siguiente alarma
        tiempoEspera = np.random.exponential(1 / (self.lambdaEvento), 1)  # el siguiente arribo se producirá segun una varible exponencial
        self.siguienteArribo=self.siguienteArribo + tiempoEspera
        #Generar posición en un círculo
        theta = 2 * np.pi * np.random.uniform(0, 1, 1);  # componente angular
        rho = radio * np.sqrt(np.random.uniform(0, 1, 1));  # componente radial
        # convertimos coordenadas polares a cartesianas
        xx = rho * np.cos(theta);
        yy = rho * np.sin(theta);
        self.posicion=[xx, yy] # se asigna la posición del evento dentro de la célula
        self.totalAlarmas.append([self.idAlarma,self.siguienteArribo,self.posicion])
        self.idAlarma=self.idAlarma+1

    def generarAlarma(self,tiempoActual,radio): # Función que verifica si ya sucedio la última alarma

        if(self.siguienteArribo <= tiempoActual and self.modeloTrafico==0): # Si ya sucedió la última alarma calcular una nueva, sólo en caso de modelo CMMPP
            self.calcularSiguienteAlarma(radio)
            return True
        else:
            return False


