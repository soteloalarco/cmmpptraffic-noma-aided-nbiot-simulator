class Subportadora(object):
    def __init__(self, id,  C, c_, Cluster):
        self.id = id                #Identificador para cada suubportadora
        self.C = C                  #Grupo NOMA
        self.c_ = c_                #Mejor grupo NOMA que maximisa la tasa
        self.Cluster = Cluster      #Cluster asignado a subportadora
