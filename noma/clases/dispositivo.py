class Dispositivo(object):
    #Constructor
    def __init__(self, id, tipo, alphabeta, d, h_, h, Rx, Rs, Px, Rth):
        self.id = id        #Identificador de dispositivo
        self.tipo = tipo    #Tipo de Dispositivo
        self.alphabeta = alphabeta  #Variable binaria que indica si el dispositivo esta agrupado en un cluster NOMA
        self.d = d         #Distancia entre BS y UE
        self.h_ = h_        #Ganancia de canal promedio
        self.h = h          #Ganancias de canal por subportadora
        self.Rx = Rx        #Tasa de transmisión
        self.Rs = Rs        #Suma acumulada de tasas de tx por subportadora
        self.Px = Px        #Potencia de transmisión
        self.Rth = Rth      #Umbral de tasa para dispositivos
