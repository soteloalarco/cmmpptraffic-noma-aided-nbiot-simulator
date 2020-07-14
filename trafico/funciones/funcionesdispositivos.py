import numpy as np  # NumPy package for arrays, random number generation, etc
import math as math
from trafico.clases.DeviceMTC import DeviceMTC
from trafico.funciones.miscelaneo import distanciaList

def creardispositivos( modeloTrafico,numeroDispositivos,posiciones, lambdaRegular_Tipo,tipo,tiempo,color,marcador,DispositivosTodos):
    dispositivos = []

    for disp in range(0, numeroDispositivos):  # Generamos la cantidad indicada de dispositivos de cada tipo
        numeroDispositivoTotal = DeviceMTC.totalDispositivos
        DeviceMTC.totalDispositivos = DeviceMTC.totalDispositivos + 1
        DispositivosTodos.append([numeroDispositivoTotal, tipo, posiciones[0][disp], posiciones[1][disp]])
        dispositivos.append(
            DeviceMTC(modeloTrafico,lambdaRegular_Tipo, posiciones[0][disp], posiciones[1][disp], 0,tipo,tiempo,numeroDispositivoTotal,[],0,color,marcador))
    return dispositivos

def funDeltaCustom(x,deltaTiempo):
    if(0<=x<deltaTiempo):
        return 1
    else:
        return 0

def calcularThetak(tiempoActual, tiempoAlarma,distancia,velocidad,deltaTiempo): #Theta_n[k] = theta[k] * delta_n

    aux = (tiempoActual-tiempoAlarma-(distancia/velocidad))
    return funDeltaCustom(aux,deltaTiempo)

def calculardn(distancia,modelo,constanteEspacial1,constanteEspacial2): #Theta_n[k] = theta[k] * delta_n
    if(modelo==0):
        return math.exp(-constanteEspacial1*distancia)
    else:
        return raisedCosineWindow(distancia,constanteEspacial1,constanteEspacial2)


def calcularPnk(tiempoActual,alarmas,velocidad,modelo,constanteEspacial1,constanteEspacial2,Pu,Pc,deltaTiempo): #Proceso maestro
    # alarma=[idAlarma,tiempoAparicion,tiempoLLegada,posicionAlarma,self.posicion]
    Pnk=[] # Pn[k]= Theta_n[k]*Pc + (1-Theta_n[k]*Pu)
    nuevaAlarma=[]  # despues de borrar los eventos que se resuelvan, esta sera la lista a sustituir en el dispositivo
    for alarma in alarmas: # Se verifican todas las alarmas pendientes
        distancia= distanciaList(alarma[3],alarma[4])
        thetak=calcularThetak(tiempoActual,alarma[1],distancia,velocidad,deltaTiempo) #Theta_n[k] = theta[k] * delta_n
        dn= calculardn(distancia,modelo,constanteEspacial1,constanteEspacial2)
        thetank = thetak*dn
        if(thetak==0): # si en esta ventana de tiempo la alarma no llega al dispositivo aun se agrega a la nueva lista
                nuevaAlarma.append(alarma)

        Pnk.append((1 - thetank) * Pu + thetank * Pc)   # Pn[k]= Theta_n[k]*Pc + (1-Theta_n[k]*Pu)

    return [Pnk,nuevaAlarma]

def raisedCosineWindow(dn,W,dth):
    if(dn<dth):
        return 1
    elif(dth<dn<2*W-dth):
        return (1/2)*(1 - math.sin((math.pi*(dn-W))/(2*(W-dth))))
    else:
        return 0
