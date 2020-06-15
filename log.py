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

import sim
from packet import Packet

#TODO corregir problema con los logs
class Log:
    """
    Defines data logging utilities
    """

    # packet has been correctly received
    LOG_RECEIVED = Packet.PKT_RECEIVED
    # packet has been corrupted due to, for example, a collision
    LOG_CORRUPTED = Packet.PKT_CORRUPTED
    # packet has just been generated
    LOG_GENERATED = LOG_CORRUPTED + 1
    LOG_GENERATED_DES = 'paquete generado'
    # packet has been dropped because there is no space in the queue
    LOG_QUEUE_DROPPED = LOG_GENERATED + 1
    LOG_QUEUE_DROPPED_DES = "paquete depreciado"
    # use to log queue size in time
    LOG_QUEUE_SIZE = LOG_QUEUE_DROPPED + 1
    LOG_QUEUE_SIZE_DES = 'tamano queue'
    # use to log node state in time
    LOG_NODE_STATE = LOG_QUEUE_SIZE + 1
    LOG_NODE_STATE_DES = 'nuevo estatus'
    #
    LOG_NPRACH= LOG_NODE_STATE + 1
    LOG_NPRACH_DES = 'NPRACH inicio'
    LOG_NPRACH_FIN = LOG_NPRACH + 1
    LOG_NPRACH_FIN_DES = 'NPRACH fin'
    #
    LOG_NOMA = LOG_NPRACH_FIN + 1
    LOG_NOMA_DES = 'NOMA inicio'
    LOG_NOMA_FIN = LOG_NOMA + 1
    LOG_NOMA_FIN_DES = 'NOMA fin'

    def __init__(self, output_file, log_packets=True, log_queue_drops=True,
                 log_arrivals=True, log_queue_lengths=True, log_states=True):
        """
        Constructor.
        :param output_file: output file name. will be overwritten if already
        existing
        :param log_packets: enable/disable logging of packets
        (RECEIVED/CORRUPTED)
        :param log_queue_drops: enable/disable logging of packet drops
        :param log_arrivals: enable/disable logging of packet arrivals
        :param log_queue_lengths: enable/disable logging of queue lengths
        :param log_states: enable/disable logging of the state of nodes
        """
        self.sim = sim.Sim.Instance()
        self.log_file = open(output_file, "w")
        self.log_file.write("tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n")
        self.log_packets = log_packets
        self.log_queue_drops = log_queue_drops
        self.log_arrivals = log_arrivals
        self.log_queue_lengths = log_queue_lengths
        self.log_states = log_states

    def log_packet(self, source, destination, packet):
        """
        Logs the result of a packet reception.
        :param source: source node
        :param destination: destination node id
        :param packet: the packet to log
        """
        if self.log_packets:
            # ["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 destination.get_id(),destination.get_tipo(), packet.get_state(),Packet.estados[packet.get_state()],
                                 packet.get_size(),'bytes'))

    def log_queue_drop(self, source, packet_size):
        """
        Logs a queue drop
        :param source: source node
        :param packet_size: size of the packet being dropped
        """
        if self.log_queue_drops:
            # ["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 source.get_id(),source.get_tipo, Log.LOG_QUEUE_DROPPED,Log.LOG_QUEUE_DROPPED_DES,
                                 packet_size,'bytes'))

    def log_arrival(self, source, packet_size):
        """
        Logs an arrival
        :param source: source node
        :param packet_size: size of the packet being dropped
        """
        if self.log_arrivals:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), source.get_id(),source.get_tipo(),
                                 source.get_id(),source.get_tipo(), Log.LOG_GENERATED,Log.LOG_GENERATED_DES,
                                 packet_size,'bytes'))

    def log_queue_length(self, node, length):
        """
        Logs the length of the queue for a particular node
        :param node: node
        :param length: length of the queue
        """
        if self.log_queue_lengths:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_QUEUE_SIZE,Log.LOG_QUEUE_SIZE_DES, length,'paquetes'))

    def log_state(self, node, state):
        """
        Logs the state of a particular node
        :param node: node
        :param state: state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NODE_STATE,Log.LOG_NODE_STATE_DES, state,node.estados[state]))

    def log_state_event(self, node,event, state):
        """
        Logs the state of a particular node
        :param node: node
        :param state: state of the node
        """
        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), event.source.get_id(),event.source.get_id(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NODE_STATE,Log.LOG_NODE_STATE_DES, state,node.estados[state]))


    def log_periodoNPRACH(self,node,throughput):

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NPRACH,Log.LOG_NPRACH_DES, throughput,'preambulos'))


    def log_periodoNPRACH_fin(self,node,throughput):

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NPRACH_FIN,Log.LOG_NPRACH_FIN_DES, throughput,'throughput'))

    def log_periodoNOMA(self,node,throughput):

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NOMA,Log.LOG_NOMA_DES, throughput,'dispositivos'))

    def log_periodoNOMA_fin(self, node, throughput):

        if self.log_states:
            #["tiempo,fuente,tipo,destino,tipo,evento,descripcion,tamano/estado,detalles\n"]
            self.log_file.write("%f,%d,%s,%d,%s,%d,%s,%d,%s\n" %
                                (self.sim.get_time(), node.get_id(),node.get_tipo(),
                                 node.get_id(),node.get_tipo(), Log.LOG_NOMA_FIN,Log.LOG_NOMA_FIN_DES, throughput,'throughput'))

