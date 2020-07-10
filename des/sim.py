# la versión original de este software libre ha sido modificada a su
# forma actual por Rolando Sotelo y Fernando Salazar, pero hereda su
# licencia de uso público

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2016 Michele Segata <segata@ccs-labs.org>


from __future__ import division
import sys
import heapq
import time
import math
from des.singleton import Singleton
from des.config import Config
from des.channel import Channel
from des.node import Node
from des.log import Log
import pandas as pd

# comando VT100 para borrar contenido de la terminal actual
# VT100 command for erasing content of the current prompt line
ERASE_LINE = '\x1b[2K'


@Singleton
class Sim:
    """
    Clase principal del simulador.
    Main simulator class.
    """

    # nombre de la sección en el archivo de configuración que incluye todos los parámetros
    # name of the section in the configuration file that includes all simulation parameters
    PAR_SECTION = "Simulacion"
    # parámetro de duración de la simulación
    # simulation duration parameter
    PAR_DURATION = "duracion"
    # la cantidad de tiempo mímino detectada por el sistema
    # smallest amount of time the system can detect
    PAR_TIEMPOMINIMO = "tiempo-minimo"
    # .csv con información de los dispositivos
    # .csv file with information of the UE
    PAR_UE = "dispositivos"
    # .cvs con información de los eventos generados con el algoritmo CMMPP
    # .csv file with CMMPP events
    PAR_EVENTOS = "eventos"
    # Exponente de perdida de trayectoria
    # Path Loss Exponent
    PLExp = "PLE"
    # ancho de banda de subportadora
    # subchannel bandwith
    BW_subportadoraNBIoT = "BW-subportadoraNBIoT"
    # Potencia máxima de dispositivos URLLC
    # Pmax for URLLC devices
    PURLLC = "Pmax-URLLC"
    # Potencia máxima de dispositivos mMTC
    # Pmax for mMTC devices
    PmMTC = "Pmax-mMTC"
    # tamaño máximo de cluster
    # cluster max size
    k_max = "kmax"
    # radio de la célula
    # cell radius
    CELL_RADIO = "radio"

    def __init__(self):
        """
        Constructor inicializando el tiempo actual en 0 y las colas de eventos vacias.
        Constructor initializing current time to 0 and the queue of events to
        empty.
        """
        # tiempo actual de la simulación
        # current simulation time
        self.time = 0
        # cola de eventos, se implementa como una estructura heap
        # queue of events, implemented as a heap
        self.queue = []
        # lista de nodos, UE's y eNB
        # list of nodes, ue's and eNB
        self.nodes = []
        # lista de eventos que importaremos del archivo .csv
        # list of eventos imported from .csv
        self.eventos = []
        # esta lista registra todos los eventos y no solo los que se agregan al log
        # this list registers all events and not only the ones in the logs
        self.eventosaux=[]
        # lista de dispositivos a ser evaluados en el siguiente algoritmo NOMA
        # list of UE's to be evaluated in the next NOMA computing
        self.universoNOMA =[]
        # initialize() debe ser llamada antes de correr la simulación
        # initialize() should be called before running the simulation
        self.initialized = False
        # archivo de configuración
        # empty config file
        self.config_file = ""
        # sección dentro del archivo de configuración
        # empty section
        self.section = ""

    def set_config(self, config_file, section):
        """
        Establecer el archivo de configuración y la sección.
        Set config file and section.
        :param config_file: nombre del archivo de config. | file name of the config file
        :param section: la sección dentro del archivo | the section within the config file
        """
        self.config_file = config_file
        self.section = section
        # se crea una instancia del administrador de la configuración
        # instantiate config manager
        self.config = Config(self.config_file, self.section)


    def initialize(self, run_number):
        """
        Método para inicializar la simulación.
        Simulation initialization method.
        :param run_number: el índice de la simulación a correr | the index of the simulation to be run
        """
        if self.config_file == "" or self.section == "":
            print("Configuration error. Call set_config() before initialize()")
            sys.exit(1)
        # set and check run number
        self.run_number = run_number
        if run_number >= self.config.get_runs_count():
            print("Simulation error. Run number %d does not exist. Please run "
                  "the simulator with the --list option to list all possible "
                  "runs" % run_number)
            sys.exit(1)
        self.config.set_run_number(run_number)

        # instanciamos el logger de los eventos
        # instantiate data logger
        self.logger = Log(self.config.get_output_file())
        # obtenemos la duración de la simulación
        # get simulation duration
        self.duration = self.config.get_param(self.PAR_DURATION)
        # obtener el tiempo mínimo registrado por el simulador
        # get minimum time registered by the simulator
        self.tiempoMinimo = self.config.get_param(self.PAR_TIEMPOMINIMO)
        # radio de célula
        # cell radius
        self.radio_cell = self.config.get_param(self.CELL_RADIO)
        # exponente de pérdida por trayectoria
        # path loss exponent
        self.PLE = self.config.get_param(self.PLExp)
        # ancho de banda de subportadora
        # subcarrier bandwidth
        self.bwSubportNBIoT = self.config.get_param(self.BW_subportadoraNBIoT)
        # Potencia de ruido térmico
        self.potenciaRuidoTermico = 5.012e-21
        # Potencia de dispositivos URLLC
        self.pmaxURLLC = self.config.get_param(self.PURLLC)
        # Potencia de dispositivos mMTC
        self.pmaxmMTC = self.config.get_param(self.PmMTC)
        # tamaño máximo de cluster
        self.kmax = self.config.get_param(self.k_max)
        # se instancia el canal
        # instantiate the channel
        self.channel = Channel(self.config)
        # nombre del archivo que contiene los eventos
        # name of the files with the events
        self.eventosArchivo = self.config.get_param(self.PAR_EVENTOS)
        # Formato | Format
        # [0,0.02,7,Monitoreo de agua y electricidad,0,20.65,1] => [idalarma,tiempo,iddispositivo,tipodispositivo,tipoevento,tampaquete,modelotrafico]
        # se lee el archivo .csv y se guardan en la lista eventos
        # .csv file is saved into eventos list
        eventos_rec = pd.read_csv(self.eventosArchivo, index_col=0)
        self.eventos = eventos_rec.values.tolist()
        # nombre del archivo que contiene los dispositivos
        # name of the file conteining the UE's
        self.dispositivos = self.config.get_param(self.PAR_UE)
        # Formato  | Format
        #[1, Control de iluminacion, 7.776887288396965, 26.52437539236592] => [iddispositivo, tipodispositivo, posx, posy]
        # se lee el archivo .csv y se guardan en la lista dispositivosLista
        # .csv file is saved into dispositivosLista list
        dispositivos_rec = pd.read_csv(self.dispositivos, index_col=0)
        self.dispositivosLista= dispositivos_rec.values.tolist()
        # instanciamos todos los nodos incluyendo eNB
        # instantiate all the nodes starting by the eNB
        # creamos la estacion base como nodo 0
        # eNB is created as node 0
        self.node_eNB = Node(0, 'eNB', self.config, self.channel, 0, 0)
        # avisamos al canal de la existencia del nodo
        # let the channel know about this node
        #self.channel.register_node(self.node_eNB)
        # inicializamos enB y lo agregamos a la lista de nodos
        # eNB is initialized and added to nodes list
        self.node_eNB.initialize_eNB()
        self.nodes.append(self.node_eNB)
        # se crean los dispositivos
        # UE's are created
        for d in self.dispositivosLista:
            id= d[0]
            tipo= d[1]
            x = d[2]
            y = d[3]
            node = Node(id,tipo,self.config, self.channel, x, y)
            # inicializamos el nodo y lo agregamos a la lista de nodos
            # node is initialized and added to nodes list
            node.initialize()
            self.nodes.append(node)
        # hecho esto, la simulación puede iniciar
        # all done. simulation can start now
        self.initialized = True

    def run(self):
        """
        Corre la simulación.
        Runs the simulation.
        """
        # primero verifica que la simulación está inicializada antes
        # first check that everything is ready
        if not self.initialized:
            print("Cannot run the simulation. Call initialize() first")
            sys.exit(1)
        # se guarda el momento en el que la simulación inicio
        # save the time at which the simulation started, for statistical purpose
        start_time = time.time()
        # la última vez que se imprimio el porcentaje de la simulación
        # last time we printed the simulation percentage
        prev_time = start_time
        # se imprime el porcentaje por primera vez (0%)
        # print percentage for the first time (0%)
        self.print_percentage(True)
        # bucle de simulación principal
        # main simulation loop
        while self.time <= self.duration:
            # obtenemos el siguiente evento y se llama al método que se encarga de ese evento en el destino
            # get next event and call the handle method of the destination
            event = self.next_event()
            dst = event.get_destination()
            src = event.get_source()
            dst.handle_event(event, src)
            # obtenemos el tiempo actual
            # get current real time
            curr_time = time.time()
            # si más de un segundo ha pasdo, se actualiza la barra de porcenteje
            # if more than a second has elapsed, update the percentage bar
            if curr_time - prev_time >= 1:
                self.print_percentage(False)
                prev_time = curr_time
        # completada la simulación, se imprime el porcentaje por última vez (100%)
        # simulation completed, print the percentage for the last time (100%)
        self.print_percentage(False)
        # se calcula cúanto tiempo tomó la simulación
        # compute how much time the simulation took
        end_time = time.time()
        total_time = round(end_time - start_time)
        print("\nMaximum simulation time reached. Terminating.")
        print("Total simulation time: %d hours, %d minutes, %d seconds" %
              (total_time // 3600, total_time % 3600 // 60,
               total_time % 3600 % 60))
        self.logger.log_file.close()


#########################

    def schedule_event(self, event):
        """
        Calendariza un nuevo evento en la cola queue.
        Adds a new event to the queue of events
        :param event: el evento a calendarizar | the event to schedule.
        """
        if event.get_time() < self.time:
            print("Schedule error: Module with id %d of type %s is trying to "
                  "schedule an event in the past. Current time = %f, schedule "
                  "time = %f", (event.get_source.get_id(),
                                event.get_source.get_type(),
                                self.time,
                                event.get_time()))
            sys.exit(1)
        heapq.heappush(self.queue, event)

    def next_event(self):
        """
        Retorna el primer evento en la cola queue
        Returns the first event in the queue
        """
        try:
            event = heapq.heappop(self.queue)
            self.time = event.event_time
            return event
        except IndexError:
            print("No more events in the simulation queue. Terminating.")
            sys.exit(0)

    def cancel_event(self, event):
        """
        Elimina un evento calendarizado de la cola queue
        Deletes a scheduled event from the queue
        :param event: the event to be canceled
        """
        try:
            self.queue.remove(event)
            heapq.heapify(self.queue)
        except ValueError:
            print("Trying to delete an event that does not exist.")
            sys.exit(1)

    def print_percentage(self, first):
        # se regresa al inicio de la línea
        # go back to the beginning of the line
        if not first:
            sys.stdout.write('\r' + ERASE_LINE)
        # se calcula el porcentaje
        # compute percentage
        perc = min(100, int(math.floor(self.time / self.duration * 100)))
        # se imprime la barra de progreso
        # print progress bar, percentage, and current element
        sys.stdout.write("[%-20s] %d%% (time = %f, total time = %f)" %
                         ('=' * (perc // 5), perc, self.time, self.duration))
        sys.stdout.flush()

    def get_runs_count(self):
        """
        Retorna el número de corridas para el archivo de configuración y sección dados
        Returns the number of runs for the given config file and section
        :returs: the total number of runs
        """
        if self.config_file == "" or self.section == "":
            print("Configuration error. Call set_config() before "
                  "get_runs_count()")
            sys.exit(1)
        return self.config.get_runs_count()

    def get_logger(self):
        """
        Retorna el módulo que que crea logs de los eventos.
        Returns the data logger to modules.
        """
        return self.logger

    def get_time(self):
        """
        Retorna el tiempo actual de la simulación.
        Returns current simulation time.
        """
        return self.time

    def get_params(self, run_number):
        """
        Retorna una representación textual de los parámetros de la simualción dados
        para un número de corrida (run).
        Returns a textual representation of simulation parameters for a given
        run number.
        :param run_number: el número de corrida | the run number
        :returns: representación textual del parámetro| textual representation of parameters for run_number
        """
        return self.config.get_params(run_number)

    # def algoritmo_RA(self):
    #     """
    #     Algoritmo para computar el resultado del RA.
    #     Returns the result of the Random Access.
    #     """
    #     preambulos=len(self.universoNPRACH)
    #     #throughput = int(np.random.uniform(0, preambulos, 1))
    #     if preambulos==0:
    #         throughput=0
    #     else:
    #         throughput = self.RAmaxthroughput[preambulos-1][1]
    #
    #     # calculamos aleatoriamente qué dispositivos del universo no completaron su RA
    #     # we compute the preambles that didn't pass the RA
    #     random.shuffle(self.universoNPRACH)
    #     universoNPRACHaux= self.universoNPRACH[:(preambulos-throughput)]
    #
    #     for evento in universoNPRACHaux:
    #         self.cancel_event(evento)
    #         evento.get_source().current_pkt=None
    #         evento.get_source().state=Node.IDLE
    #         # schedule next arrival
    #         evento.get_source().schedule_next_arrival()
    #
    #     assert (len(universoNPRACHaux)+throughput==preambulos)
    #     self.universoNPRACH = []
    #     return throughput