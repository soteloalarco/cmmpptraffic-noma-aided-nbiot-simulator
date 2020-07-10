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

import math
from des.module import Module
from des.event import Event
from des.events import Events
from noma.clases.simulacion import Simulacion
from noma.clases.nbIoT import NB_IoT
from noma.funciones.funcionDispositivo import creardispositivosDES
from noma.clases.grupoNOMA import GrupoNOMA

# TODO tal vez sea necesario generar los 48 canales

class Channel(Module):
    """
    Esta clase se encarga de simular el canal.
    This class takes care of simulating the channel, signaling the beginning of
    reception to nodes within the communication range. For the sake of
    simplicity, the end of reception is automatically scheduled by the receiving
    node.
    """

    # velocidad de la luz
    # speed of light in m/s, used to compute propagation delay
    SOL = 299792458.0

    def __init__(self, config):
        """
        Constructor.
        Constructor.
        :param config: the set of configs loaded by the simulator to obtain, for
        example, the communication range. The parameter is an instance of the
        Config class
        """
        # call superclass constructor
        Module.__init__(self,-1,'canal')

        # lista de los  nodos comunicandose
        # list of all communication nodes in the simulation
        self.nodes = []
        self.universomMTC = []
        self.universoURLLC = []


    def register_node(self, node):
        """
        Registrar un nodo participando en la simulación.
        Registers a node participating to the simulation. This way the channel
        knows who is participating and can notify them when transmissions start
        or end
        :param node: the node to register, an instance of the Node class
        """
        self.nodes.append(node)
        # recompute the neighbors of all nodes considering the new node as well
        #self.recompute_neighbors(node)

    def distance(self, a, b):
        """
        Calcula la distancia en euclidiana en dos dimensiones entre los nodos a y b
        Computes the two-dimensional Euclidean distance between nodes a and b
        :param a: first node
        :param b: second node
        """
        return math.sqrt(math.pow(a.get_posx() - b.get_posx(), 2) +
                         math.pow(a.get_posy() - b.get_posy(), 2))


    def start_transmission(self, source_node, packet=None):
        """
        Begins transmission of a frame on the channel, notifying all neighbors
        about such event
        :param source_node: node that starts the transmission
        :param packet: packet being transmitted
        """
        #TODO agregar a lista de nodos en el canal para hacer noma posteriormente
        #nosotros no avisamos a vecinos por eso está comentado, pero aqui tal vez deba ir la base
        # avisamos al canal de la existencia del nodo
        # let the channel know about this node
        self.register_node(source_node)
        # for neighbor in self.neighbors[source_node.get_id()]:
        #     # compute propagation delay: distance / speed of light
        #     propagation_delay = self.distance(source_node, neighbor) /\
        #                         Channel.SOL
        #     # generate and schedule START_RX event at receiver
        #     # be sure to make a copy of the packet and not pass the same
        #     # reference to multiple nodes, as they will process the packet in
        #     # different ways. one node might be able to receive it, one node
        #     # might not
        #     event = Event(self.sim.get_time() + propagation_delay,
        #                   Events.START_RX, neighbor, source_node,
        #                   copy.deepcopy(packet))
        #     self.sim.schedule_event(event)

    def algoritmo_NOMA(self,enb):

        self.universomMTC=[]
        self.universoURLLC=[]

        for nodo in self.nodes:

            if(nodo.get_tipo()=='Dispositivos URLLC'):
                self.universoURLLC.append(nodo)
            else:
                self.universomMTC.append(nodo)
        enb.logger.log_inicio_NOMA(enb)

        # TODO algoritmo noma que resultará en algunos dispositivos que no pudieron ser atendidos y tasas para los demas
        self.noma()

        #actulizamos los dispositivos que transmitiran
        for nodo in self.nodes:

            if(nodo.evento_end_tx is None):
                nueva_tasa=20
                nodo.tasa_tx=nueva_tasa
                nodo.ultimo_proc_noma=self.sim.get_time()
                nodo.paquete_restante = nodo.current_pkt.get_size()
                tiempo_end_tx= self.sim.get_time() + (nodo.paquete_restante/ nodo.tasa_tx)
                nodo.evento_end_tx = Event(tiempo_end_tx, Events.END_TX, nodo,
                               nodo, nodo.current_pkt)
            else:
                self.sim.cancel_event(nodo.evento_end_tx)
                nueva_tasa = 20
                tiempo_entre_noma = self.sim.get_time() - nodo.ultimo_proc_noma
                nodo.paquete_restante = nodo.paquete_restante - ( nodo.tasa_tx * tiempo_entre_noma)
                tiempo_end_tx = self.sim.get_time() + (nodo.paquete_restante / nueva_tasa)
                nodo.evento_end_tx = Event(tiempo_end_tx, Events.END_TX, nodo,
                               nodo, nodo.current_pkt)
                nodo.tasa_tx = nueva_tasa
                nodo.ultimo_proc_noma = self.sim.get_time()

            nodo.transmit_packet()

    def noma(self):

        # Variables de entrada
        RadioCelular = self.sim.radio_cell  # Modelo válido en distancias sin LoS en [61-1238] y con LoS en [60-930]
        PLE = self.sim.PLE  # 2.9 con NloS y con LoS usar 2.0
        BW_subportadoraNBIoT = self.sim.bwSubportNBIoT
        Potencia_ruidoTermico = self.sim.potenciaRuidoTermico

        NumDispositivosURLLC = len(self.universoURLLC)
        NumDispositivosMTC = len(self.universomMTC)
        Pmax_URLLC = self.sim.pmaxURLLC  # Siempre en Clase 23dBm (.2)
        Pmax_MTC = self.sim.pmaxmMTC  # Pueden ser Clase 23dBm (.2), 20dBm (.1) o 14dBm (0.025)
        kmax = self.sim.kmax

        # Regla 1
        Num_Total_Dispositivos = NumDispositivosURLLC + NumDispositivosMTC
        if Num_Total_Dispositivos < 48:
            Numero_clusters = Num_Total_Dispositivos
        else:
            Numero_clusters = 48

        # Creación de Objetos para la simulación
        DESsim = Simulacion(0, PLE, RadioCelular)
        NBIoT = NB_IoT(48, [], [], [], [], Numero_clusters, [], int(NumDispositivosURLLC), [], int(NumDispositivosMTC),
                       [], 0, [], kmax, BW_subportadoraNBIoT, Potencia_ruidoTermico)
        # Creacion de Dispositivos URLLC
        NBIoT.U.append(creardispositivosDES(self.universoURLLC, 1, DESsim.PLE, DESsim.r_cell, NBIoT.numS, Pmax_URLLC))
        # Creacion de Dispositivos mMTC
        NBIoT.M.append(creardispositivosDES(self.universomMTC, 2, DESsim.PLE, DESsim.r_cell, NBIoT.numS, Pmax_MTC))

        def AlgoritmoAgrupacionNOMA():
            # Se empiezan a agrupar usuarios con una alta ganancia de canal promedio,
            # en la recepción tipo SIC se decodifican primero los usuarios con una alta ganancia de canal promedio antes que los de baja ganancia  de canal promedio
            # Los rangos de los dispositivos uRLLC deben ser menores que los MTC para que sea eficiente la decodificación SIC

            # indices que indican cual es la última posición de asignación de usuarios URLLC
            indicePos1Grupo = 0
            indicePos2Grupo = 0

            # AGRUPAMIENTO DE USUARIOS URLLC
            # Solo para grupos de 4 usuarios
            for deviceURLLC in range(0, int(NBIoT.numU)):
                # deviceURLLC corresponde al número de dispositivos uRLLC [U]
                if deviceURLLC < NBIoT.numC:
                    # Asignar los dispositivos uRLLC a rangos bajos de los primeros grupos
                    NBIoT.C.append(GrupoNOMA(deviceURLLC, [], 0, 1, [], False))
                    NBIoT.C[deviceURLLC].dispositivos.append(
                        [NBIoT.U[0][deviceURLLC], False, False, False, False, False])

                    # guardamos el numero de cluster en el nodo
                    NBIoT.U[0][deviceURLLC].nodo.cluster=deviceURLLC

                    NBIoT.U[0][deviceURLLC].alphabeta = 1
                    indicePos1Grupo = indicePos1Grupo + 1
                    if (indicePos1Grupo == NBIoT.numC) and (NBIoT.kmax == 1):
                        return 0

                # Validación de que si el agrupamiento es de 2 entonces solo se asignarán al rango 1
                elif deviceURLLC < 2 * NBIoT.numC:
                    # Si el número de dispositivos uRLLC [U] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
                    # serán asignados a los siguientes rangos del grupo
                    NBIoT.C[indicePos2Grupo].dispositivos[0][1] = NBIoT.U[0][deviceURLLC]

                    # guardamos el numero de cluster en el nodo
                    NBIoT.U[0][deviceURLLC].nodo.cluster = indicePos2Grupo

                    NBIoT.U[0][deviceURLLC].alphabeta = 1
                    indicePos2Grupo = indicePos2Grupo + 1

                    if (indicePos2Grupo == NBIoT.numC) and (NBIoT.kmax == 2):
                        return 0
                else:
                    # Solo se podrán asignar dispositivos URLLC hasta el segundo rango  de cada cluster
                    # print('Se asignaron',deviceURLLC, 'usuarios URLLC pero eran ', NBIoT.numU, ' usuarios MTC' )
                    break

            # Se checa en que cluster se quedó asignado el ultimo dispositivo URLLC
            if indicePos2Grupo != 0:
                indiceAsignacionCluster = indicePos2Grupo
                cerosEliminar = indicePos2Grupo
                # k _= es una variable que indica en que rango se quedó asignado el ultimo dispositivo URLLC
                k_ = 1
                if indicePos2Grupo == NBIoT.numC:  ####
                    indiceAsignacionCluster = 0
                    cerosEliminar = 0
                    k_ = 2
            else:
                indiceAsignacionCluster = indicePos1Grupo
                cerosEliminar = indicePos1Grupo
                k_ = 0

                if indiceAsignacionCluster != NBIoT.numC:
                    for cn in range(indiceAsignacionCluster, int(NBIoT.numC)):
                        NBIoT.C.append(GrupoNOMA(cn, [], 0, 1, [], False))
                        NBIoT.C[cn].dispositivos.append([False, False, False, False, False, False])
                else:
                    indiceAsignacionCluster = 0
                    cerosEliminar = 0
                    k_ = 1

            # Agregar ceros a lista de usuarios MTC para que se empiezen a agrupar desde esa posición
            for g in range(0, indiceAsignacionCluster):
                NBIoT.M[0].insert(0, 0)

            # AGRUPAMIENTO DE USUARIOS mMTC
            for deviceMTC in range(indiceAsignacionCluster, len(NBIoT.M[0])):
                # Si el número de dispositivos mMTC [M] es mayor que el numero de grupos NOMA [C], los dispositivos sobrantes
                # serán asignados a los siguientes rangos del grupo, última posición de asignación

                # Asignar los dispositivos mmtc a los rangos mas bajos de los primeros grupos
                NBIoT.C[indiceAsignacionCluster].dispositivos[0][k_] = NBIoT.M[0][deviceMTC]

                # guardamos el numero de cluster en el nodo
                NBIoT.M[0][deviceMTC].nodo.cluster = indiceAsignacionCluster

                NBIoT.M[0][deviceMTC].alphabeta = 1
                indiceAsignacionCluster = indiceAsignacionCluster + 1

                if indiceAsignacionCluster == (NBIoT.numC):
                    k_ = k_ + 1
                    indiceAsignacionCluster = 0
                    if k_ == NBIoT.kmax:
                        # print('Se asignaron',deviceMTC, 'usuarios MTC pero eran ', NBIoT.numM, ' usuarios MTC' )
                        break

            # Eliminar ceros que se agregaron a lista
            del NBIoT.M[0][0:cerosEliminar]

        AlgoritmoAgrupacionNOMA()
        #AlgoritmoAsignacionRecursos()

