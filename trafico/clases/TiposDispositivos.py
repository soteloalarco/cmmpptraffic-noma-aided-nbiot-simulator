
class TiposDispositivos:

    TIPO1 = 'Control de iluminacion'
    TIPO2 = 'Monitoreo de agua y electricidad'
    TIPO3 = 'Deteccion de terremotos'
    TIPO4 = 'Contaminacion del aire'
    TIPO5 =  'Semaforos inteligentes'
    TIPO6 =  'Otros dispositivos mMTC'
    TIPO7 = 'Dispositivos URLLC'

    def tipocolor(tipo):
        if tipo==TiposDispositivos.TIPO1:
            return 'b'
        if tipo==TiposDispositivos.TIPO2:
            return 'g'
        if tipo==TiposDispositivos.TIPO3:
            return 'tab:orange'
        if tipo==TiposDispositivos.TIPO4:
            return 'c'
        if tipo==TiposDispositivos.TIPO5:
            return 'm'
        if tipo==TiposDispositivos.TIPO6:
            return 'y'
        if tipo==TiposDispositivos.TIPO7:
            return 'tab:brown'
