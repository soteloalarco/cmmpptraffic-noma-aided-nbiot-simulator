
from singleton import Singleton


@Singleton
class Sim:

    """
    Clase principal del simulador
    """

# nombre de las secciones en el archivo de configuración que incluyen los parámetros
    PAR_SECCION = "Simulacion"
    # parámetro de duración de la simulación
    PAR_DURACION = "duracion"
    # nombre del archivo del que se leerán los eventos
    PAR_EVENTOS = "archivoEventos"
    # position of the nodes
    PAR_TIEMPOINICIAL = "TiempoInicial"
    PAR_TSNPRACH = "TsNPRACH"
    PAR_TSNOMA = "TsNOMA"

    """ahora = tiempoInicial  # variable que regristra el avance en el tiempo
    universoNOMA = {}
    universoNPRACH = {}"""

    def __init__(self):
        """
        Constructor inicializando el tiempoActual con el tiempoInicial y creando
        las listas de colas vacias.
        """
        # Tiempo actual en la simulación
        self.tiempo = 0
        # queue of events, implemented as a heap
        self.queue = []
        # list of nodes
        self.UE = []
        # inicializar() debe llamarse antes de iniciar la simulación
        self.inicializar = False
        # archivo de configuracion vacio
        self.config_archivo = ""
        # seccion vacia
        self.seccion = ""
