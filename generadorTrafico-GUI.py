import tkinter as tk
from tkinter import ttk
import pandas as pd
import itertools as iter
from decimal import *
import numpy as np
from trafico.clases.GeneradorAlarma import GeneradorAlarmas
from trafico.funciones.funcionesdispositivos import creardispositivos
from trafico.funciones.funcionesdispositivos import calcularPnk
from trafico.funciones.miscelaneo import distanciaList
from trafico.clases.DeviceMTC import DeviceMTC


class Application(tk.Frame):

    # Variables a modificar
    tiempoLimite = 1  # segundos, tiempo de paro del algoritmo
    deltaTiempo = 0.1  # segundos , diferencial de tiempo entre iteración
    numerosDecimalesDeltaTiempo = 1  # Si se modifica deltaTiempo modificar también esta variable
    tiposDispositivos = 0  # Cantidad total de dispositivos a caracterizar a continuación
    radiocelula=50 # radio de la célula en metros
    modelodispositivos=0 # 0 para PPP y 1 para uniforme
    repeticiones=1 # repeticiones de la rutina CCMMPP


    ### Control de iluminación
    dipositivos_Tipo1 = 0.05  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo1 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo1 = 1 / 40  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 1, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo1 = 1 / 40  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 500 seg)
    velPropagacionAlarma_Tipo1 = 500  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo1 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo1 = 0.007  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo1 = 0  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo1 = 'b'
    marcador_Tipo1 = 'd'

    ### Monitoreo de consumo del agua y electricidad
    dipositivos_Tipo2 = 0.03  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo2 = 1  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo2 = 1 / 15  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 2, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo2 = 1 / 1000  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 200 seg)
    velPropagacionAlarma_Tipo2 = 500  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo2 = 1  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo2 = 200  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo2 = 80  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo2 = 'r'
    marcador_Tipo2 = '*'

    ### Detección de terremotos
    dipositivos_Tipo3 = 0.08 # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo3 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo3 = 1 / 180  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 3, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo3 = 1 / 100  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 350 seg)
    velPropagacionAlarma_Tipo3 = 3000  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo3 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo3 = 0.007  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo3 = 0  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo3 = 'k'
    marcador_Tipo3 = '^'

    ### Contaminación del aire
    dipositivos_Tipo4 = 0.01  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo4 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo4 = 1 / 190  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 4, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo4 = 1 / 100  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 350 seg)
    velPropagacionAlarma_Tipo4 = 1000  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo4 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo4 = 0.005  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo4 = 0  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo4 = 'k'
    marcador_Tipo4 = '^'

    ### Control de semáforos
    dipositivos_Tipo5 = 0.03  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo5 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo5 = 1 / 170  #  si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 5, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo5 = 1 / 200  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 350 seg)
    velPropagacionAlarma_Tipo5 = 2000  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo5 = 1  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo5 = 300  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo5 = 200  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo5 = 'k'
    marcador_Tipo5 = '^'

    ### Otros dispositivos nMTC
    dipositivos_Tipo6 = 0.03  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo6 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo6 = 1 / 170  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 5, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo6 = 1 / 200  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 350 seg)
    velPropagacionAlarma_Tipo6 = 2000  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo6 = 1  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo6 = 300  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo6 = 200  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo6 = 'k'
    marcador_Tipo6 = '^'

    ### Dispositivos URLLC
    dipositivos_Tipo7 = 0.03  # intensidad de dispositivos/m^2, o cantidad total si el modelo de distribución  (modelodispositivos) es uniforme
    modeloTrafico_Tipo7 = 0  # Modelo de generación de tráfico, 0 CMMPP 1 Periódico
    tasaPaquete_Tipo7 = 1 / 170  # si modelotrafico==0 la tasa lambda para el estado regular de los dispositivos de tipo 5, si modelotrafico==1 tasa de Paquete/seg
    lambdaAlarma_Tipo7 = 1 / 200  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 350 seg)
    velPropagacionAlarma_Tipo7 = 2000  # m/s Velocidad de propagación de alarma
    modeloEspacial_Tipo7 = 1  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
    constanteEspacial1_Tipo7 = 300  # alpha para Decaying exponential, W para raised-cosine Window
    constanteEspacial2_Tipo7 = 200  # ignorar para Decaying exponential, dth para raised-cosine Window
    # animacion
    color_Tipo7 = 'k'
    marcador_Tipo7 = '^'

    tasasEventosAlarmas = []
    configSalida = []

    def resetTodo(self): #Cargamos al GUI los valores de la clase Application, los que erán poteriormente leidos para realizar la rutina
        #TODO leer de un archido
        #-----Inicio de Rutina

        self.tiemposimulacion.delete(0,tk.END)
        self.tiemposimulacion.insert(0,str(self.tiempoLimite))
        self.diftiempo.delete(0,tk.END)
        self.diftiempo.insert(0,str(self.deltaTiempo))
        if(self.modelodispositivos==0):
            self.modelodisp00.set('PPP')
        else:
            self.modelodisp00.set('Uniforme')
        self.radio00.delete(0,tk.END)
        self.radio00.insert(0,str(self.radiocelula))
        self.repeticiones00.delete(0,tk.END)
        self.repeticiones00.insert(0,str(self.repeticiones))

        self.cambiomodelodispresettodo()

        #-----Control de iluminación
        # Cantidad de dispositivos
        self.numero01.delete(0,tk.END)
        self.numero01.insert(0,str(self.dipositivos_Tipo1))
        # modelo tráfico
        if (self.modeloTrafico_Tipo1 == 0):
            self.modelotra01.set("CMMPP")
            self.constante10.set('Tasa Promedio')
            self.const001['state'] = 'normal'
            self.constante15.set('Tasa alarma')
            self.tasaalarma01['state'] = 'normal'
            self.constante16.set('Veolcidad alarma')
            self.veloalarma01['state'] = 'normal'
            self.modeloesp01['state'] = 'readonly'
        else:
            self.modelotra01.set("Periódico")
            self.constante10.set('Tasa de paquetes')
            self.const001['state'] = 'normal'
            self.constante15.set('---')
            self.tasaalarma01.delete(0, tk.END)
            self.tasaalarma01['state'] = 'disabled'
            self.constante16.set('---')
            self.veloalarma01.delete(0, tk.END)
            self.veloalarma01['state'] = 'disabled'
            self.constante11.set('')
            self.constante12.set('')
            self.const101.delete(0, tk.END)
            self.const201.delete(0, tk.END)
            self.const101['state'] = 'disabled'
            self.const201['state'] = 'disabled'
            self.modeloesp01.set('Seleccionar modelo')
            self.modeloesp01['state'] = 'disabled'
        # Tasa de paquete
        self.const001.delete(0, tk.END)
        self.const001.insert(0, str(self.tasaPaquete_Tipo1))
        # Tasa de alarma
        self.tasaalarma01.delete(0,tk.END)
        self.tasaalarma01.insert(0,str(self.lambdaAlarma_Tipo1))
        # Velocidad alarma
        self.veloalarma01.delete(0,tk.END)
        self.veloalarma01.insert(0,str(self.velPropagacionAlarma_Tipo1))
        # Propagación espacial
        if(self.modeloEspacial_Tipo1==0 and self.modeloTrafico_Tipo1 == 0):
            self.modeloesp01.set("Decaying Exponential")
            self.constante11.set('Alpha')
            self.constante12.set('----')
            self.const101['state'] = 'normal'
            self.const201.delete(0, tk.END)
            self.const201['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo1==1 and self.modeloTrafico_Tipo1 == 0):
            self.modeloesp01.set("Raised-Cosine Window")
            self.constante11.set('W')
            self.constante12.set('dth')
            self.const101['state'] = 'normal'
            self.const201['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const101.delete(0,tk.END)
        self.const101.insert(0,str(self.constanteEspacial1_Tipo1))
        self.const201.delete(0, tk.END)
        self.const201.insert(0, str(self.constanteEspacial2_Tipo1))

        # -----Consumo de agua y electricidad
        # Cantidad de dispositivos
        self.numero02.delete(0, tk.END)
        self.numero02.insert(0, str(self.dipositivos_Tipo2))
        # modelo tráfico
        if (self.modeloTrafico_Tipo2 == 0):
            self.modelotra02.set("CMMPP")
            self.constante20.set('Tasa Promedio')
            self.const002['state'] = 'normal'
            self.constante25.set('Tasa alarma')
            self.tasaalarma02['state'] = 'normal'
            self.constante26.set('Veolcidad alarma')
            self.veloalarma02['state'] = 'normal'
            self.modeloesp02['state'] = 'readonly'
        else:
            self.modelotra02.set("Periódico")
            self.constante20.set('Tasa de paquetes')
            self.const002['state'] = 'normal'
            self.constante25.set('---')
            self.tasaalarma02.delete(0, tk.END)
            self.tasaalarma02['state'] = 'disabled'
            self.constante26.set('---')
            self.veloalarma02.delete(0, tk.END)
            self.veloalarma02['state'] = 'disabled'
            self.constante21.set('')
            self.constante22.set('')
            self.const102.delete(0, tk.END)
            self.const202.delete(0, tk.END)
            self.const102['state'] = 'disabled'
            self.const202['state'] = 'disabled'
            self.modeloesp02.set('Seleccionar modelo')
            self.modeloesp02['state'] = 'disabled'
        # Tasa de paquete
        self.const002.delete(0, tk.END)
        self.const002.insert(0, str(self.tasaPaquete_Tipo2))
        # Tasa de alarma
        self.tasaalarma02.delete(0, tk.END)
        self.tasaalarma02.insert(0, str(self.lambdaAlarma_Tipo2))
        # Velocidad alarma
        self.veloalarma02.delete(0, tk.END)
        self.veloalarma02.insert(0, str(self.velPropagacionAlarma_Tipo2))
        # Propagación espacial
        if (self.modeloEspacial_Tipo2 == 0 and self.modeloTrafico_Tipo2 == 0):
            self.modeloesp02.set("Decaying Exponential")
            self.constante21.set('Alpha')
            self.constante22.set('----')
            self.const102['state'] = 'normal'
            self.const202.delete(0, tk.END)
            self.const202['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo2 == 1 and self.modeloTrafico_Tipo2 == 0):
            self.modeloesp02.set("Raised-Cosine Window")
            self.constante21.set('W')
            self.constante22.set('dth')
            self.const102['state'] = 'normal'
            self.const202['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const102.delete(0, tk.END)
        self.const102.insert(0, str(self.constanteEspacial1_Tipo2))
        self.const202.delete(0, tk.END)
        self.const202.insert(0, str(self.constanteEspacial2_Tipo2))

        # -----Detección de terremotos
        # Cantidad de dispositivos
        self.numero03.delete(0, tk.END)
        self.numero03.insert(0, str(self.dipositivos_Tipo3))
        # modelo tráfico
        if (self.modeloTrafico_Tipo3 == 0):
            self.modelotra03.set("CMMPP")
            self.constante30.set('Tasa Promedio')
            self.const003['state'] = 'normal'
            self.constante35.set('Tasa alarma')
            self.tasaalarma03['state'] = 'normal'
            self.constante36.set('Velocidad alarma')
            self.veloalarma03['state'] = 'normal'
            self.modeloesp03['state'] = 'readonly'
        else:
            self.modelotra03.set("Periódico")
            self.constante30.set('Tasa de paquetes')
            self.const003['state'] = 'normal'
            self.constante35.set('---')
            self.tasaalarma03.delete(0, tk.END)
            self.tasaalarma03['state'] = 'disabled'
            self.constante36.set('---')
            self.veloalarma03.delete(0, tk.END)
            self.veloalarma03['state'] = 'disabled'
            self.constante31.set('')
            self.constante32.set('')
            self.const103.delete(0, tk.END)
            self.const203.delete(0, tk.END)
            self.const103['state'] = 'disabled'
            self.const203['state'] = 'disabled'
            self.modeloesp03.set('Seleccionar modelo')
            self.modeloesp03['state'] = 'disabled'
        # Tasa de paquete
        self.const003.delete(0, tk.END)
        self.const003.insert(0, str(self.tasaPaquete_Tipo3))
        # Tasa de alarma
        self.tasaalarma03.delete(0, tk.END)
        self.tasaalarma03.insert(0, str(self.lambdaAlarma_Tipo3))
        # Velocidad alarma
        self.veloalarma03.delete(0, tk.END)
        self.veloalarma03.insert(0, str(self.velPropagacionAlarma_Tipo3))
        # Propagación espacial
        if (self.modeloEspacial_Tipo3 == 0 and self.modeloTrafico_Tipo3 == 0):
            self.modeloesp03.set("Decaying Exponential")
            self.constante31.set('Alpha')
            self.constante32.set('----')
            self.const103['state'] = 'normal'
            self.const203.delete(0, tk.END)
            self.const203['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo3 == 1 and self.modeloTrafico_Tipo3 == 0):
            self.modeloesp03.set("Raised-Cosine Window")
            self.constante31.set('W')
            self.constante32.set('dth')
            self.const103['state'] = 'normal'
            self.const203['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const103.delete(0, tk.END)
        self.const103.insert(0, str(self.constanteEspacial1_Tipo3))
        self.const203.delete(0, tk.END)
        self.const203.insert(0, str(self.constanteEspacial2_Tipo3))

        # -----Contaminacion del aire
        # Cantidad de dispositivos
        self.numero10.delete(0, tk.END)
        self.numero10.insert(0, str(self.dipositivos_Tipo4))
        # modelo tráfico
        if (self.modeloTrafico_Tipo4 == 0):
            self.modelotra10.set("CMMPP")
            self.constante40.set('Tasa Promedio')
            self.const010['state'] = 'normal'
            self.constante45.set('Tasa alarma')
            self.tasaalarma10['state'] = 'normal'
            self.constante46.set('Velocidad alarma')
            self.veloalarma10['state'] = 'normal'
            self.modeloesp10['state'] = 'readonly'
        else:
            self.modelotra10.set("Periódico")
            self.constante40.set('Tasa de paquetes')
            self.const010['state'] = 'normal'
            self.constante45.set('---')
            self.tasaalarma10.delete(0, tk.END)
            self.tasaalarma10['state'] = 'disabled'
            self.constante46.set('---')
            self.veloalarma10.delete(0, tk.END)
            self.veloalarma10['state'] = 'disabled'
            self.constante41.set('')
            self.constante42.set('')
            self.const110.delete(0, tk.END)
            self.const210.delete(0, tk.END)
            self.const110['state'] = 'disabled'
            self.const210['state'] = 'disabled'
            self.modeloesp10.set('Seleccionar modelo')
            self.modeloesp10['state'] = 'disabled'
        # Tasa de paquete
        self.const010.delete(0, tk.END)
        self.const010.insert(0, str(self.tasaPaquete_Tipo4))
        # Tasa de alarma
        self.tasaalarma10.delete(0, tk.END)
        self.tasaalarma10.insert(0, str(self.lambdaAlarma_Tipo4))
        # Velocidad alarma
        self.veloalarma10.delete(0, tk.END)
        self.veloalarma10.insert(0, str(self.velPropagacionAlarma_Tipo4))
        # Propagación espacial
        if (self.modeloEspacial_Tipo4 == 0 and self.modeloTrafico_Tipo4 == 0):
            self.modeloesp10.set("Decaying Exponential")
            self.constante41.set('Alpha')
            self.constante42.set('----')
            self.const110['state'] = 'normal'
            self.const210.delete(0, tk.END)
            self.const210['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo4 == 1 and self.modeloTrafico_Tipo4 == 0):
            self.modeloesp10.set("Raised-Cosine Window")
            self.constante41.set('W')
            self.constante42.set('dth')
            self.const110['state'] = 'normal'
            self.const210['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const110.delete(0, tk.END)
        self.const110.insert(0, str(self.constanteEspacial1_Tipo4))
        self.const210.delete(0, tk.END)
        self.const210.insert(0, str(self.constanteEspacial2_Tipo4))

        # -----Control de semáforos
        # Cantidad de dispositivos
        self.numero11.delete(0, tk.END)
        self.numero11.insert(0, str(self.dipositivos_Tipo5))
        # modelo tráfico
        if (self.modeloTrafico_Tipo5 == 0):
            self.modelotra11.set("CMMPP")
            self.constante50.set('Tasa Promedio')
            self.const011['state'] = 'normal'
            self.constante55.set('Tasa alarma')
            self.tasaalarma11['state'] = 'normal'
            self.constante56.set('Velocidad alarma')
            self.veloalarma11['state'] = 'normal'
            self.modeloesp11['state'] = 'readonly'
        else:
            self.modelotra11.set("Periódico")
            self.constante50.set('Tasa de paquetes')
            self.const011['state'] = 'normal'
            self.constante55.set('---')
            self.tasaalarma11.delete(0, tk.END)
            self.tasaalarma11['state'] = 'disabled'
            self.constante56.set('---')
            self.veloalarma11.delete(0, tk.END)
            self.veloalarma11['state'] = 'disabled'
            self.constante51.set('')
            self.constante52.set('')
            self.const111.delete(0, tk.END)
            self.const211.delete(0, tk.END)
            self.const111['state'] = 'disabled'
            self.const211['state'] = 'disabled'
            self.modeloesp11.set('Seleccionar modelo')
            self.modeloesp11['state'] = 'disabled'
        # Tasa de paquete
        self.const011.delete(0, tk.END)
        self.const011.insert(0, str(self.tasaPaquete_Tipo5))
        # Tasa de alarma
        self.tasaalarma11.delete(0, tk.END)
        self.tasaalarma11.insert(0, str(self.lambdaAlarma_Tipo5))
        # Velocidad alarma
        self.veloalarma11.delete(0, tk.END)
        self.veloalarma11.insert(0, str(self.velPropagacionAlarma_Tipo5))
        # Propagación espacial
        if (self.modeloEspacial_Tipo5 == 0 and self.modeloTrafico_Tipo5 == 0):
            self.modeloesp11.set("Decaying Exponential")
            self.constante51.set('Alpha')
            self.constante52.set('----')
            self.const111['state'] = 'normal'
            self.const211.delete(0, tk.END)
            self.const211['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo5 == 1 and self.modeloTrafico_Tipo5 == 0):
            self.modeloesp11.set("Raised-Cosine Window")
            self.constante51.set('W')
            self.constante52.set('dth')
            self.const111['state'] = 'normal'
            self.const211['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const111.delete(0, tk.END)
        self.const111.insert(0, str(self.constanteEspacial1_Tipo5))
        self.const211.delete(0, tk.END)
        self.const211.insert(0, str(self.constanteEspacial2_Tipo5))

        # -----Otros dispositivos mMTC
        # Cantidad de dispositivos
        self.numero12.delete(0, tk.END)
        self.numero12.insert(0, str(self.dipositivos_Tipo6))
        # modelo tráfico
        if (self.modeloTrafico_Tipo6 == 0):
            self.modelotra12.set("CMMPP")
            self.constante60.set('Tasa Promedio')
            self.const012['state'] = 'normal'
            self.constante65.set('Tasa alarma')
            self.tasaalarma12['state'] = 'normal'
            self.constante66.set('Velocidad alarma')
            self.veloalarma12['state'] = 'normal'
            self.modeloesp12['state'] = 'readonly'
        else:
            self.modelotra12.set("Periódico")
            self.constante60.set('Tasa de paquetes')
            self.const012['state'] = 'normal'
            self.constante65.set('---')
            self.tasaalarma12.delete(0, tk.END)
            self.tasaalarma12['state'] = 'disabled'
            self.constante66.set('---')
            self.veloalarma12.delete(0, tk.END)
            self.veloalarma12['state'] = 'disabled'
            self.constante61.set('')
            self.constante62.set('')
            self.const112.delete(0, tk.END)
            self.const212.delete(0, tk.END)
            self.const112['state'] = 'disabled'
            self.const212['state'] = 'disabled'
            self.modeloesp12.set('Seleccionar modelo')
            self.modeloesp12['state'] = 'disabled'
        # Tasa de paquete
        self.const012.delete(0, tk.END)
        self.const012.insert(0, str(self.tasaPaquete_Tipo6))
        # Tasa de alarma
        self.tasaalarma12.delete(0, tk.END)
        self.tasaalarma12.insert(0, str(self.lambdaAlarma_Tipo6))
        # Velocidad alarma
        self.veloalarma12.delete(0, tk.END)
        self.veloalarma12.insert(0, str(self.velPropagacionAlarma_Tipo6))
        # Propagación espacial
        if (self.modeloEspacial_Tipo6 == 0 and self.modeloTrafico_Tipo6 == 0):
            self.modeloesp12.set("Decaying Exponential")
            self.constante61.set('Alpha')
            self.constante62.set('----')
            self.const112['state'] = 'normal'
            self.const212.delete(0, tk.END)
            self.const212['state'] = 'disabled'
        elif (self.modeloEspacial_Tipo6 == 1 and self.modeloTrafico_Tipo6 == 0):
            self.modeloesp12.set("Raised-Cosine Window")
            self.constante61.set('W')
            self.constante62.set('dth')
            self.const112['state'] = 'normal'
            self.const212['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const112.delete(0, tk.END)
        self.const112.insert(0, str(self.constanteEspacial1_Tipo6))
        self.const212.delete(0, tk.END)
        self.const212.insert(0, str(self.constanteEspacial2_Tipo6))

        # -----Dispositivos URLLC
        # Cantidad de dispositivos
        self.numero13.delete(0, tk.END)
        self.numero13.insert(0, str(self.dipositivos_Tipo7))
        # modelo tráfico
        if (self.modeloTrafico_Tipo7 == 0):
            self.modelotra13.set("CMMPP")
            self.constante70.set('Tasa Promedio')
            self.const013['state'] = 'normal'
            self.constante75.set('Tasa alarma')
            self.tasaalarma13['state'] = 'normal'
            self.constante76.set('Velocidad alarma')
            self.veloalarma13['state'] = 'normal'
            self.modeloesp13['state'] = 'readonly'
        else:
            self.modelotra13.set("Periódico")
            self.constante70.set('Tasa de paquetes')
            self.const013['state'] = 'normal'
            self.constante75.set('---')
            self.tasaalarma13.delete(0, tk.END)
            self.tasaalarma13['state'] = 'disabled'
            self.constante76.set('---')
            self.veloalarma13.delete(0, tk.END)
            self.veloalarma13['state'] = 'disabled'
            self.constante71.set('')
            self.constante72.set('')
            self.const113.delete(0, tk.END)
            self.const213.delete(0, tk.END)
            self.const113['state'] = 'disabled'
            self.const213['state'] = 'disabled'
            self.modeloesp13.set('Seleccionar modelo')
            self.modeloesp13['state'] = 'disabled'
        # Tasa de paquete
        self.const013.delete(0, tk.END)
        self.const013.insert(0, str(self.tasaPaquete_Tipo7))
        # Tasa de alarma
        self.tasaalarma13.delete(0, tk.END)
        self.tasaalarma13.insert(0, str(self.lambdaAlarma_Tipo7))
        # Velocidad alarma
        self.veloalarma13.delete(0, tk.END)
        self.veloalarma13.insert(0, str(self.velPropagacionAlarma_Tipo7))
        # Propagación espacial
        if (self.modeloEspacial_Tipo7 == 0 and self.modeloTrafico_Tipo7 == 0):
            self.modeloesp13.set("Decaying Exponential")
            self.constante71.set('Alpha')
            self.constante72.set('----')
            self.const113['state'] = 'normal'
            self.const213.delete(0, tk.END)
            self.const213['state'] = 'disabled'
        elif (self.modeloEspacial_Tipo7 == 1 and self.modeloTrafico_Tipo7 == 0):
            self.modeloesp13.set("Raised-Cosine Window")
            self.constante71.set('W')
            self.constante72.set('dth')
            self.const113['state'] = 'normal'
            self.const213['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const113.delete(0, tk.END)
        self.const113.insert(0, str(self.constanteEspacial1_Tipo7))
        self.const213.delete(0, tk.END)
        self.const213.insert(0, str(self.constanteEspacial2_Tipo7))

    def reset1(self): # Función para resetear valores del frame Control de Iluminación
        # -----Control de iluminación
        # Cantidad de dispositivos
        self.numero01.delete(0, tk.END)
        self.numero01.insert(0, str(self.dipositivos_Tipo1))
        # modelo tráfico
        if (self.modeloTrafico_Tipo1 == 0):
            self.modelotra01.set("CMMPP")
            self.constante10.set('Tasa Promedio')
            self.const001['state'] = 'normal'
            self.constante15.set('Tasa alarma')
            self.tasaalarma01['state'] = 'normal'
            self.constante16.set('Velocidad alarma')
            self.veloalarma01['state'] = 'normal'
            self.modeloesp01['state'] = 'readonly'
        else:
            self.modelotra01.set("Periódico")
            self.constante10.set('Tasa de paquetes')
            self.const001['state'] = 'normal'
            self.constante15.set('---')
            self.tasaalarma01.delete(0, tk.END)
            self.tasaalarma01['state'] = 'disabled'
            self.constante16.set('---')
            self.veloalarma01.delete(0, tk.END)
            self.veloalarma01['state'] = 'disabled'
            self.constante11.set('')
            self.constante12.set('')
            self.const101.delete(0, tk.END)
            self.const201.delete(0, tk.END)
            self.const101['state'] = 'disabled'
            self.const201['state'] = 'disabled'
            self.modeloesp01.set('Seleccionar modelo')
            self.modeloesp01['state'] = 'disabled'
        # Tasa de paquete
        self.const001.delete(0, tk.END)
        self.const001.insert(0, str(self.tasaPaquete_Tipo1))
        # Tasa de alarma
        self.tasaalarma01.delete(0, tk.END)
        self.tasaalarma01.insert(0, str(self.lambdaAlarma_Tipo1))
        # Velocidad alarma
        self.veloalarma01.delete(0, tk.END)
        self.veloalarma01.insert(0, str(self.velPropagacionAlarma_Tipo1))
        # Propagación espacial
        if (self.modeloEspacial_Tipo1 == 0 and self.modeloTrafico_Tipo1 == 0):
            self.modeloesp01.set("Decaying Exponential")
            self.constante11.set('Alpha')
            self.constante12.set('----')
            self.const101['state'] = 'normal'
            self.const201.delete(0, tk.END)
            self.const201['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo1 == 1 and self.modeloTrafico_Tipo1 == 0):
            self.modeloesp01.set("Raised-Cosine Window")
            self.constante11.set('W')
            self.constante12.set('dth')
            self.const101['state'] = 'normal'
            self.const201['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const101.delete(0, tk.END)
        self.const101.insert(0, str(self.constanteEspacial1_Tipo1))
        self.const201.delete(0, tk.END)
        self.const201.insert(0, str(self.constanteEspacial2_Tipo1))

    def reset2(self):
        # -----Consumo de agua y electricidad
        # Cantidad de dispositivos
        self.numero02.delete(0, tk.END)
        self.numero02.insert(0, str(self.dipositivos_Tipo2))
        # modelo tráfico
        if (self.modeloTrafico_Tipo2 == 0):
            self.modelotra02.set("CMMPP")
            self.constante20.set('Tasa Promedio')
            self.const002['state'] = 'normal'
            self.constante25.set('Tasa alarma')
            self.tasaalarma02['state'] = 'normal'
            self.constante26.set('Velocidad alarma')
            self.veloalarma02['state'] = 'normal'
            self.modeloesp02['state'] = 'readonly'
        else:
            self.modelotra02.set("Periódico")
            self.constante20.set('Tasa de paquetes')
            self.const002['state'] = 'normal'
            self.constante25.set('---')
            self.tasaalarma02.delete(0, tk.END)
            self.tasaalarma02['state'] = 'disabled'
            self.constante26.set('---')
            self.veloalarma02.delete(0, tk.END)
            self.veloalarma02['state'] = 'disabled'
            self.constante21.set('')
            self.constante22.set('')
            self.const102.delete(0, tk.END)
            self.const202.delete(0, tk.END)
            self.const102['state'] = 'disabled'
            self.const202['state'] = 'disabled'
            self.modeloesp02.set('Seleccionar modelo')
            self.modeloesp02['state'] = 'disabled'
        # Tasa de paquete
        self.const002.delete(0, tk.END)
        self.const002.insert(0, str(self.tasaPaquete_Tipo2))
        # Tasa de alarma
        self.tasaalarma02.delete(0, tk.END)
        self.tasaalarma02.insert(0, str(self.lambdaAlarma_Tipo2))
        # Velocidad alarma
        self.veloalarma02.delete(0, tk.END)
        self.veloalarma02.insert(0, str(self.velPropagacionAlarma_Tipo2))
        # Propagación espacial
        if (self.modeloEspacial_Tipo2 == 0 and self.modeloTrafico_Tipo2 == 0):
            self.modeloesp02.set("Decaying Exponential")
            self.constante21.set('Alpha')
            self.constante22.set('----')
            self.const102['state'] = 'normal'
            self.const202.delete(0, tk.END)
            self.const202['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo2 == 1 and self.modeloTrafico_Tipo2 == 0):
            self.modeloesp02.set("Raised-Cosine Window")
            self.constante21.set('W')
            self.constante22.set('dth')
            self.const102['state'] = 'normal'
            self.const202['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const102.delete(0, tk.END)
        self.const102.insert(0, str(self.constanteEspacial1_Tipo2))
        self.const202.delete(0, tk.END)
        self.const202.insert(0, str(self.constanteEspacial2_Tipo2))

    def reset3(self):
        # -----Detección de terremotos
        # Cantidad de dispositivos
        self.numero03.delete(0, tk.END)
        self.numero03.insert(0, str(self.dipositivos_Tipo3))
        # modelo tráfico
        if (self.modeloTrafico_Tipo3 == 0):
            self.modelotra03.set("CMMPP")
            self.constante30.set('Tasa Promedio')
            self.const003['state'] = 'normal'
            self.constante35.set('Tasa alarma')
            self.tasaalarma03['state'] = 'normal'
            self.constante36.set('Velocidad alarma')
            self.veloalarma03['state'] = 'normal'
            self.modeloesp03['state'] = 'readonly'
        else:
            self.modelotra03.set("Periódico")
            self.constante30.set('Tasa de paquetes')
            self.const003['state'] = 'normal'
            self.constante35.set('---')
            self.tasaalarma03.delete(0, tk.END)
            self.tasaalarma03['state'] = 'disabled'
            self.constante36.set('---')
            self.veloalarma03.delete(0, tk.END)
            self.veloalarma03['state'] = 'disabled'
            self.constante31.set('')
            self.constante32.set('')
            self.const103.delete(0, tk.END)
            self.const203.delete(0, tk.END)
            self.const103['state'] = 'disabled'
            self.const203['state'] = 'disabled'
            self.modeloesp03.set('Seleccionar modelo')
            self.modeloesp03['state'] = 'disabled'
        # Tasa de paquete
        self.const003.delete(0, tk.END)
        self.const003.insert(0, str(self.tasaPaquete_Tipo3))
        # Tasa de alarma
        self.tasaalarma03.delete(0, tk.END)
        self.tasaalarma03.insert(0, str(self.lambdaAlarma_Tipo3))
        # Velocidad alarma
        self.veloalarma03.delete(0, tk.END)
        self.veloalarma03.insert(0, str(self.velPropagacionAlarma_Tipo3))
        # Propagación espacial
        if (self.modeloEspacial_Tipo3 == 0 and self.modeloTrafico_Tipo3 == 0):
            self.modeloesp03.set("Decaying Exponential")
            self.constante31.set('Alpha')
            self.constante32.set('----')
            self.const103['state'] = 'normal'
            self.const203.delete(0, tk.END)
            self.const203['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo3 == 1 and self.modeloTrafico_Tipo3 == 0):
            self.modeloesp03.set("Raised-Cosine Window")
            self.constante31.set('W')
            self.constante32.set('dth')
            self.const103['state'] = 'normal'
            self.const203['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const103.delete(0, tk.END)
        self.const103.insert(0, str(self.constanteEspacial1_Tipo3))
        self.const203.delete(0, tk.END)
        self.const203.insert(0, str(self.constanteEspacial2_Tipo3))

    def reset4(self):
        # -----Contaminacion del aire
        # Cantidad de dispositivos
        self.numero10.delete(0, tk.END)
        self.numero10.insert(0, str(self.dipositivos_Tipo4))
        # modelo tráfico
        if (self.modeloTrafico_Tipo4 == 0):
            self.modelotra10.set("CMMPP")
            self.constante40.set('Tasa Promedio')
            self.const010['state'] = 'normal'
            self.constante45.set('Tasa alarma')
            self.tasaalarma10['state'] = 'normal'
            self.constante46.set('Velocidad alarma')
            self.veloalarma10['state'] = 'normal'
            self.modeloesp10['state'] = 'readonly'
        else:
            self.modelotra10.set("Periódico")
            self.constante40.set('Tasa de paquetes')
            self.const010['state'] = 'normal'
            self.constante45.set('---')
            self.tasaalarma10.delete(0, tk.END)
            self.tasaalarma10['state'] = 'disabled'
            self.constante46.set('---')
            self.veloalarma10.delete(0, tk.END)
            self.veloalarma10['state'] = 'disabled'
            self.constante41.set('')
            self.constante42.set('')
            self.const110.delete(0, tk.END)
            self.const210.delete(0, tk.END)
            self.const110['state'] = 'disabled'
            self.const210['state'] = 'disabled'
            self.modeloesp10.set('Seleccionar modelo')
            self.modeloesp10['state'] = 'disabled'
        # Tasa de paquete
        self.const010.delete(0, tk.END)
        self.const010.insert(0, str(self.tasaPaquete_Tipo4))
        # Tasa de alarma
        self.tasaalarma10.delete(0, tk.END)
        self.tasaalarma10.insert(0, str(self.lambdaAlarma_Tipo4))
        # Velocidad alarma
        self.veloalarma10.delete(0, tk.END)
        self.veloalarma10.insert(0, str(self.velPropagacionAlarma_Tipo4))
        # Propagación espacial
        if (self.modeloEspacial_Tipo4 == 0 and self.modeloTrafico_Tipo4 == 0):
            self.modeloesp10.set("Decaying Exponential")
            self.constante41.set('Alpha')
            self.constante42.set('----')
            self.const110['state'] = 'normal'
            self.const210.delete(0, tk.END)
            self.const210['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo4 == 1 and self.modeloTrafico_Tipo4 == 0):
            self.modeloesp10.set("Raised-Cosine Window")
            self.constante41.set('W')
            self.constante42.set('dth')
            self.const110['state'] = 'normal'
            self.const210['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const110.delete(0, tk.END)
        self.const110.insert(0, str(self.constanteEspacial1_Tipo4))
        self.const210.delete(0, tk.END)
        self.const210.insert(0, str(self.constanteEspacial2_Tipo4))

    def reset5(self):
        # -----Control de semáforos
        # Cantidad de dispositivos
        self.numero11.delete(0, tk.END)
        self.numero11.insert(0, str(self.dipositivos_Tipo5))
        # modelo tráfico
        if (self.modeloTrafico_Tipo5 == 0):
            self.modelotra11.set("CMMPP")
            self.constante50.set('Tasa Promedio')
            self.const011['state'] = 'normal'
            self.constante55.set('Tasa alarma')
            self.tasaalarma11['state'] = 'normal'
            self.constante56.set('Velocidad alarma')
            self.veloalarma11['state'] = 'normal'
            self.modeloesp11['state'] = 'readonly'
        else:
            self.modelotra11.set("Periódico")
            self.constante50.set('Tasa de paquetes')
            self.const011['state'] = 'normal'
            self.constante55.set('---')
            self.tasaalarma11.delete(0, tk.END)
            self.tasaalarma11['state'] = 'disabled'
            self.constante56.set('---')
            self.veloalarma11.delete(0, tk.END)
            self.veloalarma11['state'] = 'disabled'
            self.constante51.set('')
            self.constante52.set('')
            self.const111.delete(0, tk.END)
            self.const211.delete(0, tk.END)
            self.const111['state'] = 'disabled'
            self.const211['state'] = 'disabled'
            self.modeloesp11.set('Seleccionar modelo')
            self.modeloesp11['state'] = 'disabled'
        # Tasa de paquete
        self.const011.delete(0, tk.END)
        self.const011.insert(0, str(self.tasaPaquete_Tipo5))
        # Tasa de alarma
        self.tasaalarma11.delete(0, tk.END)
        self.tasaalarma11.insert(0, str(self.lambdaAlarma_Tipo5))
        # Velocidad alarma
        self.veloalarma11.delete(0, tk.END)
        self.veloalarma11.insert(0, str(self.velPropagacionAlarma_Tipo5))
        # Propagación espacial
        if (self.modeloEspacial_Tipo5 == 0 and self.modeloTrafico_Tipo5 == 0):
            self.modeloesp11.set("Decaying Exponential")
            self.constante51.set('Alpha')
            self.constante52.set('----')
            self.const111['state'] = 'normal'
            self.const211['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo5 == 1 and self.modeloTrafico_Tipo5 == 0):
            self.modeloesp11.set("Raised-Cosine Window")
            self.constante51.set('W')
            self.constante52.set('dth')
            self.const111['state'] = 'normal'
            self.const211.delete(0, tk.END)
            self.const211['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const111.delete(0, tk.END)
        self.const111.insert(0, str(self.constanteEspacial1_Tipo5))
        self.const211.delete(0, tk.END)
        self.const211.insert(0, str(self.constanteEspacial2_Tipo5))

    def reset6(self):
        # -----Control de semáforos
        # Cantidad de dispositivos
        self.numero12.delete(0, tk.END)
        self.numero12.insert(0, str(self.dipositivos_Tipo6))
        # modelo tráfico
        if (self.modeloTrafico_Tipo6 == 0):
            self.modelotra12.set("CMMPP")
            self.constante60.set('Tasa Promedio')
            self.const012['state'] = 'normal'
            self.constante65.set('Tasa alarma')
            self.tasaalarma12['state'] = 'normal'
            self.constante66.set('Velocidad alarma')
            self.veloalarma12['state'] = 'normal'
            self.modeloesp12['state'] = 'readonly'
        else:
            self.modelotra12.set("Periódico")
            self.constante60.set('Tasa de paquetes')
            self.const012['state'] = 'normal'
            self.constante65.set('---')
            self.tasaalarma12.delete(0, tk.END)
            self.tasaalarma12['state'] = 'disabled'
            self.constante66.set('---')
            self.veloalarma12.delete(0, tk.END)
            self.veloalarma12['state'] = 'disabled'
            self.constante61.set('')
            self.constante62.set('')
            self.const112.delete(0, tk.END)
            self.const212.delete(0, tk.END)
            self.const112['state'] = 'disabled'
            self.const212['state'] = 'disabled'
            self.modeloesp12.set('Seleccionar modelo')
            self.modeloesp12['state'] = 'disabled'
        # Tasa de paquete
        self.const012.delete(0, tk.END)
        self.const012.insert(0, str(self.tasaPaquete_Tipo6))
        # Tasa de alarma
        self.tasaalarma12.delete(0, tk.END)
        self.tasaalarma12.insert(0, str(self.lambdaAlarma_Tipo6))
        # Velocidad alarma
        self.veloalarma12.delete(0, tk.END)
        self.veloalarma12.insert(0, str(self.velPropagacionAlarma_Tipo6))
        # Propagación espacial
        if (self.modeloEspacial_Tipo6 == 0 and self.modeloTrafico_Tipo6 == 0):
            self.modeloesp12.set("Decaying Exponential")
            self.constante61.set('Alpha')
            self.constante62.set('----')
            self.const112['state'] = 'normal'
            self.const212['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo6 == 1 and self.modeloTrafico_Tipo6 == 0):
            self.modeloesp12.set("Raised-Cosine Window")
            self.constante61.set('W')
            self.constante62.set('dth')
            self.const112['state'] = 'normal'
            self.const212.delete(0, tk.END)
            self.const212['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const112.delete(0, tk.END)
        self.const112.insert(0, str(self.constanteEspacial1_Tipo6))
        self.const212.delete(0, tk.END)
        self.const212.insert(0, str(self.constanteEspacial2_Tipo6))

    def reset7(self):
        # -----Control de semáforos
        # Cantidad de dispositivos
        self.numero13.delete(0, tk.END)
        self.numero13.insert(0, str(self.dipositivos_Tipo7))
        # modelo tráfico
        if (self.modeloTrafico_Tipo7 == 0):
            self.modelotra13.set("CMMPP")
            self.constante70.set('Tasa Promedio')
            self.const013['state'] = 'normal'
            self.constante75.set('Tasa alarma')
            self.tasaalarma13['state'] = 'normal'
            self.constante76.set('Velocidad alarma')
            self.veloalarma13['state'] = 'normal'
            self.modeloesp13['state'] = 'readonly'
        else:
            self.modelotra13.set("Periódico")
            self.constante70.set('Tasa de paquetes')
            self.const013['state'] = 'normal'
            self.constante75.set('---')
            self.tasaalarma13.delete(0, tk.END)
            self.tasaalarma13['state'] = 'disabled'
            self.constante76.set('---')
            self.veloalarma13.delete(0, tk.END)
            self.veloalarma13['state'] = 'disabled'
            self.constante71.set('')
            self.constante72.set('')
            self.const113.delete(0, tk.END)
            self.const213.delete(0, tk.END)
            self.const113['state'] = 'disabled'
            self.const213['state'] = 'disabled'
            self.modeloesp13.set('Seleccionar modelo')
            self.modeloesp13['state'] = 'disabled'
        # Tasa de paquete
        self.const013.delete(0, tk.END)
        self.const013.insert(0, str(self.tasaPaquete_Tipo7))
        # Tasa de alarma
        self.tasaalarma13.delete(0, tk.END)
        self.tasaalarma13.insert(0, str(self.lambdaAlarma_Tipo7))
        # Velocidad alarma
        self.veloalarma13.delete(0, tk.END)
        self.veloalarma13.insert(0, str(self.velPropagacionAlarma_Tipo7))
        # Propagación espacial
        if (self.modeloEspacial_Tipo7 == 0 and self.modeloTrafico_Tipo7 == 0):
            self.modeloesp13.set("Decaying Exponential")
            self.constante71.set('Alpha')
            self.constante73.set('----')
            self.const113['state'] = 'normal'
            self.const213['state'] = 'disabled'
        elif(self.modeloEspacial_Tipo7 == 1 and self.modeloTrafico_Tipo7 == 0):
            self.modeloesp13.set("Raised-Cosine Window")
            self.constante71.set('W')
            self.constante73.set('dth')
            self.const113['state'] = 'normal'
            self.const213.delete(0, tk.END)
            self.const213['state'] = 'normal'
        # Constantes de propagación espacial alpha,W,dth
        self.const113.delete(0, tk.END)
        self.const113.insert(0, str(self.constanteEspacial1_Tipo7))
        self.const213.delete(0, tk.END)
        self.const213.insert(0, str(self.constanteEspacial2_Tipo7))

    def leerentradas(self):
        # Variables a modificar
        self.tiempoLimite = float(self.tiemposimulacion.get())  # segundos, tiempo de paro del algoritmo
        self.deltaTiempo = float(self.diftiempo.get())  # segundos , diferencial de tiempo entre iteración
        decimales=Decimal(self.diftiempo.get())
        self.numerosDecimalesDeltaTiempo = -1*(int(decimales.as_tuple().exponent))  # Si se modifica deltaTiempo modificar también esta veriable
        self.radiocelula=float(self.radio00.get())
        if (self.modelodisp00.get() == 'PPP'):
            self.modelodispositivos=0
        else:
            self.modelodispositivos = 1
        self.repeticiones=int(self.repeticiones00.get())

        ### Control de iluminación
        if (self.numero01.get() == ''):
            self.dipositivos_Tipo1 = 0
        else:
            self.dipositivos_Tipo1 = float(self.numero01.get())  # número de dispositivos de tipo 1,
        if (self.modelotra01.get() == 'CMMPP'):
            self.modeloTrafico_Tipo1 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo1 = 1
        self.tasaPaquete_Tipo1 = float(self.const001.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 1 (1 paquete cada 60 seg)
        if(self.tasaalarma01.get()==''):
            self.lambdaAlarma_Tipo1=0
        else:
            self.lambdaAlarma_Tipo1 = float(self.tasaalarma01.get())  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 500 seg)
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo1, self.lambdaAlarma_Tipo1])
        if(self.veloalarma01.get()==''):
            self.velPropagacionAlarma_Tipo1 =0
        else:
            self.velPropagacionAlarma_Tipo1 = float(self.veloalarma01.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp01.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo1 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo1 = 1
        if (self.const101.get() == ''):
            self.constanteEspacial1_Tipo1 = 0
        else:
            self.constanteEspacial1_Tipo1 = float(self.const101.get())  # alpha para Decaying exponential, W para raised-cosine Window

        if (self.modeloesp01.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo1 = float(self.const201.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo1 = 'b'
        self.marcador_Tipo1 = 'd'

        ### Monitoreo de consumo del agua y electricidad
        if (self.numero02.get() == ''):
            self.dipositivos_Tipo2 = 0
        else:
            self.dipositivos_Tipo2 = float(self.numero02.get())  # número de dispositivos de tipo 2
        if (self.modelotra02.get() == 'CMMPP'):
            self.modeloTrafico_Tipo2 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo2 = 1
        self.tasaPaquete_Tipo2 = float(self.const002.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)

        if (self.tasaalarma02.get() == ''):
            self.lambdaAlarma_Tipo2 = 0
        else:
            self.lambdaAlarma_Tipo2 = float(
                self.tasaalarma02.get())  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 500 seg)
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo2, self.lambdaAlarma_Tipo2])
        if (self.veloalarma02.get() == ''):
            self.velPropagacionAlarma_Tipo2 = 0
        else:
            self.velPropagacionAlarma_Tipo2 = float(self.veloalarma02.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp02.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo2 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo2 = 1

        if (self.const102.get() == ''):
            self.constanteEspacial1_Tipo2 = 0
        else:
            self.constanteEspacial1_Tipo2 = float(self.const102.get())  # alpha para Decaying exponential, W para raised-cosine Window

        if (self.modeloesp02.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo2 = float(self.const202.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo2 = 'r'
        self.marcador_Tipo2 = '*'

        ### Detección de terremotos
        if (self.numero03.get() == ''):
            self.dipositivos_Tipo3 = 0
        else:
            self.dipositivos_Tipo3 = float(self.numero03.get())  # número de dispositivos de tipo 3
        if (self.modelotra03.get() == 'CMMPP'):
            self.modeloTrafico_Tipo3 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo3 = 1
        self.tasaPaquete_Tipo3 = float(self.const003.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)

        if (self.tasaalarma03.get() == ''):
            self.lambdaAlarma_Tipo3 = 0
        else:
            self.lambdaAlarma_Tipo3 = float(
                self.tasaalarma03.get())  # la tasa a la que se producen eventos de alarma para este tipo de dispositivos (1 evento cada 500 seg)
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo3, self.lambdaAlarma_Tipo3])
        if (self.veloalarma03.get() == ''):
            self.velPropagacionAlarma_Tipo3 = 0
        else:
            self.velPropagacionAlarma_Tipo3 = float(self.veloalarma03.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp03.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo3 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo3 = 1
        if (self.const103.get() == ''):
            self.constanteEspacial1_Tipo3 = 0
        else:
            self.constanteEspacial1_Tipo3 = float(self.const103.get())  # alpha para Decaying exponential, W para raised-cosine Window
        if (self.modeloesp03.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo3 = float(self.const203.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo3 = 'k'
        self.marcador_Tipo3 = '^'


        ### Contaminación del aire
        if (self.numero10.get() == ''):
            self.dipositivos_Tipo4 = 0
        else:
            self.dipositivos_Tipo4 = float(self.numero10.get())  # número de dispositivos de tipo 4
        if (self.modelotra10.get() == 'CMMPP'):
            self.modeloTrafico_Tipo4 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo4 = 1
        self.tasaPaquete_Tipo4 = float(self.const010.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)
        if (self.tasaalarma10.get() == ''):
            self.lambdaAlarma_Tipo4 = 0
        else:
            self.lambdaAlarma_Tipo4 = float(
                self.tasaalarma10.get())
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo4, self.lambdaAlarma_Tipo4])
        if (self.veloalarma10.get() == ''):
            self.velPropagacionAlarma_Tipo4 = 0
        else:
            self.velPropagacionAlarma_Tipo4 = float(self.veloalarma10.get())  # m/s Velocidad de propagación de alarma

        if (self.modeloesp10.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo4 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo4 = 1
        if (self.const110.get() == ''):
            self.constanteEspacial1_Tipo4 = 0
        else:
            self.constanteEspacial1_Tipo4 = float(self.const110.get())   # alpha para Decaying exponential, W para raised-cosine Window
        if (self.modeloesp10.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo4 = float(self.const210.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo4 = 'k'
        self.marcador_Tipo4 = '^'

        ### Control de semáforos
        if (self.numero11.get() == ''):
            self.dipositivos_Tipo5 = 0
        else:
            self.dipositivos_Tipo5 = float(self.numero11.get())  # número de dispositivos de tipo 5
        if (self.modelotra11.get() == 'CMMPP'):
            self.modeloTrafico_Tipo5 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo5 = 1
        self.tasaPaquete_Tipo5 = float(self.const011.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)
        if (self.tasaalarma11.get() == ''):
            self.lambdaAlarma_Tipo5 = 0
        else:
            self.lambdaAlarma_Tipo5 = float(
                self.tasaalarma11.get())
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo5, self.lambdaAlarma_Tipo5])
        if (self.veloalarma11.get() == ''):
            self.velPropagacionAlarma_Tipo5 = 0
        else:
            self.velPropagacionAlarma_Tipo5 = float(self.veloalarma11.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp11.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo5 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo5 = 1
        if (self.const111.get() == ''):
            self.constanteEspacial1_Tipo5 = 0
        else:
            self.constanteEspacial1_Tipo5 = float(self.const111.get())   # alpha para Decaying exponential, W para raised-cosine Window
        if (self.modeloesp11.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo5 = float(self.const211.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo5 = 'k'
        self.marcador_Tipo5 = '^'

        ### Otros dispositivos mMTC
        if (self.numero12.get() == ''):
            self.dipositivos_Tipo6 = 0
        else:
            self.dipositivos_Tipo6 = float(self.numero12.get())  # número de dispositivos de tipo 6
        if (self.modelotra12.get() == 'CMMPP'):
            self.modeloTrafico_Tipo6 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo6 = 1
        self.tasaPaquete_Tipo6 = float(
            self.const012.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)
        if (self.tasaalarma12.get() == ''):
            self.lambdaAlarma_Tipo6 = 0
        else:
            self.lambdaAlarma_Tipo6 = float(
                self.tasaalarma12.get())
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo6, self.lambdaAlarma_Tipo6])
        if (self.veloalarma12.get() == ''):
            self.velPropagacionAlarma_Tipo6 = 0
        else:
            self.velPropagacionAlarma_Tipo6 = float(self.veloalarma12.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp12.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo6 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo6 = 1
        if (self.const112.get() == ''):
            self.constanteEspacial1_Tipo6 = 0
        else:
            self.constanteEspacial1_Tipo6 = float(
                self.const112.get())  # alpha para Decaying exponential, W para raised-cosine Window
        if (self.modeloesp12.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo6 = float(
                self.const212.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo6 = 'k'
        self.marcador_Tipo6 = '^'

        ### Dispositivos URLLC
        if (self.numero13.get() == ''):
            self.dipositivos_Tipo7 = 0
        else:
            self.dipositivos_Tipo7 = float(self.numero13.get())  # número de dispositivos de tipo 7
        if (self.modelotra13.get() == 'CMMPP'):
            self.modeloTrafico_Tipo7 = 0  # modelo de trafico 0 CMMPP 1 Periódico
        else:
            self.modeloTrafico_Tipo7 = 1
        self.tasaPaquete_Tipo7 = float(
            self.const013.get())  # la tasa lambda para el estado regular de los dispositivos de tipo 2 (0.5 paquete cada 60 seg)
        if (self.tasaalarma13.get() == ''):
            self.lambdaAlarma_Tipo7 = 0
        else:
            self.lambdaAlarma_Tipo7 = float(
                self.tasaalarma13.get())
        self.tasasEventosAlarmas.append([self.tasaPaquete_Tipo7, self.lambdaAlarma_Tipo7])
        if (self.veloalarma13.get() == ''):
            self.velPropagacionAlarma_Tipo7 = 0
        else:
            self.velPropagacionAlarma_Tipo7 = float(self.veloalarma13.get())  # m/s Velocidad de propagación de alarma
        if (self.modeloesp13.get() == 'Decaying Exponential'):
            self.modeloEspacial_Tipo7 = 0  # Propagación espacial de alarma, 0 Decaying exponential 1 raised-cosine Window
        else:
            self.modeloEspacial_Tipo7 = 1
        if (self.const113.get() == ''):
            self.constanteEspacial1_Tipo7 = 0
        else:
            self.constanteEspacial1_Tipo7 = float(
                self.const113.get())  # alpha para Decaying exponential, W para raised-cosine Window
        if (self.modeloesp13.get() == 'Raised-Cosine Window'):
            self.constanteEspacial2_Tipo7 = float(
                self.const213.get())  # ignorar para Decaying exponential, dth para raised-cosine Window
        # animacion
        self.color_Tipo7 = 'k'
        self.marcador_Tipo7 = '^'


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Generación de Tráfico IoT")
        self.master.geometry("1033x480+100+80")
        self.anchocaja1=320
        self.altocaja1=230
        self.create_widgets()

    #--------------funciones para el GUI----------------
    def cambiomodeloesp1(self, event):
        if(self.modeloesp01.get()=='Decaying Exponential'):
            self.constante11.set('Alpha')
            self.constante12.set('----')
            self.const101['state'] = 'normal'
            self.const101.delete(0, tk.END)
            self.const201.delete(0, tk.END)
            self.const201['state']='disabled'

        elif(self.modeloesp01.get()=='Raised-Cosine Window'):
            self.constante11.set('W')
            self.constante12.set('dth')
            self.const101['state'] = 'normal'
            self.const201['state'] = 'normal'
            self.const101.delete(0, tk.END)
            self.const201.delete(0, tk.END)

    def cambiomodelotra1(self, event):
        if(self.modelotra01.get()=='CMMPP'):
            self.constante10.set('Tasa promedio')
            self.const001['state'] = 'normal'
            self.const001.delete(0, tk.END)
            self.constante15.set('Tasa alarma')
            self.tasaalarma01['state'] = 'normal'
            self.tasaalarma01.delete(0, tk.END)
            self.constante16.set('Velocidad alarma')
            self.veloalarma01['state'] = 'normal'
            self.veloalarma01.delete(0, tk.END)
            self.modeloesp01['state'] = 'readonly'

        elif(self.modelotra01.get()=='Periódico'):
            self.constante10.set('Tasa de paquete')
            self.const001['state'] = 'normal'
            self.const001.delete(0, tk.END)
            self.constante15.set('---')
            self.tasaalarma01.delete(0, tk.END)
            self.tasaalarma01['state'] = 'disabled'
            self.constante16.set('---')
            self.veloalarma01.delete(0, tk.END)
            self.veloalarma01['state'] = 'disabled'
            self.constante11.set('')
            self.constante12.set('')
            self.const101.delete(0, tk.END)
            self.const201.delete(0, tk.END)
            self.const101['state'] = 'disabled'
            self.const201['state'] = 'disabled'
            self.modeloesp01.set('Seleccionar modelo')
            self.modeloesp01['state'] = 'disabled'

    def cambiomodelo2(self, event):
        if (self.modeloesp02.get() == 'Decaying Exponential'):
            self.constante21.set('Alpha')
            self.constante22.set('----')
            self.const102['state'] = 'normal'
            self.const102.delete(0, tk.END)
            self.const202.delete(0, tk.END)
            self.const202['state'] = 'disabled'

        elif (self.modeloesp02.get() == 'Raised-Cosine Window'):
            self.constante21.set('W')
            self.constante22.set('dth')
            self.const102['state'] = 'normal'
            self.const202['state'] = 'normal'
            self.const102.delete(0, tk.END)
            self.const202.delete(0, tk.END)

    def cambiomodelotra2(self, event):
        if(self.modelotra02.get()=='CMMPP'):
            self.constante20.set('Tasa promedio')
            self.const002['state'] = 'normal'
            self.const002.delete(0, tk.END)
            self.constante25.set('Tasa alarma')
            self.tasaalarma02['state'] = 'normal'
            self.tasaalarma02.delete(0, tk.END)
            self.constante26.set('Velocidad alarma')
            self.veloalarma02['state'] = 'normal'
            self.veloalarma02.delete(0, tk.END)
            self.modeloesp02['state'] = 'readonly'

        elif(self.modelotra02.get()=='Periódico'):
            self.constante20.set('Tasa de paquete')
            self.const002['state'] = 'normal'
            self.const002.delete(0, tk.END)
            self.constante25.set('---')
            self.tasaalarma02.delete(0, tk.END)
            self.tasaalarma02['state'] = 'disabled'
            self.constante26.set('---')
            self.veloalarma02.delete(0, tk.END)
            self.veloalarma02['state'] = 'disabled'
            self.constante21.set('')
            self.constante22.set('')
            self.const102.delete(0, tk.END)
            self.const202.delete(0, tk.END)
            self.const102['state'] = 'disabled'
            self.const202['state'] = 'disabled'
            self.modeloesp02.set('Seleccionar modelo')
            self.modeloesp02['state'] = 'disabled'

    def cambiomodelo3(self, event):
        if (self.modeloesp03.get() == 'Decaying Exponential'):
            self.constante31.set('Alpha')
            self.constante32.set('----')
            self.const103['state'] = 'normal'
            self.const103.delete(0, tk.END)
            self.const203.delete(0, tk.END)
            self.const203['state'] = 'disabled'

        elif (self.modeloesp03.get() == 'Raised-Cosine Window'):
            self.constante31.set('W')
            self.constante32.set('dth')
            self.const103['state'] = 'normal'
            self.const203['state'] = 'normal'
            self.const103.delete(0, tk.END)
            self.const203.delete(0, tk.END)

    def cambiomodelotra3(self, event):
        if(self.modelotra03.get()=='CMMPP'):
            self.constante30.set('Tasa promedio')
            self.const003['state'] = 'normal'
            self.const003.delete(0, tk.END)
            self.constante35.set('Tasa alarma')
            self.tasaalarma03['state'] = 'normal'
            self.tasaalarma03.delete(0, tk.END)
            self.constante36.set('Velocidad alarma')
            self.veloalarma03['state'] = 'normal'
            self.veloalarma03.delete(0, tk.END)
            self.modeloesp03['state'] = 'readonly'

        elif(self.modelotra03.get()=='Periódico'):
            self.constante30.set('Tasa de paquete')
            self.const003['state'] = 'normal'
            self.const003.delete(0, tk.END)
            self.constante35.set('---')
            self.tasaalarma03.delete(0, tk.END)
            self.tasaalarma03['state'] = 'disabled'
            self.constante36.set('---')
            self.veloalarma03.delete(0, tk.END)
            self.veloalarma03['state'] = 'disabled'
            self.constante31.set('')
            self.constante32.set('')
            self.const103.delete(0, tk.END)
            self.const203.delete(0, tk.END)
            self.const103['state'] = 'disabled'
            self.const203['state'] = 'disabled'
            self.modeloesp03.set('Seleccionar modelo')
            self.modeloesp03['state'] = 'disabled'

    def cambiomodelo4(self, event):
        if (self.modeloesp10.get() == 'Decaying Exponential'):
            self.constante41.set('Alpha')
            self.constante42.set('----')
            self.const110['state'] = 'normal'
            self.const110.delete(0, tk.END)
            self.const210.delete(0, tk.END)
            self.const210['state'] = 'disabled'
        elif (self.modeloesp10.get() == 'Raised-Cosine Window'):
            self.constante41.set('W')
            self.constante42.set('dth')
            self.const110['state'] = 'normal'
            self.const210['state'] = 'normal'
            self.const110.delete(0, tk.END)
            self.const210.delete(0, tk.END)

    def cambiomodelotra4(self, event):
        if(self.modelotra10.get()=='CMMPP'):
            self.constante40.set('Tasa promedio')
            self.const010['state'] = 'normal'
            self.const010.delete(0, tk.END)
            self.constante45.set('Tasa alarma')
            self.tasaalarma10['state'] = 'normal'
            self.tasaalarma10.delete(0, tk.END)
            self.constante46.set('Velocidad alarma')
            self.veloalarma10['state'] = 'normal'
            self.veloalarma10.delete(0, tk.END)
            self.modeloesp10['state'] = 'readonly'

        elif(self.modelotra10.get()=='Periódico'):
            self.constante40.set('Tasa de paquete')
            self.const010['state'] = 'normal'
            self.const010.delete(0, tk.END)
            self.constante45.set('---')
            self.tasaalarma10.delete(0, tk.END)
            self.tasaalarma10['state'] = 'disabled'
            self.constante46.set('---')
            self.veloalarma10.delete(0, tk.END)
            self.veloalarma10['state'] = 'disabled'
            self.constante41.set('')
            self.constante42.set('')
            self.const110.delete(0, tk.END)
            self.const210.delete(0, tk.END)
            self.const110['state'] = 'disabled'
            self.const210['state'] = 'disabled'
            self.modeloesp10.set('Seleccionar modelo')
            self.modeloesp10['state'] = 'disabled'

    def cambiomodelo5(self, event):
        if (self.modeloesp11.get() == 'Decaying Exponential'):
            self.constante51.set('Alpha')
            self.constante52.set('----')
            self.const111['state'] = 'normal'
            self.const111.delete(0, tk.END)
            self.const211.delete(0, tk.END)
            self.const211['state'] = 'disabled'

        elif (self.modeloesp11.get() == 'Raised-Cosine Window'):
            self.constante51.set('W')
            self.constante52.set('dth')
            self.const111['state'] = 'normal'
            self.const211['state'] = 'normal'
            self.const111.delete(0, tk.END)
            self.const211.delete(0, tk.END)

    def cambiomodelotra5(self, event):
        if(self.modelotra11.get()=='CMMPP'):
            self.constante50.set('Tasa promedio')
            self.const011['state'] = 'normal'
            self.const011.delete(0, tk.END)
            self.constante55.set('Tasa alarma')
            self.tasaalarma11['state'] = 'normal'
            self.tasaalarma11.delete(0, tk.END)
            self.constante56.set('Velocidad alarma')
            self.veloalarma11['state'] = 'normal'
            self.veloalarma11.delete(0, tk.END)
            self.modeloesp11['state'] = 'readonly'

        elif(self.modelotra11.get()=='Periódico'):
            self.constante50.set('Tasa de paquete')
            self.const011['state'] = 'normal'
            self.const011.delete(0, tk.END)
            self.constante55.set('---')
            self.tasaalarma11.delete(0, tk.END)
            self.tasaalarma11['state'] = 'disabled'
            self.constante56.set('---')
            self.veloalarma11.delete(0, tk.END)
            self.veloalarma11['state'] = 'disabled'
            self.constante51.set('')
            self.constante52.set('')
            self.const111.delete(0, tk.END)
            self.const211.delete(0, tk.END)
            self.const111['state'] = 'disabled'
            self.const211['state'] = 'disabled'
            self.modeloesp11.set('Seleccionar modelo')
            self.modeloesp11['state'] = 'disabled'

    def cambiomodelo6(self, event):
        if (self.modeloesp12.get() == 'Decaying Exponential'):
            self.constante61.set('Alpha')
            self.constante62.set('----')
            self.const112['state'] = 'normal'
            self.const112.delete(0, tk.END)
            self.const212.delete(0, tk.END)
            self.const212['state'] = 'disabled'
        elif (self.modeloesp12.get() == 'Raised-Cosine Window'):
            self.constante61.set('W')
            self.constante62.set('dth')
            self.const112['state'] = 'normal'
            self.const212['state'] = 'normal'
            self.const112.delete(0, tk.END)
            self.const212.delete(0, tk.END)

    def cambiomodelotra6(self, event):
        if(self.modelotra12.get()=='CMMPP'):
            self.constante60.set('Tasa promedio')
            self.const012['state'] = 'normal'
            self.const012.delete(0, tk.END)
            self.constante65.set('Tasa alarma')
            self.tasaalarma12['state'] = 'normal'
            self.tasaalarma12.delete(0, tk.END)
            self.constante66.set('Velocidad alarma')
            self.veloalarma12['state'] = 'normal'
            self.veloalarma12.delete(0, tk.END)
            self.modeloesp12['state'] = 'readonly'

        elif(self.modelotra12.get()=='Periódico'):
            self.constante60.set('Tasa de paquete')
            self.const012['state'] = 'normal'
            self.const012.delete(0, tk.END)
            self.constante65.set('---')
            self.tasaalarma12.delete(0, tk.END)
            self.tasaalarma12['state'] = 'disabled'
            self.constante66.set('---')
            self.veloalarma12.delete(0, tk.END)
            self.veloalarma12['state'] = 'disabled'
            self.constante61.set('')
            self.constante62.set('')
            self.const112.delete(0, tk.END)
            self.const212.delete(0, tk.END)
            self.const112['state'] = 'disabled'
            self.const212['state'] = 'disabled'
            self.modeloesp12.set('Seleccionar modelo')
            self.modeloesp12['state'] = 'disabled'

    def cambiomodelo7(self, event):
        if (self.modeloesp13.get() == 'Decaying Exponential'):
            self.constante71.set('Alpha')
            self.constante72.set('----')
            self.const113['state'] = 'normal'
            self.const113.delete(0, tk.END)
            self.const213.delete(0, tk.END)
            self.const213['state'] = 'disabled'
        elif (self.modeloesp13.get() == 'Raised-Cosine Window'):
            self.constante71.set('W')
            self.constante72.set('dth')
            self.const113['state'] = 'normal'
            self.const213['state'] = 'normal'
            self.const113.delete(0, tk.END)
            self.const213.delete(0, tk.END)

    def cambiomodelotra7(self, event):
        if(self.modelotra13.get()=='CMMPP'):
            self.constante70.set('Tasa promedio')
            self.const013['state'] = 'normal'
            self.const013.delete(0, tk.END)
            self.constante75.set('Tasa alarma')
            self.tasaalarma13['state'] = 'normal'
            self.tasaalarma13.delete(0, tk.END)
            self.constante76.set('Velocidad alarma')
            self.veloalarma13['state'] = 'normal'
            self.veloalarma13.delete(0, tk.END)
            self.modeloesp13['state'] = 'readonly'

        elif(self.modelotra13.get()=='Periódico'):
            self.constante70.set('Tasa de paquete')
            self.const013['state'] = 'normal'
            self.const013.delete(0, tk.END)
            self.constante75.set('---')
            self.tasaalarma13.delete(0, tk.END)
            self.tasaalarma13['state'] = 'disabled'
            self.constante76.set('---')
            self.veloalarma13.delete(0, tk.END)
            self.veloalarma13['state'] = 'disabled'
            self.constante71.set('')
            self.constante72.set('')
            self.const113.delete(0, tk.END)
            self.const213.delete(0, tk.END)
            self.const113['state'] = 'disabled'
            self.const213['state'] = 'disabled'
            self.modeloesp13.set('Seleccionar modelo')
            self.modeloesp13['state'] = 'disabled'

    def cambiomodelodisp(self,event):
        if(self.modelodisp00.get()=='PPP'):
            self.constante13.set('Intensidad')
            self.constante23.set('Intensidad')
            self.constante33.set('Intensidad')
            self.constante43.set('Intensidad')
            self.constante53.set('Intensidad')
            self.constante63.set('Intensidad')
            self.constante73.set('Intensidad')
            self.constante14.set('disp\'s/m^2')
            self.constante24.set('disp\'s/m^2')
            self.constante34.set('disp\'s/m^2')
            self.constante44.set('disp\'s/m^2')
            self.constante54.set('disp\'s/m^2')
            self.constante64.set('disp\'s/m^2')
            self.constante74.set('disp\'s/m^2')
            self.numero01['state'] = 'normal'
            self.numero01.delete(0, tk.END)
            self.numero02['state'] = 'normal'
            self.numero02.delete(0, tk.END)
            self.numero03['state'] = 'normal'
            self.numero03.delete(0, tk.END)
            self.numero10['state'] = 'normal'
            self.numero10.delete(0, tk.END)
            self.numero11['state'] = 'normal'
            self.numero11.delete(0, tk.END)
            self.numero12['state'] = 'normal'
            self.numero12.delete(0, tk.END)
            self.numero13['state'] = 'normal'
            self.numero13.delete(0, tk.END)

        else:
            self.constante13.set('Cantidad')
            self.constante23.set('Cantidad')
            self.constante33.set('Cantidad')
            self.constante43.set('Cantidad')
            self.constante53.set('Cantidad')
            self.constante63.set('Cantidad')
            self.constante73.set('Cantidad')
            self.constante14.set('dispositivos')
            self.constante24.set('dispositivos')
            self.constante34.set('dispositivos')
            self.constante44.set('dispositivos')
            self.constante54.set('dispositivos')
            self.constante64.set('dispositivos')
            self.constante74.set('dispositivos')
            self.numero01['state'] = 'normal'
            self.numero01.delete(0, tk.END)
            self.numero02['state'] = 'normal'
            self.numero02.delete(0, tk.END)
            self.numero03['state'] = 'normal'
            self.numero03.delete(0, tk.END)
            self.numero10['state'] = 'normal'
            self.numero10.delete(0, tk.END)
            self.numero11['state'] = 'normal'
            self.numero11.delete(0, tk.END)
            self.numero12['state'] = 'normal'
            self.numero12.delete(0, tk.END)
            self.numero13['state'] = 'normal'
            self.numero13.delete(0, tk.END)

    def cambiomodelodispresettodo(self):
        if (self.modelodispositivos==0):
            self.constante13.set('Intensidad')
            self.constante23.set('Intensidad')
            self.constante33.set('Intensidad')
            self.constante43.set('Intensidad')
            self.constante53.set('Intensidad')
            self.constante63.set('Intensidad')
            self.constante73.set('Intensidad')
            self.constante14.set('disp\'s/m^2')
            self.constante24.set('disp\'s/m^2')
            self.constante34.set('disp\'s/m^2')
            self.constante44.set('disp\'s/m^2')
            self.constante54.set('disp\'s/m^2')
            self.constante64.set('disp\'s/m^2')
            self.constante74.set('disp\'s/m^2')
            self.numero01['state'] = 'normal'
            self.numero01.delete(0, tk.END)
            self.numero02['state'] = 'normal'
            self.numero02.delete(0, tk.END)
            self.numero03['state'] = 'normal'
            self.numero03.delete(0, tk.END)
            self.numero10['state'] = 'normal'
            self.numero10.delete(0, tk.END)
            self.numero11['state'] = 'normal'
            self.numero11.delete(0, tk.END)
            self.numero12['state'] = 'normal'
            self.numero12.delete(0, tk.END)
            self.numero13['state'] = 'normal'
            self.numero13.delete(0, tk.END)
        else:
            self.constante13.set('Cantidad')
            self.constante23.set('Cantidad')
            self.constante33.set('Cantidad')
            self.constante43.set('Cantidad')
            self.constante53.set('Cantidad')
            self.constante63.set('Cantidad')
            self.constante73.set('Cantidad')
            self.constante14.set('dispositivos')
            self.constante24.set('dispositivos')
            self.constante34.set('dispositivos')
            self.constante44.set('dispositivos')
            self.constante54.set('dispositivos')
            self.constante64.set('dispositivos')
            self.constante74.set('dispositivos')
            self.numero01['state'] = 'normal'
            self.numero01.delete(0, tk.END)
            self.numero02['state'] = 'normal'
            self.numero02.delete(0, tk.END)
            self.numero03['state'] = 'normal'
            self.numero03.delete(0, tk.END)
            self.numero10['state'] = 'normal'
            self.numero10.delete(0, tk.END)
            self.numero11['state'] = 'normal'
            self.numero11.delete(0, tk.END)
            self.numero12['state'] = 'normal'
            self.numero12.delete(0, tk.END)
            self.numero13['state'] = 'normal'
            self.numero13.delete(0, tk.END)

    def create_widgets(self):
        self.upperFrame=tk.Frame(self.master)
        self.upperFrame.grid(row=0,column=0)
        self.middleFrame = tk.Frame(self.master)
        self.middleFrame.grid(row=1, column=0)
        self.bottomFrame = tk.LabelFrame(self.master,text='Generar Tráfico',heigh=50,width=1000,bg='grey',bd=3)
        self.bottomFrame.grid(row=2, column=0)

        self.constante10 = tk.StringVar()
        self.constante11 = tk.StringVar()
        self.constante12 = tk.StringVar()
        self.constante13 = tk.StringVar()
        self.constante14 = tk.StringVar()
        self.constante15 = tk.StringVar()
        self.constante16 = tk.StringVar()
        self.constante20 = tk.StringVar()
        self.constante21 = tk.StringVar()
        self.constante22 = tk.StringVar()
        self.constante23 = tk.StringVar()
        self.constante24 = tk.StringVar()
        self.constante25 = tk.StringVar()
        self.constante26 = tk.StringVar()
        self.constante30 = tk.StringVar()
        self.constante31 = tk.StringVar()
        self.constante32 = tk.StringVar()
        self.constante33 = tk.StringVar()
        self.constante34 = tk.StringVar()
        self.constante35 = tk.StringVar()
        self.constante36 = tk.StringVar()
        self.constante40 = tk.StringVar()
        self.constante41 = tk.StringVar()
        self.constante42 = tk.StringVar()
        self.constante43 = tk.StringVar()
        self.constante44 = tk.StringVar()
        self.constante45 = tk.StringVar()
        self.constante46 = tk.StringVar()
        self.constante50 = tk.StringVar()
        self.constante51 = tk.StringVar()
        self.constante52 = tk.StringVar()
        self.constante53 = tk.StringVar()
        self.constante54 = tk.StringVar()
        self.constante55 = tk.StringVar()
        self.constante56 = tk.StringVar()
        self.constante60 = tk.StringVar()
        self.constante61 = tk.StringVar()
        self.constante62 = tk.StringVar()
        self.constante63 = tk.StringVar()
        self.constante64 = tk.StringVar()
        self.constante65 = tk.StringVar()
        self.constante66 = tk.StringVar()
        self.constante70 = tk.StringVar()
        self.constante71 = tk.StringVar()
        self.constante72 = tk.StringVar()
        self.constante73 = tk.StringVar()
        self.constante74 = tk.StringVar()
        self.constante75 = tk.StringVar()
        self.constante76 = tk.StringVar()

        def test_Val(inStr, acttyp):
            if acttyp == '1':  # insert
                if (not inStr[len(inStr) - 1].isdigit() and not inStr[len(inStr) - 1] == '.'):
                    return False

            return True


        #----------Opciones Celula---------
        self.frame00 = tk.LabelFrame(self.upperFrame, text='Opciones de Célula', bg='grey', bd=3, height=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame00.grid(row=0, column=0, sticky='n' + 's')
        # Radio de la célula
        tk.Label(self.frame00, text='   Radio célula:  ').grid(row=0, column=0, sticky='w' + 'e')
        self.radio00 = tk.Entry(self.frame00, width=8, validate='key')
        self.radio00.grid(row=0, column=1)
        tk.Label(self.frame00, text='metros                   ').grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de distribución de usuarios
        tk.Label(self.frame00, text='   Distribución de usuarios:  ').grid(row=1, column=0, columnspan=2,sticky='w' + 'e')
        self.modelodisp00 = ttk.Combobox(self.frame00, state="readonly", width=10)
        self.modelodisp00["values"] = ['PPP', 'Uniforme']
        self.modelodisp00.set('Seleccionar')
        self.modelodisp00.bind('<<ComboboxSelected>>', self.cambiomodelodisp)
        self.modelodisp00.grid(row=1, column=2, columnspan=2)
        # Repeticiones
        tk.Label(self.frame00, text='   Repetir:  ').grid(row=2, column=0, sticky='w' + 'e')
        self.repeticiones00 = tk.Entry(self.frame00, width=8, validate='key')
        self.repeticiones00.grid(row=2, column=1)
        tk.Label(self.frame00, text='veces                    ').grid(row=2, column=2, sticky='w' + 'e')


        #-----------Recuadro de Control de iluminación------------
        self.frame01 = tk.LabelFrame(self.upperFrame, text='Control de iluminación', bg='grey', bd=3, heigh=self.altocaja1, width=self.anchocaja1)
        self.frame01.grid(row=0, column=1,sticky='n' + 's')
        #cantidad de dispositivos
        tk.Label(self.frame01,textvariable=self.constante13).grid(row=0,column=0,sticky='w'+'e')
        self.numero01 = tk.Entry(self.frame01,width=8, validate='key')
        self.numero01['validatecommand'] = (self.numero01.register(test_Val), '%P', '%d')
        self.numero01['state'] = 'disabled'
        self.numero01.grid(row=0,column=1)
        tk.Label(self.frame01, textvariable=self.constante14).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame01, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra01 = ttk.Combobox(self.frame01, state="readonly", width=18)
        self.modelotra01["values"] = ["CMMPP", "Periódico"]
        self.modelotra01.set("Seleccionar modelo")
        self.modelotra01.bind('<<ComboboxSelected>>', self.cambiomodelotra1)
        self.modelotra01.grid(row=1, column=1, columnspan=2)
        #tasa de generación de paquetes
        self.const001label =tk.Label(self.frame01, textvariable=self.constante10)
        self.const001label.grid(row=2, column=0,sticky='w'+'e')
        self.const001 = tk.Entry(self.frame01, width=8, validate='key')
        self.const001['validatecommand'] = (self.const001.register(test_Val), '%P', '%d')
        self.const001['state'] = 'disabled'
        self.const001.grid(row=2, column=1)
        tk.Label(self.frame01, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        #tasa de generación de eventos de alarma
        tk.Label(self.frame01, textvariable=self.constante15).grid(row=3, column=0,sticky='w'+'e')
        self.tasaalarma01 = tk.Entry(self.frame01,width=8, validate='key')
        self.tasaalarma01['validatecommand'] = (self.tasaalarma01.register(test_Val), '%P', '%d')
        self.tasaalarma01['state'] = 'disabled'
        self.tasaalarma01.grid(row=3, column=1)
        tk.Label(self.frame01, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        #velocidad de protagación de alarmas
        tk.Label(self.frame01, textvariable=self.constante16).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma01 = tk.Entry(self.frame01,width=8, validate='key')
        self.veloalarma01['validatecommand'] = (self.veloalarma01.register(test_Val), '%P', '%d')
        self.veloalarma01['state'] = 'disabled'
        self.veloalarma01.grid(row=4, column=1)
        tk.Label(self.frame01, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        #Modelo de propagación espacial
        tk.Label(self.frame01, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp01 = ttk.Combobox(self.frame01, state="readonly",width=18)
        self.modeloesp01["values"] = ["Decaying Exponential","Raised-Cosine Window"]
        self.modeloesp01.set("Seleccionar modelo")
        self.modeloesp01.bind('<<ComboboxSelected>>', self.cambiomodeloesp1)
        self.modeloesp01['state']='disabled'
        self.modeloesp01.grid(row=5,column=1,columnspan=2)
        #Constante modelo 1
        self.const101label = tk.Label(self.frame01, textvariable=self.constante11)
        self.const101label.grid(row=6, column=0, sticky='w' + 'e')
        self.const101= tk.Entry(self.frame01,width=8, validate='key')
        self.const101['validatecommand'] = (self.const101.register(test_Val), '%P', '%d')
        self.const101['state'] = 'disabled'
        self.const101.grid(row=6, column=1)
        # Constante modelo 2
        self.const201label = tk.Label(self.frame01, textvariable=self.constante12)
        self.const201label.grid(row=7, column=0, sticky='w' + 'e')
        self.const201 = tk.Entry(self.frame01, width=8, validate='key')
        self.const201['validatecommand'] = (self.const201.register(test_Val), '%P', '%d')
        self.const201['state'] = 'disabled'
        self.const201.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga01 =tk.Button(self.frame01,text='Reset',command=self.reset1)
        self.botoncarga01.grid(row=8,column=0,columnspan=3)

        #---------Consumo de Agua y electricidad-------------
        self.frame02 = tk.LabelFrame(self.upperFrame, text='Consumo de agua y electricidad', bg='grey', bd=3, heigh=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame02.grid(row=0, column=2, sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame02, textvariable=self.constante23).grid(row=0, column=0, sticky='w' + 'e')
        self.numero02 = tk.Entry(self.frame02, width=8, validate='key')
        self.numero02['validatecommand'] = (self.numero02.register(test_Val), '%P', '%d')
        self.numero02['state'] = 'disabled'
        self.numero02.grid(row=0, column=1)
        tk.Label(self.frame02, textvariable=self.constante24).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame02, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra02 = ttk.Combobox(self.frame02, state="readonly", width=18)
        self.modelotra02["values"] = ["CMMPP", "Periódico"]
        self.modelotra02.set("Seleccionar modelo")
        self.modelotra02.bind('<<ComboboxSelected>>', self.cambiomodelotra2)
        self.modelotra02.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const002label = tk.Label(self.frame02, textvariable=self.constante20)
        self.const002label.grid(row=2, column=0, sticky='w' + 'e')
        self.const002 = tk.Entry(self.frame02, width=8, validate='key')
        self.const002['validatecommand'] = (self.const002.register(test_Val), '%P', '%d')
        self.const002['state'] = 'disabled'
        self.const002.grid(row=2, column=1)
        tk.Label(self.frame02, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame02, textvariable=self.constante25).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma02 = tk.Entry(self.frame02, width=8, validate='key')
        self.tasaalarma02['validatecommand'] = (self.tasaalarma02.register(test_Val), '%P', '%d')
        self.tasaalarma02['state'] = 'disabled'
        self.tasaalarma02.grid(row=3, column=1)
        tk.Label(self.frame02, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame02, textvariable=self.constante26).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma02 = tk.Entry(self.frame02, width=8, validate='key')
        self.veloalarma02['validatecommand'] = (self.veloalarma02.register(test_Val), '%P', '%d')
        self.veloalarma02['state'] = 'disabled'
        self.veloalarma02.grid(row=4, column=1)
        tk.Label(self.frame02, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame02, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp02 = ttk.Combobox(self.frame02, state="readonly", width=18)
        self.modeloesp02["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp02.set("Seleccionar modelo")
        self.modeloesp02.bind('<<ComboboxSelected>>', self.cambiomodelo2)
        self.modeloesp02['state']='disabled'
        self.modeloesp02.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const102label = tk.Label(self.frame02, textvariable=self.constante21)
        self.const102label.grid(row=6, column=0, sticky='w' + 'e')
        self.const102 = tk.Entry(self.frame02, width=8, validate='key')
        self.const102['validatecommand'] = (self.const102.register(test_Val), '%P', '%d')
        self.const102['state'] = 'disabled'
        self.const102.grid(row=6, column=1)
        # Constante modelo 2
        self.const202label = tk.Label(self.frame02, textvariable=self.constante22)
        self.const202label.grid(row=7, column=0, sticky='w' + 'e')
        self.const202 = tk.Entry(self.frame02, width=8, validate='key')
        self.const202['validatecommand'] = (self.const202.register(test_Val), '%P', '%d')
        self.const202['state'] = 'disabled'
        self.const202.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga02 = tk.Button(self.frame02, text='Reset',command=self.reset2)
        self.botoncarga02.grid(row=8, column=0, columnspan=3)

        #------- Deteccción de terremotos-------------
        self.frame03 = tk.LabelFrame(self.upperFrame, text='Detección de terremotos', bg='grey', bd=3, heigh=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame03.grid(row=0, column=3,sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame03, textvariable=self.constante33).grid(row=0, column=0, sticky='w' + 'e')
        self.numero03 = tk.Entry(self.frame03, width=8, validate='key')
        self.numero03['validatecommand'] = (self.numero03.register(test_Val), '%P', '%d')
        self.numero03['state'] = 'disabled'
        self.numero03.grid(row=0, column=1)
        tk.Label(self.frame03, textvariable=self.constante34).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame03, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra03 = ttk.Combobox(self.frame03, state="readonly", width=18)
        self.modelotra03["values"] = ["CMMPP", "Periódico"]
        self.modelotra03.set("Seleccionar modelo")
        self.modelotra03.bind('<<ComboboxSelected>>', self.cambiomodelotra3)
        self.modelotra03.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const003label = tk.Label(self.frame03, textvariable=self.constante30)
        self.const003label.grid(row=2, column=0, sticky='w' + 'e')
        self.const003 = tk.Entry(self.frame03, width=8, validate='key')
        self.const003['validatecommand'] = (self.const003.register(test_Val), '%P', '%d')
        self.const003['state'] = 'disabled'
        self.const003.grid(row=2, column=1)
        tk.Label(self.frame03, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame03, textvariable=self.constante35).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma03 = tk.Entry(self.frame03, width=8, validate='key')
        self.tasaalarma03['validatecommand'] = (self.tasaalarma03.register(test_Val), '%P', '%d')
        self.tasaalarma03['state'] = 'disabled'
        self.tasaalarma03.grid(row=3, column=1)
        tk.Label(self.frame03, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame03, textvariable=self.constante36).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma03 = tk.Entry(self.frame03, width=8, validate='key')
        self.veloalarma03['validatecommand'] = (self.veloalarma03.register(test_Val), '%P', '%d')
        self.veloalarma03['state'] = 'disabled'
        self.veloalarma03.grid(row=4, column=1)
        tk.Label(self.frame03, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame03, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp03 = ttk.Combobox(self.frame03, state="readonly", width=18)
        self.modeloesp03["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp03.set("Seleccionar modelo")
        self.modeloesp03.bind('<<ComboboxSelected>>', self.cambiomodelo3)
        self.modeloesp03['state'] = 'disabled'
        self.modeloesp03.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const103label = tk.Label(self.frame03, textvariable=self.constante31)
        self.const103label.grid(row=6, column=0, sticky='w' + 'e')
        self.const103 = tk.Entry(self.frame03, width=8, validate='key')
        self.const103['validatecommand'] = (self.const103.register(test_Val), '%P', '%d')
        self.const103['state'] = 'disabled'
        self.const103.grid(row=6, column=1)
        # Constante modelo 2
        self.const203label = tk.Label(self.frame03, textvariable=self.constante32)
        self.const203label.grid(row=7, column=0, sticky='w' + 'e')
        self.const203 = tk.Entry(self.frame03, width=8, validate='key')
        self.const203['validatecommand'] = (self.const203.register(test_Val), '%P', '%d')
        self.const203['state'] = 'disabled'
        self.const203.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga03 = tk.Button(self.frame03, text='Reset',command=self.reset3)
        self.botoncarga03.grid(row=8, column=0, columnspan=3)

        #------------ Contaminación del aire -------------
        self.frame10 = tk.LabelFrame(self.middleFrame, text='Contaminación del aire', bg='grey', bd=3, heigh=self.altocaja1, width=self.anchocaja1)
        self.frame10.grid(row=0, column=0,sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame10, textvariable=self.constante43).grid(row=0, column=0, sticky='w' + 'e')
        self.numero10 = tk.Entry(self.frame10, width=8, validate='key')
        self.numero10['validatecommand'] = (self.numero10.register(test_Val), '%P', '%d')
        self.numero10['state'] = 'disabled'
        self.numero10.grid(row=0, column=1)
        tk.Label(self.frame10, textvariable=self.constante44).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame10, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra10 = ttk.Combobox(self.frame10, state="readonly", width=18)
        self.modelotra10["values"] = ["CMMPP", "Periódico"]
        self.modelotra10.set("Seleccionar modelo")
        self.modelotra10.bind('<<ComboboxSelected>>', self.cambiomodelotra4)
        self.modelotra10.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const010label = tk.Label(self.frame10, textvariable=self.constante40)
        self.const010label.grid(row=2, column=0, sticky='w' + 'e')
        self.const010 = tk.Entry(self.frame10, width=8, validate='key')
        self.const010['validatecommand'] = (self.const010.register(test_Val), '%P', '%d')
        self.const010['state'] = 'disabled'
        self.const010.grid(row=2, column=1)
        tk.Label(self.frame10, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame10, textvariable=self.constante45).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma10 = tk.Entry(self.frame10, width=8, validate='key')
        self.tasaalarma10['validatecommand'] = (self.tasaalarma10.register(test_Val), '%P', '%d')
        self.tasaalarma10['state'] = 'disabled'
        self.tasaalarma10.grid(row=3, column=1)
        tk.Label(self.frame10, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame10, textvariable=self.constante46).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma10 = tk.Entry(self.frame10, width=8, validate='key')
        self.veloalarma10['validatecommand'] = (self.veloalarma10.register(test_Val), '%P', '%d')
        self.veloalarma10['state'] = 'disabled'
        self.veloalarma10.grid(row=4, column=1)
        tk.Label(self.frame10, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame10, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp10 = ttk.Combobox(self.frame10, state="readonly", width=18)
        self.modeloesp10["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp10.set("Seleccionar modelo")
        self.modeloesp10.bind('<<ComboboxSelected>>', self.cambiomodelo4)
        self.modeloesp10['state'] = 'disabled'
        self.modeloesp10.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const110label = tk.Label(self.frame10, textvariable=self.constante41)
        self.const110label.grid(row=6, column=0, sticky='w' + 'e')
        self.const110 = tk.Entry(self.frame10, width=8, validate='key')
        self.const110['validatecommand'] = (self.const110.register(test_Val), '%P', '%d')
        self.const110['state']='disabled'
        self.const110.grid(row=6, column=1)
        # Constante modelo 2
        self.const210label = tk.Label(self.frame10, textvariable=self.constante42)
        self.const210label.grid(row=7, column=0, sticky='w' + 'e')
        self.const210 = tk.Entry(self.frame10, width=8, validate='key')
        self.const210['validatecommand'] = (self.const210.register(test_Val), '%P', '%d')
        self.const210['state']='disabled'
        self.const210.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga10 = tk.Button(self.frame10, text='Reset',command=self.reset4)
        self.botoncarga10.grid(row=8, column=0, columnspan=3)

        #------------- Control de Semáforos ----------
        self.frame11 = tk.LabelFrame(self.middleFrame, text='Control de semáforos', bg='grey', bd=3, heigh=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame11.grid(row=0, column=1,sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame11, textvariable=self.constante53).grid(row=0, column=0, sticky='w' + 'e')
        self.numero11 = tk.Entry(self.frame11, width=8, validate='key')
        self.numero11['validatecommand'] = (self.numero11.register(test_Val), '%P', '%d')
        self.numero11['state'] = 'disabled'
        self.numero11.grid(row=0, column=1)
        tk.Label(self.frame11, textvariable=self.constante54).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame11, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra11 = ttk.Combobox(self.frame11, state="readonly", width=18)
        self.modelotra11["values"] = ["CMMPP", "Periódico"]
        self.modelotra11.set("Seleccionar modelo")
        self.modelotra11.bind('<<ComboboxSelected>>', self.cambiomodelotra5)
        self.modelotra11.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const011label = tk.Label(self.frame11, textvariable=self.constante50)
        self.const011label.grid(row=2, column=0, sticky='w' + 'e')
        self.const011 = tk.Entry(self.frame11, width=8, validate='key')
        self.const011['validatecommand'] = (self.const011.register(test_Val), '%P', '%d')
        self.const011['state'] = 'disabled'
        self.const011.grid(row=2, column=1)
        tk.Label(self.frame11, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame11, textvariable=self.constante55).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma11 = tk.Entry(self.frame11, width=8, validate='key')
        self.tasaalarma11['validatecommand'] = (self.tasaalarma11.register(test_Val), '%P', '%d')
        self.tasaalarma11['state'] = 'disabled'
        self.tasaalarma11.grid(row=3, column=1)
        tk.Label(self.frame11, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame11, textvariable=self.constante56).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma11 = tk.Entry(self.frame11, width=8, validate='key')
        self.veloalarma11['validatecommand'] = (self.veloalarma11.register(test_Val), '%P', '%d')
        self.veloalarma11['state'] = 'disabled'
        self.veloalarma11.grid(row=4, column=1)
        tk.Label(self.frame11, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame11, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp11 = ttk.Combobox(self.frame11, state="readonly", width=18)
        self.modeloesp11["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp11.set("Seleccionar modelo")
        self.modeloesp11.bind('<<ComboboxSelected>>', self.cambiomodelo5)
        self.modeloesp11['state'] = 'disabled'
        self.modeloesp11.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const111label = tk.Label(self.frame11, textvariable=self.constante51)
        self.const111label.grid(row=6, column=0, sticky='w' + 'e')
        self.const111 = tk.Entry(self.frame11, width=8, validate='key')
        self.const111['validatecommand'] = (self.const111.register(test_Val), '%P', '%d')
        self.const111['state']='disabled'
        self.const111.grid(row=6, column=1)
        # Constante modelo 2
        self.const211label = tk.Label(self.frame11, textvariable=self.constante52)
        self.const211label.grid(row=7, column=0, sticky='w' + 'e')
        self.const211 = tk.Entry(self.frame11, width=8, validate='key')
        self.const211['validatecommand'] = (self.const211.register(test_Val), '%P', '%d')
        self.const211['state'] = 'disabled'
        self.const211.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga11 = tk.Button(self.frame11, text='Reset',command=self.reset5)
        self.botoncarga11.grid(row=8, column=0, columnspan=3)

        #---------Otros dispositivos mMTC

        self.frame12 = tk.LabelFrame(self.middleFrame, text='Otros dispositivos mMTC', bg='grey', bd=3, heigh=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame12.grid(row=0, column=2,sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame12, textvariable=self.constante63).grid(row=0, column=0, sticky='w' + 'e')
        self.numero12 = tk.Entry(self.frame12, width=8, validate='key')
        self.numero12['validatecommand'] = (self.numero12.register(test_Val), '%P', '%d')
        self.numero12['state'] = 'disabled'
        self.numero12.grid(row=0, column=1)
        tk.Label(self.frame12, textvariable=self.constante64).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame12, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra12 = ttk.Combobox(self.frame12, state="readonly", width=18)
        self.modelotra12["values"] = ["CMMPP", "Periódico"]
        self.modelotra12.set("Seleccionar modelo")
        self.modelotra12.bind('<<ComboboxSelected>>', self.cambiomodelotra6)
        self.modelotra12.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const012label = tk.Label(self.frame12, textvariable=self.constante60)
        self.const012label.grid(row=2, column=0, sticky='w' + 'e')
        self.const012 = tk.Entry(self.frame12, width=8, validate='key')
        self.const012['validatecommand'] = (self.const012.register(test_Val), '%P', '%d')
        self.const012['state'] = 'disabled'
        self.const012.grid(row=2, column=1)
        tk.Label(self.frame12, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame12, textvariable=self.constante65).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma12 = tk.Entry(self.frame12, width=8, validate='key')
        self.tasaalarma12['validatecommand'] = (self.tasaalarma12.register(test_Val), '%P', '%d')
        self.tasaalarma12['state'] = 'disabled'
        self.tasaalarma12.grid(row=3, column=1)
        tk.Label(self.frame12, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame12, textvariable=self.constante66).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma12 = tk.Entry(self.frame12, width=8, validate='key')
        self.veloalarma12['validatecommand'] = (self.veloalarma12.register(test_Val), '%P', '%d')
        self.veloalarma12['state'] = 'disabled'
        self.veloalarma12.grid(row=4, column=1)
        tk.Label(self.frame12, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame12, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp12 = ttk.Combobox(self.frame12, state="readonly", width=18)
        self.modeloesp12["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp12.set("Seleccionar modelo")
        self.modeloesp12.bind('<<ComboboxSelected>>', self.cambiomodelo6)
        self.modeloesp12['state'] = 'disabled'
        self.modeloesp12.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const112label = tk.Label(self.frame12, textvariable=self.constante61)
        self.const112label.grid(row=6, column=0, sticky='w' + 'e')
        self.const112 = tk.Entry(self.frame12, width=8, validate='key')
        self.const112['validatecommand'] = (self.const112.register(test_Val), '%P', '%d')
        self.const112['state'] = 'disabled'
        self.const112.grid(row=6, column=1)
        # Constante modelo 2
        self.const212label = tk.Label(self.frame12, textvariable=self.constante62)
        self.const212label.grid(row=7, column=0, sticky='w' + 'e')
        self.const212 = tk.Entry(self.frame12, width=8, validate='key')
        self.const212['validatecommand'] = (self.const212.register(test_Val), '%P', '%d')
        self.const212['state'] = 'disabled'
        self.const212.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga12 = tk.Button(self.frame12, text='Reset',command=self.reset6)
        self.botoncarga12.grid(row=8, column=0, columnspan=3)

        #----------Dispositivos URLLC-------------
        self.frame13 = tk.LabelFrame(self.middleFrame, text='Dispositivos URLLC', bg='grey', bd=3, heigh=self.altocaja1,
                                     width=self.anchocaja1)
        self.frame13.grid(row=0, column=3,sticky='n' + 's')

        # cantidad de dispositivos
        tk.Label(self.frame13, textvariable=self.constante73).grid(row=0, column=0, sticky='w' + 'e')
        self.numero13 = tk.Entry(self.frame13, width=8, validate='key')
        self.numero13['validatecommand'] = (self.numero13.register(test_Val), '%P', '%d')
        self.numero13['state'] = 'disabled'
        self.numero13.grid(row=0, column=1)
        tk.Label(self.frame13, textvariable=self.constante74).grid(row=0, column=2, sticky='w' + 'e')
        # Modelo de tráfico
        tk.Label(self.frame13, text='Modelo de tráfico:').grid(row=1, column=0, sticky='w' + 'e')
        self.modelotra13 = ttk.Combobox(self.frame13, state="readonly", width=18)
        self.modelotra13["values"] = ["CMMPP", "Periódico"]
        self.modelotra13.set("Seleccionar modelo")
        self.modelotra13.bind('<<ComboboxSelected>>', self.cambiomodelotra7)
        self.modelotra13.grid(row=1, column=1, columnspan=2)
        # tasa de generación de paquetes
        self.const013label = tk.Label(self.frame13, textvariable=self.constante70)
        self.const013label.grid(row=2, column=0, sticky='w' + 'e')
        self.const013 = tk.Entry(self.frame13, width=8, validate='key')
        self.const013['validatecommand'] = (self.const013.register(test_Val), '%P', '%d')
        self.const013['state'] = 'disabled'
        self.const013.grid(row=2, column=1)
        tk.Label(self.frame13, text='paquetes/seg').grid(row=2, column=2, sticky='w' + 'e')
        # tasa de generación de eventos de alarma
        tk.Label(self.frame13, textvariable=self.constante75).grid(row=3, column=0, sticky='w' + 'e')
        self.tasaalarma13 = tk.Entry(self.frame13, width=8, validate='key')
        self.tasaalarma13['validatecommand'] = (self.tasaalarma13.register(test_Val), '%P', '%d')
        self.tasaalarma13['state'] = 'disabled'
        self.tasaalarma13.grid(row=3, column=1)
        tk.Label(self.frame13, text='alarmas/seg').grid(row=3, column=2, sticky='w' + 'e')
        # velocidad de protagación de alarmas
        tk.Label(self.frame13, textvariable=self.constante76).grid(row=4, column=0, sticky='w' + 'e')
        self.veloalarma13 = tk.Entry(self.frame13, width=8, validate='key')
        self.veloalarma13['validatecommand'] = (self.veloalarma13.register(test_Val), '%P', '%d')
        self.veloalarma13['state'] = 'disabled'
        self.veloalarma13.grid(row=4, column=1)
        tk.Label(self.frame13, text='metros/seg').grid(row=4, column=2, sticky='w' + 'e')
        # Modelo de propagación espacial
        tk.Label(self.frame13, text='Propagación espacial:').grid(row=5, column=0, sticky='w' + 'e')
        self.modeloesp13 = ttk.Combobox(self.frame13, state="readonly", width=18)
        self.modeloesp13["values"] = ["Decaying Exponential", "Raised-Cosine Window"]
        self.modeloesp13.set("Seleccionar modelo")
        self.modeloesp13.bind('<<ComboboxSelected>>', self.cambiomodelo7)
        self.modeloesp13['state'] = 'disabled'
        self.modeloesp13.grid(row=5, column=1, columnspan=2)
        # Constante modelo 1
        self.const113label = tk.Label(self.frame13, textvariable=self.constante71)
        self.const113label.grid(row=6, column=0, sticky='w' + 'e')
        self.const113 = tk.Entry(self.frame13, width=8, validate='key')
        self.const113['validatecommand'] = (self.const113.register(test_Val), '%P', '%d')
        self.const113.grid(row=6, column=1)
        # Constante modelo 2
        self.const213label = tk.Label(self.frame13, textvariable=self.constante72)
        self.const213label.grid(row=7, column=0, sticky='w' + 'e')
        self.const213 = tk.Entry(self.frame13, width=8, validate='key')
        self.const213['validatecommand'] = (self.const213.register(test_Val), '%P', '%d')
        self.const213['state'] = 'disabled'
        self.const213.grid(row=7, column=1)
        # Boton para cargar datos
        self.botoncarga13 = tk.Button(self.frame13, text='Reset',command=self.reset7)
        self.botoncarga13.grid(row=8, column=0, columnspan=3)

        # ----------Iniciar Script-------------
        # tiempo de simulación
        tk.Label(self.bottomFrame, text='Generar por (seg):').grid(row=0, column=0, sticky='w' + 'e')
        self.tiemposimulacion = tk.Entry(self.bottomFrame, width=6)
        self.tiemposimulacion.grid(row=0, column=1)

        # diferencial de tiempo
        tk.Label(self.bottomFrame, text='Diferencial de tiempo (ms):').grid(row=0, column=3, sticky='w' + 'e')
        self.diftiempo = tk.Entry(self.bottomFrame, width=6)
        self.diftiempo.grid(row=0, column=4)

        # Boton para cargar datos
        self.cargardatos = tk.Button(self.bottomFrame, text='Cargar Datos', command=self.resetTodo)
        self.cargardatos.grid(row=0, column=5)

        # Boton para iniciar script
        self.botoniniciar = tk.Button(self.bottomFrame, text='Iniciar Rutina', command=self.rutinaCMMPP)
        self.botoniniciar.grid(row=0, column=6)

    def rutinaCMMPP(self):
        self.leerentradas()
        ######################################################
        for self.rep in range(self.repeticiones):
            tiposDisp = 0

            self.areaCelula = np.pi * self.radiocelula ** 2  # area de la célula
            # Iniciamos la creación de dispositivos según la distribución seleccionada
            # Dispositivos tipo 1
            if (self.dipositivos_Tipo1 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo1 = np.random.poisson(self.dipositivos_Tipo1 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo1 = int(self.dipositivos_Tipo1)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo1 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo1)
                self.rho_Tipo1 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo1))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo1 = self.rho_Tipo1 * np.cos(self.theta_Tipo1)
                self.yy_Tipo1 = self.rho_Tipo1 * np.sin(self.theta_Tipo1)
                self.posiciones_Tipo1 = [self.xx_Tipo1,
                                    self.yy_Tipo1]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán
            # Dispositivos tipo 2
            if (self.dipositivos_Tipo2 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo2 = np.random.poisson(self.dipositivos_Tipo2 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo2 = int(self.dipositivos_Tipo2)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo2 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo2)
                self.rho_Tipo2 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo2))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo2 = self.rho_Tipo2 * np.cos(self.theta_Tipo2)
                self.yy_Tipo2 = self.rho_Tipo2 * np.sin(self.theta_Tipo2)
                self.posiciones_Tipo2 = [self.xx_Tipo2,
                                    self.yy_Tipo2]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán
            # Dispositivos tipo 3
            if (self.dipositivos_Tipo3 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo3 = np.random.poisson(self.dipositivos_Tipo3 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo3 = int(self.dipositivos_Tipo3)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo3 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo3)
                self.rho_Tipo3 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo3))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo3 = self.rho_Tipo3 * np.cos(self.theta_Tipo3)
                self.yy_Tipo3 = self.rho_Tipo3 * np.sin(self.theta_Tipo3)
                self.posiciones_Tipo3 = [self.xx_Tipo3,
                                    self.yy_Tipo3]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán

            # Dispositivos tipo 4
            if (self.dipositivos_Tipo4 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo4 = np.random.poisson(
                        self.dipositivos_Tipo4 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo4 = int(
                        self.dipositivos_Tipo4)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo4 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo4)
                self.rho_Tipo4 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo4))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo4 = self.rho_Tipo4 * np.cos(self.theta_Tipo4)
                self.yy_Tipo4 = self.rho_Tipo4 * np.sin(self.theta_Tipo4)
                self.posiciones_Tipo4 = [self.xx_Tipo4,
                                         self.yy_Tipo4]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán

            # Dispositivos tipo 5
            if (self.dipositivos_Tipo5 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo5 = np.random.poisson(
                        self.dipositivos_Tipo5 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo5 = int(
                        self.dipositivos_Tipo5)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo5 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo5)
                self.rho_Tipo5 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo5))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo5 = self.rho_Tipo5 * np.cos(self.theta_Tipo5)
                self.yy_Tipo5 = self.rho_Tipo5 * np.sin(self.theta_Tipo5)
                self.posiciones_Tipo5 = [self.xx_Tipo5,
                                         self.yy_Tipo5]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán

            # Dispositivos tipo 6
            if (self.dipositivos_Tipo6 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo6 = np.random.poisson(
                        self.dipositivos_Tipo6 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo6 = int(
                        self.dipositivos_Tipo6)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo6 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo6)
                self.rho_Tipo6 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo6))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo6 = self.rho_Tipo6 * np.cos(self.theta_Tipo6)
                self.yy_Tipo6 = self.rho_Tipo6 * np.sin(self.theta_Tipo6)
                self.posiciones_Tipo6 = [self.xx_Tipo6,
                                         self.yy_Tipo6]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán

            # Dispositivos tipo 7 | URLLC
            if (self.dipositivos_Tipo7 > 0):  # si la cantidad de dispositivos es mayor a cero
                tiposDisp = tiposDisp + 1
                if (self.modelodispositivos == 0):
                    self.cantidad_Tipo7 = np.random.poisson(
                        self.dipositivos_Tipo7 * self.areaCelula)  # Poisson número de dispoitivos de tipo1
                else:
                    self.cantidad_Tipo7 = int(
                        self.dipositivos_Tipo7)  # si no se trata de un PPP se generarán los dispositivos especifiados
                self.theta_Tipo7 = 2 * np.pi * np.random.uniform(0, 1, self.cantidad_Tipo7)
                self.rho_Tipo7 = self.radiocelula * np.sqrt(np.random.uniform(0, 1, self.cantidad_Tipo7))
                # Convertimos las coordenadas polares a cartesianas
                self.xx_Tipo7 = self.rho_Tipo7 * np.cos(self.theta_Tipo7)
                self.yy_Tipo7 = self.rho_Tipo7 * np.sin(self.theta_Tipo7)
                self.posiciones_Tipo7 = [self.xx_Tipo7,
                                         self.yy_Tipo7]  # Esta lista se usará para asignar posiciones a los dispositivos que se crearán

            self.tiempo = 0  # tiempo inicial
            self.iteraciones = self.tiempoLimite / self.deltaTiempo  # las iteraciones  que se producirán recorriendo el tiempo k
            self.dispositivos = []  # una lista para guardar las instancias de dipoitivos de distintos tipos
            self.generadoresAlarmas = []  # una lista para guardar los genradores de eventos de alarmas, uno para cada tipo de dispositivo
            self.nuevaAlarma = [False] * tiposDisp
            DeviceMTC.tiempoLitime=self.tiempoLimite
            self.DispositivosTodos=[]



            # Se generan las instancias de cada tipo de dipositivos y sus generadores de alarmas
            # tipo 1
            if (self.dipositivos_Tipo1 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo1, self.cantidad_Tipo1, self.posiciones_Tipo1, self.tasaPaquete_Tipo1, 'Control de iluminacion', self.tiempo,
                                      self.color_Tipo1, self.marcador_Tipo1,self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(1,self.modeloTrafico_Tipo1, self.lambdaAlarma_Tipo1, self.velPropagacionAlarma_Tipo1, self.tiempo, self.modeloEspacial_Tipo1,
                                     self.constanteEspacial1_Tipo1, self.constanteEspacial2_Tipo1, [0, 0]))
            # tipo 2
            if (self.dipositivos_Tipo2 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo2, self.cantidad_Tipo2, self.posiciones_Tipo2, self.tasaPaquete_Tipo2, 'Monitoreo de agua y electricidad',
                                      self.tiempo, self.color_Tipo2, self.marcador_Tipo2, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(2,self.modeloTrafico_Tipo2, self.lambdaAlarma_Tipo2, self.velPropagacionAlarma_Tipo2, self.tiempo, self.modeloEspacial_Tipo2,
                                     self.constanteEspacial1_Tipo2, self.constanteEspacial2_Tipo2, [0, 0]))
            # tipo 3
            if (self.dipositivos_Tipo3 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo3, self.cantidad_Tipo3, self.posiciones_Tipo3, self.tasaPaquete_Tipo3, 'Deteccion de terremotos', self.tiempo,
                                      self.color_Tipo3, self.marcador_Tipo3, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(3,self.modeloTrafico_Tipo3, self.lambdaAlarma_Tipo3, self.velPropagacionAlarma_Tipo3, self.tiempo, self.modeloEspacial_Tipo3,
                                     self.constanteEspacial1_Tipo3, self.constanteEspacial2_Tipo3, [0, 0]))
            # tipo 4
            if (self.dipositivos_Tipo4 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo4, self.cantidad_Tipo4, self.posiciones_Tipo4,
                                      self.tasaPaquete_Tipo4, 'Semaforos inteligentes', self.tiempo,
                                      self.color_Tipo4, self.marcador_Tipo4, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(4,self.modeloTrafico_Tipo4, self.lambdaAlarma_Tipo4, self.velPropagacionAlarma_Tipo4,
                                     self.tiempo, self.modeloEspacial_Tipo4,
                                     self.constanteEspacial1_Tipo4, self.constanteEspacial2_Tipo4, [0, 0]))

            # tipo 5
            if (self.dipositivos_Tipo5 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo5, self.cantidad_Tipo5, self.posiciones_Tipo5,
                                      self.tasaPaquete_Tipo5, 'Contaminacion del aire', self.tiempo,
                                      self.color_Tipo5, self.marcador_Tipo5, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(5,self.modeloTrafico_Tipo5, self.lambdaAlarma_Tipo5, self.velPropagacionAlarma_Tipo5,
                                     self.tiempo, self.modeloEspacial_Tipo5,
                                     self.constanteEspacial1_Tipo5, self.constanteEspacial2_Tipo5, [0, 0]))

            # tipo 6
            if (self.dipositivos_Tipo6 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo6, self.cantidad_Tipo6, self.posiciones_Tipo6,
                                      self.tasaPaquete_Tipo6, 'Otros dispositivos mMTC', self.tiempo,
                                      self.color_Tipo6, self.marcador_Tipo6, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(6,self.modeloTrafico_Tipo6, self.lambdaAlarma_Tipo6, self.velPropagacionAlarma_Tipo6,
                                     self.tiempo, self.modeloEspacial_Tipo6,
                                     self.constanteEspacial1_Tipo6, self.constanteEspacial2_Tipo6, [0, 0]))

            # tipo 7
            if (self.dipositivos_Tipo7 > 0):
                self.dispositivos.append(
                    creardispositivos(self.modeloTrafico_Tipo7, self.cantidad_Tipo7, self.posiciones_Tipo7,
                                      self.tasaPaquete_Tipo7, 'Dispositivos URLLC', self.tiempo,
                                      self.color_Tipo7, self.marcador_Tipo7, self.DispositivosTodos))
                self.generadoresAlarmas.append(
                    GeneradorAlarmas(7,self.modeloTrafico_Tipo7, self.lambdaAlarma_Tipo7, self.velPropagacionAlarma_Tipo7,
                                     self.tiempo, self.modeloEspacial_Tipo7,
                                     self.constanteEspacial1_Tipo7, self.constanteEspacial2_Tipo7, [0, 0]))

            ##########  Algoritmo CMMPP  #################

            for self.k in range(0, int(self.iteraciones + 1)):  # Ciclo que avanza el tiempo

                for self.dispositivosaux, self.generadorAlarma, self.tipoDisp in iter.zip_longest(self.dispositivos, self.generadoresAlarmas,
                                                                                   range(0,
                                                                                         self.dispositivos.__len__())):  # Ciclo que recorre los distintos tipos de dispositivos y sus geenradores de alarmas

                    if (self.tiempo == 0):
                        self.nuevaAlarma[self.tipoDisp] = self.generadorAlarma.generarAlarma(self.tiempo, self.radiocelula)  # se calcula el primer tiempo de alarma

                    for self.dispositivo in self.dispositivosaux:  # Ciclo que recorre cada uno de los dispositivos del mismo tipo

                        ##### Esto sólo compete a los dispositivos con modelo CMMPP
                        if (self.dispositivo.modeloTrafico == 0):  # Si se trata del algoritmo CMMPP se registra la nueva alarma en caso de haberla
                            self.dispositivo.registrarAlarma(self.generadorAlarma.idAlarma, self.generadorAlarma.siguienteArribo, (
                                    self.generadorAlarma.siguienteArribo + (distanciaList(self.dispositivo.posicion,
                                                                                     self.generadorAlarma.posicion) / self.generadorAlarma.velocidad))[
                            0], self.generadorAlarma.posicion, self.nuevaAlarma[self.tipoDisp])


                            [self.listaPnk, self.nuevaListaAlarmas] = calcularPnk(self.tiempo, self.dispositivo.listaAlarmas,
                                                                    self.generadorAlarma.velocidad,
                                                                    self.generadorAlarma.modeloEspacial,
                                                                    self.generadorAlarma.constanteEspacial1,
                                                                    self.generadorAlarma.constanteEspacial2, self.dispositivo.m_Pu,
                                                                    self.dispositivo.m_Pc,
                                                                    self.deltaTiempo)  # parte A del diagrama  /assets/CMMPP_diagrama.jpg

                            # listaAlarmas=[idAlarma,tiempoAparicion,tiempoLLegada,posicionAlarma,self.posicion] esta es la forma de listaAlarmas
                            for self.pnk, self.listaAlarmas in iter.zip_longest(self.listaPnk, self.dispositivo.listaAlarmas):
                                self.dispositivo.actualizarestado(self.pnk)  # parte B del diagrama
                                self.dispositivo.generararribo(self.tiempo, self.listaAlarmas[0], self.listaAlarmas[2],
                                                      self.numerosDecimalesDeltaTiempo)  # parte C del diagrama
                                self.dispositivo.actualizarestadoanormal()  # por si hay más de un evento que cree estados de alarma, se cambia siempre a estado normal,

                            self.dispositivo.actualizarListaAlarmas(self.nuevaListaAlarmas)
                        ##### Esto sólo compete a los dispositivos con modelo Periódico
                        if (self.dispositivo.modeloTrafico == 1):
                            self.dispositivo.generararriboperiodico(self.tiempo,self.numerosDecimalesDeltaTiempo)

                    self.nuevaAlarma[self.tipoDisp] = self.generadorAlarma.generarAlarma(self.tiempo,
                                                                          self.radiocelula)  # se genera una nueva alarma en una posición aleatoria si la actual ya sucedió

                self.tiempo = round(self.tiempo + self.deltaTiempo, self.numerosDecimalesDeltaTiempo)  # Función para redondear decimales

            def takeSecond(elem):
                return elem[1]
            self.arriboOrdenado = self.dispositivo.registroCompletoArribos.sort(key=takeSecond) # Ordenamos los arribos por tiempo
            self.ultimodispositivo=self.dispositivo
            # Registro de todos los eventos
            self.ListaEventos = self.dispositivo.registroCompletoArribos
            # Creación de un Dataframe apartir de una lista
            self.df_eventos = pd.DataFrame(self.ListaEventos)
            # Creación de un Dataframe apartir de una lista
            self.df_dispositivos = pd.DataFrame(self.DispositivosTodos)
            # Guardado de datos en archivo con extensión .csv
            nombreArchivo="ArchivoEventos"+str(self.rep)+".csv"
            nombreArchivoDisp = "ArchivoDispositivos" + str(self.rep) + ".csv"
            self.df_eventos.to_csv(nombreArchivo)
            self.df_dispositivos.to_csv(nombreArchivoDisp)

            ## se crea archivo de salida con información de la configuración
            self.configSalida.append([0,self.radiocelula,self.tiempo,self.k,0.0,0.0,0.0])
            if (self.dipositivos_Tipo1 > 0):
                self.configSalida.append([1, self.modeloTrafico_Tipo1,self.tasaPaquete_Tipo1, self.lambdaAlarma_Tipo1, self.modeloEspacial_Tipo1,self.constanteEspacial1_Tipo1,self.constanteEspacial2_Tipo1])
            if (self.dipositivos_Tipo2 > 0):
                self.configSalida.append([2, self.modeloTrafico_Tipo2, self.tasaPaquete_Tipo2, self.lambdaAlarma_Tipo2, self.modeloEspacial_Tipo2,self.constanteEspacial1_Tipo2,self.constanteEspacial2_Tipo2])
            if (self.dipositivos_Tipo3 > 0):
                self.configSalida.append([3,self.modeloTrafico_Tipo3, self.tasaPaquete_Tipo3, self.lambdaAlarma_Tipo3, self.modeloEspacial_Tipo3,self.constanteEspacial1_Tipo3,self.constanteEspacial2_Tipo3])
            if (self.dipositivos_Tipo4 > 0):
                self.configSalida.append([4,self.modeloTrafico_Tipo4, self.tasaPaquete_Tipo4, self.lambdaAlarma_Tipo4, self.modeloEspacial_Tipo4,self.constanteEspacial1_Tipo4,self.constanteEspacial2_Tipo4])
            if (self.dipositivos_Tipo5 > 0):
                self.configSalida.append([5, self.modeloTrafico_Tipo5,self.tasaPaquete_Tipo5, self.lambdaAlarma_Tipo5, self.modeloEspacial_Tipo5,self.constanteEspacial1_Tipo5,self.constanteEspacial2_Tipo5])
            if (self.dipositivos_Tipo6 > 0):
                self.configSalida.append([6, self.modeloTrafico_Tipo6,self.tasaPaquete_Tipo6, self.lambdaAlarma_Tipo6, self.modeloEspacial_Tipo6,self.constanteEspacial1_Tipo6,self.constanteEspacial2_Tipo6])
            if (self.dipositivos_Tipo7 > 0):
                self.configSalida.append([7,self.modeloTrafico_Tipo7, self.tasaPaquete_Tipo7, self.lambdaAlarma_Tipo7, self.modeloEspacial_Tipo7,self.constanteEspacial1_Tipo7,self.constanteEspacial2_Tipo7])
            self.df_configSalida = pd.DataFrame(self.configSalida)
            nombreconfigSalida = "ArchivoConfigSalida" + str(self.rep) + ".csv"
            self.df_configSalida.to_csv(nombreconfigSalida)

            ## se crea archivo de salida con todas las alarmas
            self.df_ArchivoAlarmas = pd.DataFrame(GeneradorAlarmas.TodasAlarmas)
            nombreArchivoAlarmas = "ArchivoAlarmas" + str(self.rep) + ".csv"
            self.df_ArchivoAlarmas.to_csv(nombreArchivoAlarmas)

            DeviceMTC.registroCompletoArribos=[]
            DeviceMTC.cuentaAlarmas = 0
            DeviceMTC.totalAlarmas = []
            DeviceMTC.totalDispositivos=1
            GeneradorAlarmas.TodasAlarmas = []
            self.configSalida = []

            print('Fin de Rutina ')




root = tk.Tk()
app = Application(master=root)
app.mainloop()