from trafico.clases.TiposDispositivos import TiposDispositivos
from trafico.funciones.funcionesgraficar import graficaralarmas
from trafico.funciones.funcionesgraficar import graficardispositivos
from trafico.funciones.funcionesgraficar import histogramatodoseventos
from trafico.funciones.funcionesgraficar import graficareventosportipodispositivo

graficaralarmas('ArchivoEventos0.csv','ArchivoAlarmas0.csv','ArchivoDispositivos0.csv','ArchivoConfigSalida0.csv',TiposDispositivos.TIPO5)

#graficardispositivos('ArchivoDispositivos0.csv','ArchivoConfigSalida0.csv')
#histogramatodoseventos('ArchivoEventos0.csv','ArchivoConfigSalida0.csv')
#graficareventosportipodispositivo('ArchivoEventos0.csv','ArchivoConfigSalida0.csv','ArchivoAlarmas0.csv')
