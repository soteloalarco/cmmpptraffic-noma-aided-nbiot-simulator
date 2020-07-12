import numpy as np
import math as mth
import random
import operator
from scipy.stats import expon
from noma.clases.dispositivo import Dispositivo

def creardispositivos(numeroDispositivos, tipo, PLE, radio_celula, numeroSubportadoras, potenciaMaxDispositivos):

    dispositivos = []
    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo

        #Creación de ganancias por cada subportadora
        h = []
        # Usuarios uniformemente distribuidos dentro de la celda entre .1 a 500m
        # Calculo de distancia del UE a la BS
        d = mth.sqrt(np.random.uniform(0, 1) * (radio_celula ** 2))
        ple = PLE

        #subcarriers=np.linspace(2000e6, 2000180000, 48) #48 subportadoras en frecuencia de 2Ghz

        for gain in range(0, numeroSubportadoras):
            #Implementacion de desvanecimiento tipo Rayleigh
            rayleighGain = random.expovariate(1)
            h.append((d ** (-ple)) * rayleighGain)

            #Implementacion Modelo de Canal Rappaport
            #d0 = 1
            #h1 = 32.4 + 10 * ple * mth.log10(d / d0) + 20 * mth.log10(d0) + 20 * mth.log10(subcarriers[numeroSubportadoras]/1e9) + 10 * mth.log10(random.expovariate(1))
            #h2 = 10^(h1/10)
            #h.append(h2)

        h2 = sum(h)

        #Ganancia Promedio
        h_ = h2 / numeroSubportadoras

        #Asignación de potencias para cada subportadora
        Px = []
        for power in range(0, numeroSubportadoras):
            Px.append(potenciaMaxDispositivos)

        #Asignación de umbrales de tasa de transmisión dependiendo el tipo de dispositivo
        if tipo == 1:
            Rth = np.random.uniform(100, 20e3)#Esto es en bits, el de nosotros es 200 bytes ~ 1600bits
        elif tipo == 2:
            Rth = np.random.uniform(100, 2e3)

        #Se crea el dispositivo de acuerdo con las caracteristicas establecidas
        dispositivos.append(Dispositivo(disp, tipo, 0, d, h_, h, 0, 0, Px, Rth))

    # Ordenamiento de dispositivos con base en sus ganancia promedio de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h_'), reverse=True)
    return dispositivosorted

def creardispositivosDES(universoUEs, tipo, PLE, radio_celula, numeroSubportadoras, potenciaMaxDispositivos):

    dispositivos = []
    for disp in range(0,len(universoUEs)):  # Generamos la cantidad indicada de dispositivos de cada tipo

        #Asignación de potencias para cada subportadora
        Px = []
        for power in range(0, numeroSubportadoras):
            Px.append(potenciaMaxDispositivos)

        #Se crea el dispositivo de acuerdo con las caracteristicas establecidas
        dispositivos.append(Dispositivo(universoUEs[disp].get_id(), tipo, 0, universoUEs[disp].get_distancia(), universoUEs[disp].get_h_(), universoUEs[disp].get_h(), 0, 0, Px, universoUEs[disp].get_Rth()))

    # Ordenamiento de dispositivos con base en sus ganancia promedio de canal (descendentemente)
    dispositivosorted = sorted(dispositivos, key=operator.attrgetter('h_'), reverse=True)
    return dispositivosorted
