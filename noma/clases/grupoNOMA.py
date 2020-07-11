class GrupoNOMA(object):
    def __init__(self, id, dispositivos, RTotal, gamma, Sac, tasasSatisfechas):
        self.id = id        # Identificador de Grupo
        self.dispositivos = dispositivos    #Lista de dispositivos agrupados en orden
        self.RTotal = RTotal        #RTotal acumula las tasas de cada dispositivo por grupo y asi obtener la tasa alcanzada por grupo
        self.gamma = gamma          #Variable binaria que indica la asignación de un cluster para una subportadora
        self.Sac = Sac              #Conjunto de subportadoras asignadas a un cluster C
        self.tasasSatisfechas = tasasSatisfechas    #Booleano