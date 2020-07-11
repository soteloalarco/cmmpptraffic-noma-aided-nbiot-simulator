import sys
from des import sim


class Module:
    """
    Define un módulo de simulación genérico, implementando algunas funcionalidades
    básicas que todos los módulos deben heredar.
    Defines a generic simulation module, implementing some basic functionalities
    that all modules should inherit from.
    """
    # variable de clase estática que incrementa automáticamente cada vez que un
    # módulo es instanciado
    # static class variable automatically incremented everytime a new module is
    # instantiated
    __modules_count = 0

    def __init__(self,id,tipo):
        """
        Constructor. Obtiene una instancia de la simulación para calendarizar
        eventos y asigna un id al módulo.
        Constructor. Gets simulation instance for scheduling events and
        automatically assigns an ID to the module.
        """
        self.sim = sim.Sim.Instance()
        # se asigna id al módulo
        # assign id to module
        self.module_id = id
        Module.__modules_count = Module.__modules_count + 1
        # se asigna tipo al módulo
        # module type is asigned
        self.module_tipo= tipo
        # se obtiene el lógger de la instancia del simulador
        # get data logger from simulator
        self.logger = self.sim.get_logger()

    def initialize(self):
        """
        Método de inicialización llamado por la simulación para cada
        nuevo módulo instanciado.
        Initialization method called by the simulation for each newly
        instantiated module.
        """
        return

    def handle_event(self, event):
        """
        Esta función debería ser sobreescrita por los módulos que heredan
        esta clase para encargarse de los eventos.
        This function should be overridden by inheriting modules to handle
        events for this module. If not overridden, this method will throw an
        error and stop the simulation.
        """
        print("Module error: class %s does not override handle_event() method",
              self.get_type())
        sys.exit(1)

    def get_id(self):
        """
        Retorna el id del módulo.
        Returns module id.
        """
        return self.module_id

    def get_type(self):
        """
        Retorna el tipo del módulo.
        Returns module type.
        """
        return self.__class__.__name__

    def get_tipo(self):
        """
        Retorna el tipo del módulo ingresado
        Returns module type
        """
        return self.module_tipo