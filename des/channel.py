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
import math as mth
import copy
from des.module import Module
from des.event import Event
from des.events import Events
from noma.clases.simulacion import Simulacion
from noma.clases.nbIoT import NB_IoT
from noma.funciones.funcionDispositivo import creardispositivosDES
from noma.clases.grupoNOMA import GrupoNOMA
from noma.clases.subportadora import  Subportadora
import numpy as np

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
        self.numeroSubportadoras = 48
        self.subcarriers = np.linspace(2000e6, 2000180000,self.numeroSubportadoras)  # 48 subportadoras en frecuencia de 2Ghz
        # cola de dispositivos con paquetes
        self.dispConCluster = []
        # lita de disp con tasas satisfechas a la hora de hacer noma
        self.mMTC_tasanocubierta = []
        self.URLLC_tasanocubierta = []


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
        self.dispConCluster=[]

        for nodo in self.nodes:

            if(nodo.get_tipo()=='Dispositivos URLLC'):
                self.universoURLLC.append(nodo)
            else:
                self.universomMTC.append(nodo)
        enb.logger.log_inicio_NOMA(enb)

        self.noma()

        #actulizamos los dispositivos que transmitiran
        for nodo in self.nodes:
            if (nodo in self.dispConCluster):
                if(nodo.evento_end_tx is None):
                    nueva_tasa= nodo.nueva_tasa_tx
                    nodo.tasa_tx=nueva_tasa
                    nodo.ultimo_proc_noma=self.sim.get_time()
                    nodo.paquete_restante = nodo.current_pkt.get_size()
                    tiempo_end_tx= self.sim.get_time() + (nodo.paquete_restante/ (nodo.tasa_tx))
                    nodo.evento_end_tx = Event(tiempo_end_tx, Events.END_TX, nodo,
                                   nodo, nodo.current_pkt)
                    nodo.nueva_tasa_tx = 0
                else:
                    self.sim.cancel_event(nodo.evento_end_tx)
                    nueva_tasa = nodo.nueva_tasa_tx
                    tiempo_entre_noma = self.sim.get_time() - nodo.ultimo_proc_noma
                    nodo.paquete_restante = nodo.paquete_restante - ( (nodo.tasa_tx)  * tiempo_entre_noma)
                    tiempo_end_tx = self.sim.get_time() + (nodo.paquete_restante / (nueva_tasa))
                    nodo.evento_end_tx = Event(tiempo_end_tx, Events.END_TX, nodo,
                                   nodo, nodo.current_pkt)
                    nodo.tasa_tx = nueva_tasa
                    nodo.ultimo_proc_noma = self.sim.get_time()
                    nodo.nueva_tasa_tx = 0

                nodo.transmit_packet()
            else: #si el dispossitivo no alcanzo cluster
                if (nodo.evento_end_tx is None): # si recien comienza a transmitir
                    self.sim.bloqueoSinCluster.append([self.sim.get_time(),nodo.get_id(),nodo.get_tipo(),nodo.current_pkt.get_size(),0])
                else: # si ya había transmitido durante algun tiempo
                    self.sim.cancel_event(nodo.evento_end_tx)

                    tiempo_entre_noma = self.sim.get_time() - nodo.ultimo_proc_noma
                    nodo.paquete_restante = nodo.paquete_restante - ((nodo.tasa_tx) * tiempo_entre_noma)

                    self.sim.bloqueoSinCluster.append([self.sim.get_time(),nodo.get_id(),nodo.get_tipo(),nodo.current_pkt.get_size(),nodo.current_pkt.get_size()-nodo.paquete_restante])

                nodo.end_transmit_packet()

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
        assert(Num_Total_Dispositivos >0)
        if Num_Total_Dispositivos < self.numeroSubportadoras:
            Numero_clusters = Num_Total_Dispositivos
        else:
            Numero_clusters = self.numeroSubportadoras

        # Creación de Objetos para la simulación
        DESsim = Simulacion(0, PLE, RadioCelular)
        NBIoT = NB_IoT(48, [], [], [], [], Numero_clusters, [], int(NumDispositivosURLLC), [], int(NumDispositivosMTC),
                       [], 0, [], kmax, BW_subportadoraNBIoT, Potencia_ruidoTermico)
        # Creacion de Dispositivos URLLC
        NBIoT.U.append(creardispositivosDES(self.universoURLLC, 1, DESsim.PLE, DESsim.r_cell, NBIoT.numS, Pmax_URLLC))
        # Creacion de Dispositivos mMTC
        NBIoT.M.append(creardispositivosDES(self.universomMTC, 2, DESsim.PLE, DESsim.r_cell, NBIoT.numS, Pmax_MTC))

        def AlgoritmoAgrupacionNOMA(sim):
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
                    sim.nodes[NBIoT.U[0][deviceURLLC].id].cluster=deviceURLLC
                    sim.channel.dispConCluster.append(sim.nodes[NBIoT.U[0][deviceURLLC].id])

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
                    sim.nodes[NBIoT.U[0][deviceURLLC].id].cluster = indicePos2Grupo
                    sim.channel.dispConCluster.append(sim.nodes[NBIoT.U[0][deviceURLLC].id])

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
                sim.nodes[NBIoT.M[0][deviceMTC].id].cluster = indiceAsignacionCluster
                sim.channel.dispConCluster.append(sim.nodes[NBIoT.M[0][deviceMTC].id])

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

        def AlgoritmoAsignacionRecursos(sim):
            # Conjunto de clusters de dispositivos con tasas insatisfechas
            NBIoT.Cns = copy.deepcopy(NBIoT.C)

            # Creacion de Subportadoras NB_IoT cada una con 48 grupos NOMA
            for s in range(0, NBIoT.numS):
                NBIoT.S.append(Subportadora(s, [], 0, []))

            # Inicio del bucle del algoritmo de asignación de recursos
            while True:
                # Validación de todas las tasas de los usuarios y que las subportadoras se hayan asignado
                if ((NBIoT.S == []) and (NBIoT.Cns == [])):
                    break
                NBIoT.numS = len(NBIoT.S)

                # ---------------------------------------------------PRIMERA PARTE DEL ALGORITMO----------------------------------------------------

                # For para recorrer todas las subportadoras disponibles
                for subportadora in range(0, NBIoT.numS):
                    NBIoT.S[subportadora].c_ = []
                    NBIoT.Sv = []
                    # Validacion para ver si hay aún clusters sin asignar
                    if NBIoT.Cns == []:
                        break
                    NBIoT.numC = len(NBIoT.Cns)
                    # For para recorrer los grupos NOMA no satisfechos (Cns)
                    for cluster in range(0, NBIoT.numC):
                        # Inicilalización a cero de las tasas totales de cada cluster
                        NBIoT.Cns[cluster].RTotal = 0

                        # For para recorrer todos los rangos del grupo NOMA
                        for device in range(0, NBIoT.kmax):
                            # Validación de que algun rango del cluster está vacio o desocupado
                            if NBIoT.Cns[cluster].dispositivos[0][device] != False:
                                Interferencias = calculoInterferencia(NBIoT.Cns, subportadora, cluster, device)
                                R = calculoTasaTx(Interferencias, NBIoT.Cns, subportadora, cluster, device)
                                # Se asigna la tasa lograda a dispositivo
                                NBIoT.Cns[cluster].dispositivos[0][device].Rx = R
                                NBIoT.Cns[cluster].RTotal = NBIoT.Cns[cluster].RTotal + R

                    # Grupo NOMA que maximiza la tasa
                    NBIoT.S[subportadora].c_ = busquedaMejorGrupoNOMA(NBIoT.Cns)

                    # Se busca en la lista Cns el grupo NOMA que maximiza la tasa
                    ID_cluster_c = busquedaID(NBIoT.Cns, NBIoT.S[subportadora].c_)

                    # Actualizar lista de subportadoras asignadas al cluster Sac
                    NBIoT.Cns[ID_cluster_c].Sac.append(NBIoT.S[subportadora].id)

                    Sac = len(NBIoT.Cns[ID_cluster_c].Sac)

                    # S^ para tener registro de las s que quedan
                    NBIoT.Sv.append(NBIoT.S[subportadora].id)

                    # Actualización de Tasas del mejor grupo NOMA
                    # Inicializar Rs
                    if (Sac == 1):
                        NBIoT.Cns = actualizacionTasascDES_(NBIoT.Cns, ID_cluster_c, sim)

                    else:
                        for device in range(0, NBIoT.kmax):
                            if NBIoT.Cns[ID_cluster_c].dispositivos[0][device] != False:
                                NBIoT.Cns[ID_cluster_c].dispositivos[0][device].Rs = 0

                        for carrier in range(0, Sac):
                            if carrier == Sac - 1:
                                NBIoT.Cns = actualizacionPotenciasc_(NBIoT.Cns, ID_cluster_c, NBIoT.S[subportadora].id,
                                                                     Sac - 1)
                            for device in range(0, NBIoT.kmax):
                                # Validación de que algun rango del cluster está vacio o desocupado
                                if NBIoT.Cns[ID_cluster_c].dispositivos[0][device] != False:
                                    Interferencias = calculoInterferencia(NBIoT.Cns,
                                                                          NBIoT.Cns[ID_cluster_c].Sac[carrier],
                                                                          ID_cluster_c, device)
                                    R = calculoTasaTx(Interferencias, NBIoT.Cns, NBIoT.Cns[ID_cluster_c].Sac[carrier],
                                                      ID_cluster_c, device)
                                    NBIoT.Cns[ID_cluster_c].dispositivos[0][device].Rx = R
                            NBIoT.Cns = actualizacionTasascDES_(NBIoT.Cns, ID_cluster_c, sim)

                    for carrier in range(0, Sac):
                        # Actualización de Potencias del mejor grupo NOMA
                        NBIoT.Cns = actualizacionPotenciasc_(NBIoT.Cns, ID_cluster_c,
                                                             NBIoT.Cns[ID_cluster_c].Sac[carrier], Sac)

                    # Validación del cumplimiento de tasas del mejor grupo NOMA c_ (c*)
                    condicion = validacionTasas(NBIoT.Cns, ID_cluster_c)
                    if condicion == True:
                        NBIoT.Cns[ID_cluster_c].tasasSatisfechas = True

                    # Retribución de subportadora a cluster de acuerdo con c* en caso de que se cumplan los umbrales de las tasas
                    if Sac == 1:
                        # Asignacion de s y c por medio de sus ids en lista Agrupaciones
                        NBIoT.Agrupaciones.append(NBIoT.Cns[ID_cluster_c])
                        # Asignación de grupo NOMA Cns
                        NBIoT.Cns[ID_cluster_c] = 0
                        # Quitar a  c_ de los cluters que no han cumplido su tasa Cns
                        # Limpiar Lista de Cns ya asignadas
                        for clus in range(0, len(NBIoT.Cns)):
                            if NBIoT.Cns[clus] == 0:
                                del NBIoT.Cns[clus]
                                break

                    # Asignación de subportadora s
                    NBIoT.S[subportadora] = 0

                # Limpiar Lista de Subportadoras ya asignadas
                sub = 0
                numS = len(NBIoT.S)
                while sub < numS:
                    if NBIoT.S[sub] == 0:
                        del NBIoT.S[sub]
                        numS -= 1
                    else:
                        sub += 1

                usuariosSatisfechos(NBIoT.Agrupaciones)
                #print("Subportadoras restantes:", len(NBIoT.S))
                # ---------------------------------------------------SEGUNDA PARTE DEL ALGORITMO----------------------------------------------------

                # Asignación de las subportadoras restantes
                # Validación si todas las tasas de los usuarios C se han cumplido
                if (NBIoT.Cns == []):
                    NBIoT.numS = len(NBIoT.S)
                    # For para recorrer todas las subportadoras disponibles
                    for subportadora in range(0, NBIoT.numS):
                        NBIoT.S[subportadora].c_ = []
                        NBIoT.Sv = []
                        NBIoT.numC = len(NBIoT.Agrupaciones)

                        # For para recorrer los grupos NOMA
                        for cluster in range(0, NBIoT.numC):
                            # Inicilalización a cero de las tasas totales de cada cluster
                            NBIoT.Agrupaciones[cluster].RTotal = 0
                            if NBIoT.Agrupaciones[cluster].tasasSatisfechas == False:
                                # For para recorrer todos los rangos del grupo NOMA
                                for device in range(0, NBIoT.kmax):
                                    # Validación de que algun rango del cluster está vacio o desocupado
                                    if NBIoT.Agrupaciones[cluster].dispositivos[0][device] != False:
                                        Interferencias = calculoInterferencia(NBIoT.Agrupaciones, subportadora, cluster,
                                                                              device)
                                        R = calculoTasaTx(Interferencias, NBIoT.Agrupaciones, subportadora, cluster,
                                                          device)
                                        # Se asigna la tasa lograda a dispositivo
                                        NBIoT.Agrupaciones[cluster].dispositivos[0][device].Rx = R


                                        NBIoT.Agrupaciones[cluster].RTotal = NBIoT.Agrupaciones[cluster].RTotal + R

                        # Grupo NOMA que maximiza la tasa
                        NBIoT.S[subportadora].c_ = busquedaMejorGrupoNOMA(NBIoT.Agrupaciones)

                        # Se busca en la lista el grupo NOMA que maximiza la tasa
                        ID_cluster_c = busquedaID(NBIoT.Agrupaciones, NBIoT.S[subportadora].c_)

                        # Actualizar lista de subportadoras asignadas al cluster Sac
                        NBIoT.Agrupaciones[ID_cluster_c].Sac.append(NBIoT.S[subportadora].id)

                        Sac = len(NBIoT.Agrupaciones[ID_cluster_c].Sac)

                        # S^ para tener registro de las s que quedan
                        NBIoT.Sv.append(NBIoT.S[subportadora].id)

                        # Actualización de Tasas del mejor grupo NOMA
                        # Inicializar Rs
                        if (Sac == 1):
                            NBIoT.Agrupaciones = actualizacionTasascDES_(NBIoT.Agrupaciones, ID_cluster_c, sim)

                        else:
                            for device in range(0, NBIoT.kmax):
                                if NBIoT.Agrupaciones[ID_cluster_c].dispositivos[0][device] != False:
                                    NBIoT.Agrupaciones[ID_cluster_c].dispositivos[0][device].Rs = 0

                            for carrier in range(0, Sac):
                                if carrier == Sac - 1:
                                    NBIoT.Agrupaciones = actualizacionPotenciasc_(NBIoT.Agrupaciones, ID_cluster_c,
                                                                                  NBIoT.S[subportadora].id, Sac - 1)
                                for device in range(0, NBIoT.kmax):
                                    # Validación de que algun rango del cluster está vacio o desocupado
                                    if NBIoT.Agrupaciones[ID_cluster_c].dispositivos[0][device] != False:
                                        Interferencias = calculoInterferencia(NBIoT.Agrupaciones,
                                                                              NBIoT.Agrupaciones[ID_cluster_c].Sac[
                                                                                  carrier], ID_cluster_c, device)
                                        R = calculoTasaTx(Interferencias, NBIoT.Agrupaciones,
                                                          NBIoT.Agrupaciones[ID_cluster_c].Sac[carrier], ID_cluster_c,
                                                          device)
                                        NBIoT.Agrupaciones[ID_cluster_c].dispositivos[0][device].Rx = R
                                NBIoT.Agrupaciones = actualizacionTasascDES_(NBIoT.Agrupaciones, ID_cluster_c, sim)

                        for carrier in range(0, Sac):
                            # Actualización de Potencias del mejor grupo NOMA
                            NBIoT.Agrupaciones = actualizacionPotenciasc_(NBIoT.Agrupaciones, ID_cluster_c,
                                                                          NBIoT.Agrupaciones[ID_cluster_c].Sac[carrier],
                                                                          Sac)

                        # Validación del cumplimiento de tasas del mejor grupo NOMA c_ (c*)
                        condicion = validacionTasas(NBIoT.Agrupaciones, ID_cluster_c)
                        if condicion == True:
                            NBIoT.Agrupaciones[ID_cluster_c].tasasSatisfechas = True

                        # Asignación de subportadora s
                        NBIoT.S[subportadora] = 0

                    # Limpiar Lista de Subportadoras ya asignadas
                    sub = 0
                    numS = len(NBIoT.S)
                    while sub < numS:
                        if NBIoT.S[sub] == 0:
                            del NBIoT.S[sub]
                            numS -= 1
                        else:
                            sub += 1

                    # print("Subportadoras:", len(NBIoT.S))
                usuariosSatisfechos(NBIoT.Agrupaciones)

        # ++++++++++++++++++++++++++++++Funciones que se utilizan en algoritmo de asignación de recursos++++++++++++++++++++++++++++++++

        # Calcula la Interferencia de los dispositivos del grupo NOMA para un dispositivo
        def calculoInterferencia(ListaClusters, subportadora, cluster, device):
            Interference = 0
            # Se buscan dispositivos del mimsmo grupo pero con rangos superiores para calcular su contribución de interferencia
            for disp in range(device + 1, NBIoT.kmax):
                # Validación de que algun rango del cluster está vacio o desocupado
                if ListaClusters[cluster].dispositivos[0][disp] != False:
                    I = (abs(ListaClusters[cluster].dispositivos[0][disp].h[subportadora]) ** 2) * (
                    ListaClusters[cluster].dispositivos[0][disp].Px[subportadora])
                    Interference = Interference + I
            return Interference

        # Calcula las tasas de transmisión para un dispositivo
        def calculoTasaTx(Interferencias, ListaClusters, subportadora, cluster, device):
            return NBIoT.BW * mth.log2(1 + (((abs(
                ListaClusters[cluster].dispositivos[0][device].h[subportadora]) ** 2) * (
                                             ListaClusters[cluster].dispositivos[0][device].Px[subportadora])) / (
                                                        (NBIoT.No * NBIoT.BW) + Interferencias)))

        # La optimización del algoritmo es de acuerdo con el grupo NOMA que maximize la tasa de transmisión
        # Esta función busca el mejor grupo NOMA, es decir, el que maximize la tasa con base en las tasas que logra cada cluster (Rtotal)
        def busquedaMejorGrupoNOMA(ListaClusters):
            buscargrupo = max(GrupoNOMA.RTotal for GrupoNOMA in ListaClusters)
            for cluster in range(0, NBIoT.numC):
                # Se busca el identificador del mejor grupo
                if ListaClusters[cluster].RTotal == buscargrupo:
                    break
            return ListaClusters[cluster].id

        # Como la lista Cns es dinámica los indices van a ir cambiendo por lo que el id no correspondrá con el indice por eso se busca su id
        def busquedaID(ListaClusters, ID):
            for cluster in range(0, len(ListaClusters)):
                # Se busca el identificador del cluster
                if ListaClusters[cluster].id == ID:
                    break
            return cluster

        # Como la lista S es dinámica los indices van a ir cambiendo por lo que el id no correspondrá con el indice por eso se busca su id
        def busquedaIDSub(ListaSubportadoras, ID):
            for subportadora in range(0, len(ListaSubportadoras)):
                # Se busca el identificador de la subportadora
                if ListaSubportadoras[subportadora].id == ID:
                    break
            return subportadora

        # Se actualizan las tasas de los dispositivos de acuerdo
        def actualizacionTasascDES_(ListaClusters, cluster, sim):
            for device in range(0, NBIoT.kmax):
                # Validación de que algun rango del cluster está vacio o desocupado
                if ListaClusters[cluster].dispositivos[0][device] != False:
                    # Rx va ir cambiando en cada dispositivo entonces por eso se crea un nuevo campo Rs que indica la suma acumulada por subportadora
                    ListaClusters[cluster].dispositivos[0][device].Rs = ListaClusters[cluster].dispositivos[0][
                                                                            device].Rs + \
                                                                        ListaClusters[cluster].dispositivos[0][
                                                                            device].Rx
                    # se guarda la tasa en la simulación
                    sim.nodes[ListaClusters[cluster].dispositivos[0][device].id].nueva_tasa_tx = (ListaClusters[cluster].dispositivos[0][device].Rs /8)
            return ListaClusters

        # Función que actualiza las potencias de los dispositivos de un determinado cluster de acuerdo con Sac
        def actualizacionPotenciasc_(ListaClusters, cluster, subportadora, Sac):
            for device in range(0, NBIoT.kmax):
                # Validación de que algun rango del cluster está vacio o desocupado
                if ListaClusters[cluster].dispositivos[0][device] != False:
                    if ListaClusters[cluster].dispositivos[0][device].tipo == 1:
                        for sub in range(0, 48):
                            # ListaClusters[cluster].dispositivos[0][device].Px[subportadora] = (0.2/(device+1)) / ( Sac + 1)
                            ListaClusters[cluster].dispositivos[0][device].Px[sub] = Pmax_URLLC / (Sac + 1)
                    elif ListaClusters[cluster].dispositivos[0][device].tipo == 2:
                        for sub in range(0, 48):
                            # ListaClusters[cluster].dispositivos[0][device].Px[subportadora] = (0.2/(device+1)) / ( Sac + 1)
                            ListaClusters[cluster].dispositivos[0][device].Px[sub] = Pmax_MTC / (Sac + 1)
            return ListaClusters

        # Función que checa que las tasas de los dispositivos sean satisfacidas
        def validacionTasas(ListaClusters, cluster):
            for device in range(0, NBIoT.kmax):
                # Validación de que algun rango del cluster está vacio o desocupado
                if ListaClusters[cluster].dispositivos[0][device] != False:
                    if (ListaClusters[cluster].dispositivos[0][device].Rs) < (
                    ListaClusters[cluster].dispositivos[0][device].Rth):
                        return False
            return True

        # Funcion que calcula cuantos usuarios alcanzaron su tasa
        def usuariosSatisfechos(ListaClusters):
            contadorUsuarios = 0
            contadorU = 0
            contadorM = 0
            sumRate = 0
            for cluster in range(0, len(ListaClusters)):
                if ListaClusters[cluster].Sac:
                    for device in range(0, NBIoT.kmax):
                        # Validación de que algun rango del cluster está vacio o desocupado
                        if ListaClusters[cluster].dispositivos[0][device] != False:
                            if (ListaClusters[cluster].dispositivos[0][device].Rs) >= (
                            ListaClusters[cluster].dispositivos[0][device].Rth):
                                contadorUsuarios = contadorUsuarios + 1
                                sumRate = sumRate + ListaClusters[cluster].dispositivos[0][device].Rs
                                if ListaClusters[cluster].dispositivos[0][device].tipo == 1:
                                    contadorU = contadorU + 1
                                else:
                                    contadorM = contadorM + 1

            #print("Usuarios con tasas satisfechas: ", contadorUsuarios, " URLLC: ", contadorU, " MTC: ", contadorM,
            #      " Sum Rate: ", sumRate)

        AlgoritmoAgrupacionNOMA(self.sim)
        AlgoritmoAsignacionRecursos(self.sim)

