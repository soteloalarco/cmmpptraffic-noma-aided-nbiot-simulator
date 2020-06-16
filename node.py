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

import sys
from module import Module
#from distribution import Distribution
from event import Event
from events import Events
from packet import Packet
import numpy as np


class Node(Module):
    """
    This class implements a node capable of communicating with other devices
    """

    # transmission speed parameter (bits per second)
    #DATARATE = "datarate"
    # queue size
    #QUEUE = "queue"
    # inter-arrival distribution (seconds)
    #INTERARRIVAL = "interarrival"
    # packet size distribution (bytes)
    #SIZE = "size"
    # processing time distribution (seconds)
    #PROC_TIME = "processing"
    # max packet size (bytes)
    #MAXSIZE = "maxsize"

    # list of possible states for this node
    IDLE = 0
    TX = 1
    RX = 2
    PROC = 3
    NPRACH = 4
    TX_MSG1 = 5
    PROC_RA = 6
    estados=["IDLE","TX-PKG","RX","PROC","NPRACH","TX-MSG1","PROC-RA"]

    def __init__(self,id,tipo, config, channel, x, y):
        """
        Constructor.
        :param config: the set of configs loaded by the simulator
        :param channel: the channel to which frames are sent
        :param x: x position
        :param y: y position
        """
        Module.__init__(self,id,tipo)
        # load configuration parameters
        #self.datarate = config.get_param(Node.DATARATE)
        #self.queue_size = config.get_param(Node.QUEUE)
        #self.interarrival = Distribution(config.get_param(Node.INTERARRIVAL))
        #self.size = Distribution(config.get_param(Node.SIZE))
        #self.proc_time = 0.01
        #self.maxsize = config.get_param(Node.MAXSIZE)
        # queue of packets to be sent
        self.queue = []
        # current state
        self.state = Node.IDLE
        self.logger.log_state(self, Node.IDLE)
        # save position
        self.x = x
        self.y = y
        # save channel
        self.channel = channel
        # current packet being either sent or received
        self.current_pkt = None
        # count the number of frames currently under reception
        self.receiving_count = 0
        # timeout event used to avoid being stuck in the RX state
        #self.timeout_event = None
        # timeout time for the rx timeout event. set as the time needed to
        # transmit a packet of the maximum size plus a small amount of 10
        # microseconds
        #self.timeout_time = self.maxsize * 8.0 / self.datarate + 10e-6

    def initialize(self):
        """
        Initialization. Starts node operation by scheduling the first packet
        """
        self.schedule_next_arrival()

    def initialize_eNB(self):
        """
        Initialization. Starts node operation by scheduling the first packet
        """
        self.schedule_next_periodoNOMA()
        self.schedule_next_periodoNPRACH()


    def handle_event(self, event):
        """
        Handles events notified to the node
        :param event: the event
        """
        #TODO programar el handle de eventos
        if event.get_type() == Events.PACKET_ARRIVAL: # Evento soportado
            self.handle_arrival()
        elif event.get_type() == Events.START_TX_MSG1:
            self.handle_start_tx_msg1(event)
        elif event.get_type() == Events.END_TX_MSG1:
            self.handle_end_tx_msg1(event)
        elif event.get_type() == Events.START_RX:
            self.handle_start_rx(event)
        elif event.get_type() == Events.END_RX:
            self.handle_end_rx(event)
        elif event.get_type() == Events.END_TX:
            self.handle_end_tx(event)
        elif event.get_type() == Events.END_PROC:
            self.handle_end_proc(event)
        elif event.get_type() == Events.END_PROC_MSG1:
            self.handle_end_proc_msg1(event)
        elif event.get_type() == Events.RX_TIMEOUT:
            self.handle_rx_timeout(event)
        elif event.get_type() == Events.PERIODO_NPRACH:
            self.handle_periodo_nprach()
        elif event.get_type() == Events.PERIODO_NOMA:
            self.handle_periodo_noma()
        else:
            print("Node %d has received a notification for event type %d which"
                  " can't be handled", (self.get_id(), event.get_type()))
            sys.exit(1)

    def schedule_next_periodoNPRACH(self):
        Ts = self.sim.TsNPRACH
        # Para asegurarnos que se resuelva antes que NOMA
        if self.sim.sig_periodo_NPRACH + Ts == self.sim.sig_periodo_NOMA:
            self.sim.sig_periodo_NPRACH = self.sim.sig_periodo_NPRACH + Ts
            sig_periodo_NPRACHaux= self.sim.sig_periodo_NPRACH + self.sim.duration_NPRACH #5.6 ms     #packet_size * 8 / 8000000
        else:
            self.sim.sig_periodo_NPRACH= self.sim.sig_periodo_NPRACH + Ts
            sig_periodo_NPRACHaux= self.sim.sig_periodo_NPRACH + self.sim.duration_NPRACH #5.6 ms     #packet_size * 8 / 8000000
        event = Event(sig_periodo_NPRACHaux, Events.PERIODO_NPRACH,self, self)
        self.sim.eventosaux.append([event.event_id,event.event_time,event.source.get_id()])
        self.sim.schedule_event(event)

    def schedule_next_periodoNOMA(self):
        Ts = self.sim.TsNOMA
        self.sim.sig_periodo_NOMA = self.sim.sig_periodo_NOMA + Ts
        event = Event(self.sim.sig_periodo_NOMA + self.sim.duration_NPRACH + self.sim.tiempoMinimo, Events.PERIODO_NOMA, self, self)
        self.sim.eventosaux.append([event.event_id, event.event_time, event.source.get_id()])
        self.sim.schedule_event(event)

    def schedule_next_arrival(self):
        """
        Schedules a new arrival event
        """
        #TODO guardar tamaño de paquete
        #enlista=False
        #extraemos el siguiente evento correspodiente a este nodo
        #[0,0.02,7,Monitoreo de agua y electricidad,0,20.65,1] => [idalarma,tiempo,iddispositivo,tipodispositivo,tipoevento,tampaquete,modelotrafico]
        for evento in self.sim.eventos:
            if evento[2]==self.module_id: # cuando se encuentre el siguiente evento en la lista corressspondiente a este modulo
                arrival = evento[1]

                # generate an event setting this node as destination
                event = Event(arrival, Events.PACKET_ARRIVAL,
                              self, self)
                self.sim.eventosaux.append([event.event_id, event.event_time, event.source.get_id()])
                self.sim.schedule_event(event)
                #enlista=True
                # eliminamos el evento de la lista
                self.sim.eventos.remove(evento)
                break

        #TODO Hard coded el tiempo en el que pasará el siguiente arribo

        # #generate an event setting this node as destination
        # if not enlista:
        #     arrival=1.6
        #     event = Event(self.sim.get_time() + arrival, Events.PACKET_ARRIVAL,
        #                    self, self)
        #     self.sim.eventosaux.append([event.event_id,event.event_time,event.source.get_id()])
        #     self.sim.schedule_event(event)

    def handle_periodo_nprach(self):
        self.logger.log_periodoNPRACH(self,len(self.sim.universoNPRACH))
        #TODO lógica para NPRACH
        self.sim.universoNPRACH = [1]
        #TODO el trhoughput se agrega al universo NOMA
        self.sim.universoNOMA.append(1)
        throughputNPRACH=len(self.sim.universoNPRACH)
        self.logger.log_periodoNPRACH_fin(self, throughputNPRACH)
        self.schedule_next_periodoNPRACH()
        self.sim.universoNPRACH = []

    def handle_periodo_noma(self):
        self.logger.log_periodoNOMA(self, len(self.sim.universoNOMA))
        # TODO lógica para NOMA
        self.sim.universoNOMA = []
        throughputNOMA = len(self.sim.universoNOMA)
        self.logger.log_periodoNOMA_fin(self, throughputNOMA)
        self.schedule_next_periodoNOMA()

    #def handle_start_tx(self):

    def handle_start_tx_msg1(self, event):
        packet_size = 500  # self.size.get_value()
        if self.state == Node.IDLE:

            # if we are in a idle state, then there must be no packets in the
            # queue
            assert(len(self.queue) == 0)
            # if current state is IDLE and there are no packets in the queue, we
            # can start transmitting
            # event.obj.pa
            self.transmit_msg1(packet_size)

            #se agrega el paquete a la lista del universo
            self.sim.universoNPRACH.append(self)

            self.state = Node.TX_MSG1
            self.logger.log_state(self, Node.TX_MSG1)
        else:
            # if we are either transmitting or receiving, packet must be queued
            if self.queue_size == 0 or len(self.queue) < self.queue_size:
                # if queue size is infinite or there is still space
                self.queue.append(packet_size)
                self.logger.log_queue_length(self, len(self.queue))
            else:
                # if there is no space left, we drop the packet and log
                self.logger.log_queue_drop(self, packet_size)
        # schedule next arrival
        self.schedule_next_arrival()


    def handle_arrival(self):
        """
        Handles a packet transmission
        """
        #TODO leer el tamaño del paquete y agregarlo al evento

        packet_size = 500  # self.size.get_value()

        # log the arrival
        self.logger.log_arrival(self, packet_size)
        # Programamos la tx para el siguiente periodo NPRACH
        start_tx = Event(self.sim.sig_periodo_NPRACH, Events.START_TX_MSG1, self,
                       self)
        self.sim.eventosaux.append([start_tx.event_id, start_tx.event_time, start_tx.source.get_id()])
        self.sim.schedule_event(start_tx)



    def handle_start_rx(self, event):
        """
        Handles beginning of a frame reception
        :param event: the RX event including the frame being received
        """
        new_packet = event.get_obj()
        if self.state == Node.IDLE:
            if self.receiving_count == 0:
                # node is idle: it will try to receive this packet
                assert(self.current_pkt is None)
                new_packet.set_state(Packet.PKT_RECEIVING)
                self.current_pkt = new_packet
                self.state = Node.RX
                assert(self.timeout_event is None)
                # create and schedule the RX timeout
                self.timeout_event = Event(self.sim.get_time() +
                                           self.timeout_time, Events.RX_TIMEOUT,
                                           self, self, None)
                self.sim.schedule_event(self.timeout_event)
                self.logger.log_state(self, Node.RX)
            else:
                # there is another signal in the air but we are IDLE. this
                # happens if we start receiving a frame while transmitting
                # another. when we are done with the transmission we assume we
                # are not able to detect that there is another frame in the air
                # (we are not doing carrier sensing). In this case we assume we
                # are not able to detect the new one and set that to corrupted
                new_packet.set_state(Packet.PKT_CORRUPTED)
        else:
            # node is either receiving or transmitting
            if self.state == Node.RX and self.current_pkt is not None:
                # the frame we are currently receiving is corrupted by a
                # collision, if we have one
                self.current_pkt.set_state(Packet.PKT_CORRUPTED)
            # the same holds for the new incoming packet. either if we are in
            # the RX, TX, or PROC state, we won't be able to decode it
            new_packet.set_state(Packet.PKT_CORRUPTED)
        # in any case, we schedule a new event to handle the end of this frame
        end_rx = Event(self.sim.get_time() + new_packet.get_duration(),
                       Events.END_RX, self, self, new_packet)
        self.sim.schedule_event(end_rx)
        # count this as currently being received
        self.receiving_count = self.receiving_count + 1

    def handle_end_rx(self, event):
        """
        Handles the end of a reception
        :param event: the END_RX event
        """
        packet = event.get_obj()
        # if the packet that ends is the one that we are trying to receive, but
        # we are not in the RX state, then something is very wrong
        if self.current_pkt is not None and \
           packet.get_id() == self.current_pkt.get_id():
            assert(self.state == Node.RX)
        if self.state == Node.RX:
            if packet.get_state() == Packet.PKT_RECEIVING:
                # the packet is not in a corrupted state: we succesfully
                # received it
                packet.set_state(Packet.PKT_RECEIVED)
                # just to be sure: we can only correctly receive the packet we
                # were trying to decode
                assert(packet.get_id() == self.current_pkt.get_id())
            # we might be in RX state but have no current packet. this can
            # happen when a packet overlaps with the current one being received
            # and the one being received terminates earlier. we assume to stay
            # in the RX state because we are not able to detect the end of the
            # frame
            if self.current_pkt is not None and \
               packet.get_id() == self.current_pkt.get_id():
                self.current_pkt = None
            if self.receiving_count == 1:
                # this is the only frame currently in the air, move to PROC
                # before restarting operations
                self.switch_to_proc()
                # delete the timeout event
                self.sim.cancel_event(self.timeout_event)
                self.timeout_event = None
        self.receiving_count = self.receiving_count - 1
        # log packet
        self.logger.log_packet(event.get_source(), self, packet)

    def switch_to_proc(self):
        """
        Switches to the processing state and schedules the end_proc event
        """
        #TODO hardcoded tiempo de procesamiento
        proc_time = 0
        proc = Event(self.sim.get_time() + proc_time, Events.END_PROC, self,
                     self)
        self.sim.eventosaux.append([proc.event_id, proc.event_time, proc.source.get_id()])
        self.sim.schedule_event(proc)
        self.state = Node.PROC
        #self.logger.log_state(self, Node.PROC)

    def switch_to_proc_msg1(self):
        proc = Event(self.sim.sig_periodo_NPRACH +self.sim.duration_NPRACH+ self.sim.time_slot, Events.END_PROC_MSG1, self,
                     self)
        self.sim.eventosaux.append([proc.event_id, proc.event_time, proc.source.get_id()])
        self.sim.schedule_event(proc)
        self.state = Node.PROC_RA
        self.logger.log_state(self, Node.PROC_RA)

    def handle_rx_timeout(self, event):
        """
        Handles RX timeout
        :param event: the RX_TIMEOUT event
        """
        # when this event happens, we can only be in RX state, otherwise
        # something is wrong
        assert(self.state == Node.RX)
        # in addition, the timeout should be longer than any possible packet,
        # meaning that we must not be receiving a packet when the timeout occurs
        assert(self.current_pkt is None)
        # the timeout forces us to switch to the PROC state
        self.switch_to_proc()
        self.timeout_event = None

    def handle_end_tx_msg1(self, event):
        assert (self.state == Node.TX_MSG1)
        assert (self.current_pkt is not None)
        assert (self.current_pkt.get_id() == event.get_obj().get_id())
        self.current_pkt = None
        self.switch_to_proc_msg1()

    def handle_end_tx(self, event):
        """
        Handles the end of a transmission done by this node
        :param event: the END_TX event
        """
        assert(self.state == Node.TX)
        assert(self.current_pkt is not None)
        assert(self.current_pkt.get_id() == event.get_obj().get_id())
        self.current_pkt = None
        # the only thing to do here is to move to the PROC state
        self.switch_to_proc()

    def handle_end_proc_msg1(self, event):
        #TODO programar bien la transmision del paquete porq ahorita nadamas tenemos 1 paquete y no el preambulo
        assert (self.state == Node.PROC_RA)
        # if len(self.queue) == 1:
            # resuming operations but nothing to transmit. back to IDLE
        self.transmit_packet(packet_size=500)
        self.state = Node.TX
        self.logger.log_state(self, Node.TX)
        # else:
        #     # there is a packet ready, trasmit it
        #     packet_size = self.queue.pop(0)
        #     self.transmit_packet(packet_size)
        #     self.state = Node.TX
        #     self.logger.log_state(self, Node.TX)
        #     self.logger.log_queue_length(self, len(self.queue))

    def handle_end_proc(self, event):
        """
        Handles the end of the processing period, resuming operations
        :param event: the END_PROC event
        """
        assert(self.state == Node.PROC)
        if len(self.queue) == 0:
            # resuming operations but nothing to transmit. back to IDLE
            self.state = Node.IDLE
            self.logger.log_state(self, Node.IDLE)
        else:
            # there is a packet ready, trasmit it
            packet_size = self.queue.pop(0)
            self.transmit_packet(packet_size)
            self.state = Node.TX
            self.logger.log_state(self, Node.TX)
            self.logger.log_queue_length(self, len(self.queue))

    def transmit_msg1(self, packet_size):
        """
        Generates, sends, and schedules end of transmission of a new packet
        :param packet_size: size of the packet to send in bytes
        """

        #TODO hardcoded, podemos calcular el tiempo en el que se transmitirá el mensaje con la tasa lograda ?

        packet = Packet(packet_size, self.sim.duration_NPRACH)
        # transmit packet
        #self.channel.start_transmission(self, packet)
        # schedule end of transmission
        # aquí programamos el envio en el siguiente periodo NPRACH
        end_tx_msg1 = Event(self.sim.get_time() + self.sim.duration_NPRACH, Events.END_TX_MSG1, self,
                       self, packet)
        self.sim.eventosaux.append([end_tx_msg1.event_id, end_tx_msg1.event_time, end_tx_msg1.source.get_id()])
        self.sim.schedule_event(end_tx_msg1)
        self.current_pkt = packet

    def transmit_packet(self, packet_size):
        """
        Generates, sends, and schedules end of transmission of a new packet
        :param packet_size: size of the packet to send in bytes
        """

        #TODO hardcoded, podemos calcular el tiempo en el que se transmitirá el mensaje con la tasa lograda

        packet = Packet(packet_size, self.sim.duration_NPRACH)
        # transmit packet
        #self.channel.start_transmission(self, packet)
        # schedule end of transmission
        # aquí programamos el envio en el siguiente periodo NPRACH
        end_tx = Event(self.sim.sig_periodo_NOMA  -self.sim.tiempoMinimo, Events.END_TX, self,
                       self, packet)
        self.sim.eventosaux.append([end_tx.event_id, end_tx.event_time, end_tx.source.get_id()])
        self.sim.schedule_event(end_tx)
        self.current_pkt = packet

    def get_posx(self):
        """
        Returns x position
        :returns: x position in meters
        """
        return self.x

    def get_posy(self):
        """
        Returns y position
        :returns: y position in meters
        """
        return self.y
