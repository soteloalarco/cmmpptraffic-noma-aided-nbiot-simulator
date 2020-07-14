import numpy as np  # NumPy package for arrays, random number generation, etc


class DeviceMTC(object):

    totalDispositivos=1

    # Definición de constructor
    def __init__(self, modelotrafico,lambdareg, Xpos, Ypos, estado, tipo,tiempoInicial,identificador, registroArribos, tamañopkt,color,marcador):
        self.modeloTrafico= modelotrafico # 0 para tráfico CMMPP y 1 para periodico
        self.lambdareg = lambdareg # tasa de generación de paquetes
        self.posicion = [Xpos, Ypos]  # la posición espacial dentro de la celula
        self.estado = estado  # estado regular o de alarma (0 es regular y 1 alarma)
        self.tipo = tipo  # tipo de dispositivo
        self.tiempoArribo = self.calculartiempoinicial(tiempoInicial,modelotrafico,lambdareg) # siguiente instante en el que se realizará una petición, debe iniciarse con el tiempo inicial
        self.identificador = identificador # un id de cada dispositivo, se puede repetir en distintos tipos de dispositivo
        self.registroArribos = registroArribos # lista de los arribos calendarizados a partir de este dispositivo
        self.tamañopkt = tamañopkt # tamaño de paquete del evento actual calculado
        self.color=color # color de dispositivo en la animacion
        self.marcador=marcador # marcador del dispositivo en la animacion
        self.listaAlarmas=[] # en esta lista se guardan los eventos de alarma que aun no llegan a la posición del dispositivo, se guarda el tiempo y la posicion donde se origina la alarma

    def calculartiempoinicial(self,tiempoInicial,modelotrafico,lambdareg): # se calcula el tiempo inicial, apartir del cual se generan paquetes, si el modelo es periodico se calcula aleatoriamenten en un valor menor a un periodo
        if(modelotrafico==0):
            return tiempoInicial
        else:
            return tiempoInicial + np.random.uniform(0,1/lambdareg,1)

    matriz_Pu = [[1, 1], [0, 0]]  # matriz que describe el comportamiento no unsincronized
    m_Pu = np.array(matriz_Pu)
    matriz_Pc = [[0, 1], [1, 0]]  # matriz que describe el comportamiento sincronized
    m_Pc = np.array(matriz_Pc)
    registroCompletoArribos = []  # El conglomerado de arribos del estado normal y del de alarma
    cuentaAlarmas = 0  # Contador que registra las veces que se estuvo en estado de alarma
    totalAlarmas=[]
    tiempoLitime=0

    def actualizarestado(self, pnk):
        auxUniforme = np.random.uniform(0, 1, 1)
        if self.estado == 1 and auxUniforme > pnk[1][1]:  # Si se está en estado alarma y si la variable uniforme es mayor a la probabilidad de que no cambie de estado, cambia de estado
            self.estado = 0
        if self.estado == 0 and auxUniforme > pnk[0][0]:  # Si se está en estado normal y si la variable uniforme es mayor a la probabilidad de que no cambie de estado, cambia de estado
            self.estado = 1

    def generararribo(self, tiempo, identificadorEvento, tiempoAlarma,numeroDecimales):
        if self.estado == 1:  # alarma
            self.generarpaquetealarma() # tamaño fijo parte D del diagrama  /assets/CMMPP_diagrama.jpg
            self.generararriboalarma(tiempoAlarma,identificadorEvento,numeroDecimales)  # Generar exactamente 1 paquete

        elif self.tiempoArribo <= tiempo:
            self.generarpaquetenormal() # variable de pareto parte D del diagrama  /assets/CMMPP_diagrama.jpg
            self.generararribonormal(numeroDecimales)  # Generar un paquete en caso de que no exista ya uno

    def generararriboalarma(self, tiempo,identificadorEvento,numeroDecimales):
        self.registroArribos.append([identificadorEvento, round(tiempo,numeroDecimales+1),self.identificador,self.tipo,self.estado,self.tamañopkt])  # se registra el arribo en la lista
        self.registroCompletoArribos.append([identificadorEvento, round(tiempo,numeroDecimales+1),self.identificador,self.tipo,self.estado,self.tamañopkt,self.modeloTrafico])
        self.cuentaAlarmas = self.cuentaAlarmas + 1 #¿QUE FUNCION TIENE ESTE CONTADOR?, sólo es para ver si los valores que produce el programa tienen sentido.
        self.totalAlarmas.append([self.identificador,self.tipo,tiempo])

    def generararribonormal(self,numeroDecimales):
        tiempoEspera = np.random.exponential(1 / (self.lambdareg), 1)  # el siguiente arribo se producirá segun una varible exponencial
        self.tiempoArribo = self.tiempoArribo + tiempoEspera
        #TODO dar flexibilidad a la cantidad de decimales que se pueden evaluar
        if(self.tiempoArribo<=self.tiempoLitime): # Sólo registrar el evento si ocurriría antes que el tiempo límite de la simulación
            self.registroArribos.append([0,round(float(self.tiempoArribo),numeroDecimales+1),self.identificador, self.tipo,self.estado,self.tamañopkt])  # se registra el arribo en la lista
            self.registroCompletoArribos.append([0,round(float(self.tiempoArribo),numeroDecimales+1),self.identificador, self.tipo,self.estado, self.tamañopkt,self.modeloTrafico])

    def generararriboperiodico(self,tiempo,numeroDecimales):
        if self.tiempoArribo <= tiempo:
            self.generarpaquetenormal()
            self.registroArribos.append(
                [0, round(float(self.tiempoArribo), numeroDecimales + 1), self.identificador, self.tipo, self.estado,
                 self.tamañopkt])  # se registra el arribo en la lista
            self.registroCompletoArribos.append(
                [0, round(float(self.tiempoArribo), numeroDecimales + 1), self.identificador, self.tipo, self.estado,
                 self.tamañopkt,self.modeloTrafico])

            self.tiempoArribo=self.tiempoArribo+(1/self.lambdareg) # se agrega un arribo en el siguiente periodo



    def generarpaquetenormal(self): # Generar paquete con distribución de Pareto
        while True:
            minimo = 20  # la cota menor para los tamaños
            shape = 1  # el parámetro de forma de la disgtribución, también conocido como `a` o `alpha`
            tamano = 1  # el tamaño de tu muestra (número de valores aleatorios)
            x = np.random.pareto(shape, tamano) + minimo
            upper = x
            if upper<=200:
                break
        self.tamañopkt=round(x[0],2)

    def generarpaquetealarma(self):
        self.tamañopkt=20

    def hayPaquete(self,tiempo,delta):
        if(tiempo <= self.tiempoArribo < tiempo+delta):
            return True
        else:
            return False

    def registrarAlarma(self, idAlarma, tiempoAparicion, tiempoLLegada, posicionAlarma, nuevaAlarma):
        if(nuevaAlarma):
            self.listaAlarmas.append([idAlarma,tiempoAparicion,tiempoLLegada,posicionAlarma,self.posicion])

    def actualizarListaAlarmas(self,nuevaLista):
        self.listaAlarmas=nuevaLista

    def actualizarestadoanormal(self):
        self.estado=0
