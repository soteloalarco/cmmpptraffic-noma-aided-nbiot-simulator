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

from des import sim
from des.packet import Packet


class Log:
    """
    Define las utilidades para crear logs de datos
    Defines data logging utilities
    """

    # paquete que ha sido recibido recientemente
    # packet has been correctly received
    LOG_RECEIVED = Packet.PKT_RECEIVED
    # paquete que ha sido corrupto debido a, por ejemplo, una colisión
    # packet has been corrupted due to, for example, a collision
    LOG_CORRUPTED = Packet.PKT_CORRUPTED
    # paquete ha sido generado
    # packet has just been generated
    LOG_GENERATED = LOG_CORRUPTED + 1
    LOG_GENERATED_DES = 'paquete generado'
    # el paquete se ha depreciado debido a que no hay espacio en la cola
    # packet has been dropped because there is no space in the queue
    LOG_QUEUE_DROPPED = LOG_GENERATED + 1
    LOG_QUEUE_DROPPED_DES = "paquete depreciado"
    # utilizado para hacer log con el tamaño de la cola
    # use to log queue size in time
    LOG_QUEUE_SIZE = LOG_QUEUE_DROPPED + 1
    LOG_QUEUE_SIZE_DES = 'tamano queue'
    # utilizado para crear log de estado de nodo
    # use to log node state in time
    LOG_NODE_STATE = LOG_QUEUE_SIZE + 1
    LOG_NODE_STATE_DES = 'nuevo estatus'
    # utilizado para crear log de estado del periodo NPRACH
    # use to log NPRACH status
    LOG_NPRACH= LOG_NODE_STATE + 1
    LOG_NPRACH_DES = 'NPRACH inicio'
    LOG_NPRACH_FIN = LOG_NPRACH + 1
    LOG_NPRACH_FIN_DES = 'NPRACH fin'
    # utilizado para crear log de estado del periodo NOMA
    # use to log NOMA status
    LOG_NOMA = LOG_NPRACH_FIN + 1
    LOG_NOMA_DES = 'NOMA inicio'
    LOG_NOMA_FIN = LOG_NOMA + 1
    LOG_NOMA_FIN_DES = 'Tasas insatisfechas'

    LOG_NUEVO_CLUSTER = LOG_NOMA_FIN + 1
    LOG_NUEVO_CLUSTER_DES = 'Nuevo cluster'

    LOG_BLOQUEO_CLUSTER = LOG_NUEVO_CLUSTER + 1
    LOG_BLOQUEO_CLUSTER_DES = 'Bloqueo cluster'

    def __init__(self, output_file, log_packets=True, log_queue_drops=True,
                 log_arrivals=True, log_queue_lengths=True, log_states=True):
        """
        Constructor.
        Constructor.
        :param output_file: archivo de salida | output file name. will be overwritten if already
        existing
        :param log_packets: logging de paquetes | enable/disable logging of packets
        (RECEIVED/CORRUPTED)
        :param log_queue_drops: logginf de paquetes depreciados | enable/disable logging of packet drops
        :param log_arrivals: logging de llegada de paquetes | enable/disable logging of packet arrivals
        :param log_queue_lengths: logging del tamaño de la cola | enable/disable logging of queue lengths
        :param log_states: logging del estado de los nodos | enable/disable logging of the state of nodes
        """
        self.sim = sim.Sim.Instance()
        self.log_file = open(output_file, "w")
        self.log_file.write("tiempo,fuente,tipo,destino,tipo,evento,descripcion,tam/estado,detalles\n")
        self.log_packets = log_packets
        self.log_queue_drops = log_queue_drops
        self.log_arrivals = log_arrivals
        self.log_queue_lengths = log_queue_lengths
        self.log_states = log_states

    def log_packet(self, source, destination, packet):
        """
        Logea el resultado de la recepción de un paquete.
        Logs the result of a packet reception.
        :param source: fuente | source node
        :param destination: destino | destination node id
        :param packet: el paquete a loggear | the packet to log
        """
        if self.log_packets:
            # ["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 destination.get_id(),destination.get_tipo(), packet.get_state(),Packet.estados[packet.get_state()],
                                 packet.get_size(),'bytes'))

    def log_queue_drop(self, source, packet_size):
        """
        Logea la depreciación de un paquete.
        Logs a queue drop.
        :param source: fuente | source node
        :param packet_size: tamaño del paquete | size of the packet being dropped
        """
        if self.log_queue_drops:
            # ["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 source.get_id(),source.get_tipo, Log.LOG_QUEUE_DROPPED,Log.LOG_QUEUE_DROPPED_DES,
                                 packet_size,'bytes'))

    def log_arrival(self, source, packet_size):
        """
        Logea un arribo.
        Logs an arrival.
        :param source: fuente | source node
        :param packet_size: tamaño del paquete | size of the packet being dropped
        """
        if self.log_arrivals:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 source.get_id(),source.get_tipo(), Log.LOG_GENERATED,Log.LOG_GENERATED_DES,
                                 packet_size,'bytes'))

    def log_queue_length(self, node, length):
        """
        Logea el tamaño de la cola para un nodo en particular.
        Logs the length of the queue for a particular node.
        :param node: nodo | node
        :param length: tamaño de la cola | length of the queue
        """
        if self.log_queue_lengths:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_QUEUE_SIZE,Log.LOG_QUEUE_SIZE_DES, length,'paquetes'))

    def log_state(self, node, state):
        """
        Logea el estado de un nodo en particular.
        Logs the state of a particular node.
        :param node: nodo | node
        :param state: estado del nodo | state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NODE_STATE,Log.LOG_NODE_STATE_DES, state,node.estados[state]))

    def log_estado(self, evento, state):
        """
        Logea el estado de un nodo en particular.
        Logs the state of a particular node.
        :param node: nodo | node
        :param state: estado del nodo | state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), evento.get_source().get_id(),evento.get_source().get_tipo(),
                                 evento.get_destination().get_id(),evento.get_destination().get_tipo(), Log.LOG_NODE_STATE,Log.LOG_NODE_STATE_DES, state,evento.get_destination().estados[state]))


    def log_state_event(self, node,event, state):
        """
        Logea el estado de un evento y nodo en particular
        Logs the state of a particular node y evento
        :param node: nodo | node
        :param event: evento que activo el log | event that started the log
        :param state: estado de un nodo | state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), event.source.get_id(),event.source.get_id(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NODE_STATE,Log.LOG_NODE_STATE_DES, state,node.estados[state]))

    def log_bloqueo_cluster(self, enb,node, cluster, tasa):
        """
        Logea el estado de un evento y nodo en particular
        Logs the state of a particular node y evento
        :param node: nodo | node
        :param event: evento que activo el log | event that started the log
        :param state: estado de un nodo | state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), enb.get_id(),enb.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_BLOQUEO_CLUSTER,Log.LOG_BLOQUEO_CLUSTER_DES, cluster +1,str(int(tasa)) + ' bytes/s'))


    def log_nuevo_cluster(self, enb,node, cluster, tasa):
        """
        Logea el estado de un evento y nodo en particular
        Logs the state of a particular node y evento
        :param node: nodo | node
        :param event: evento que activo el log | event that started the log
        :param state: estado de un nodo | state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), enb.get_id(),enb.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NUEVO_CLUSTER,Log.LOG_NUEVO_CLUSTER_DES, cluster +1,str(int(tasa)) + ' bytes/s'))

    def log_periodoNPRACH(self,node,preambulos):
        """
        Logea el inicio del proceso NPRACH.
        Logs beginning of NPRACH process.
        :param node: nodo | node
        :param preambulos: preambulos al inicio del proceso | preambles at the start of the process
        """

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NPRACH,Log.LOG_NPRACH_DES, preambulos,'preambulos'))


    def log_periodoNPRACH_fin(self,node,throughput):
        """
        Logea el final del proceso NPRACH.
        Logs the ending of NPRACH process.
        :param node: nodo | node
        :param throughput: preambulos al final del proceso | preambles at the end of the process
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NPRACH_FIN,Log.LOG_NPRACH_FIN_DES, throughput,'throughput'))

    def log_inicio_NOMA(self,node):
        """
        Logea el inicio del proceso NOMA.
        Logs beginning of NOMA process.
        :param node: nodo | node
        :param dispositivos: dispositivos al inicio del proceso | UE's at the start of the process
        """

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%s,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NOMA,Log.LOG_NOMA_DES, str(len(node.channel.universoURLLC))+' URLLC', str(len(node.channel.universomMTC)) +' mMTC'))

    def log_fin_NOMA(self, node):
        """
        Logea el final del proceso NOMA.
        Logs the ending of NOMA process.
        :param node: nodo | node
        :param throughput: dispositivos al final del proceso | UE's at the end of the process
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%s,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NOMA_FIN,Log.LOG_NOMA_FIN_DES, str(len(node.channel.URLLC_tasanocubierta))+' URLLC',str(len(node.channel.mMTC_tasanocubierta)) +' mMTC'))

