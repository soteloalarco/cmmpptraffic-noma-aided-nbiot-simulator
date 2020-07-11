class NB_IoT(object):
    def __init__(self, numS, S, Sv, Agrupaciones, Cns, numC, C, numU, U, numM, M, id_c, c_, kmax, BW, No):
        self.numS = numS    #Numero de subportadoras
        self.S = S          #Lista de subportadoras
        self.Sv = Sv        #Conjunto de subportadoras eliminadas
        self.Agrupaciones = Agrupaciones #Conjunto de agrupaciones finales entre S y C
        self.Cns = Cns      #Lista de grupos NOMA con tasas insatisfechas
        self.numC = numC    #Numero de grupos NOMA
        self.C = C          #Lista de Grupos NOMA
        self.numU = numU    #Numero de dispositivos URLLC
        self.U = U          #Lista de dispositivos URLLC
        self.numM = numM    #Numero de dispositivos mMTC
        self.M = M          #Lista de dispositivos mMTC
        self.id_c = id_c    #Id del mejor grupo NOMA
        self.c_ = c_        #Mejor grupo NOMA que maximisa la tasa
        self.kmax = kmax    #Máxima capacidad de grupo NOMA
        self.BW = BW        #Ancho de banda por bloque de recurso (Subportadora)
        self.No = No        #Densidad de potencia spectral -173 dBm/Hz,
