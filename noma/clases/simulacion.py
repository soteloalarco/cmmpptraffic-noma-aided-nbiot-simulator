class Simulacion(object):
    def __init__(self, umbralArribos, PLE, r_cell):
        self.umbralArribos = umbralArribos          #Umbral de arribos para paro de la simulación
        self.PLE = PLE       #Path Loss Exponent
        self.r_cell = r_cell #Radio de la celula
