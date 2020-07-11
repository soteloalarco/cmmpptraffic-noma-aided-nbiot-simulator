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

import sys
from des.module import Module
from des.event import Event
from des.events import Events
from des.packet import Packet


class Node(Module):
    """
    Esta clase implementa a un nodo capaz de comunicarse con otros dispositivos.
    This class implements a node capable of communicating with other devices.
    """
    # lista de los posibles estados de un nodo
    # list of possible states for this node
    IDLE = 0
    TX = 1
    RX = 2
    PROC = 3
    NOMA = 4
    TX_MSG1 = 5
    PREAMBULO = 6
    estados=["IDLE","TX-PKG","RX","PROC","NOMA","TX-MSG1","PREAMBULO"]

    TIPO1 ='Control de iluminacion'
    TIPO2 = 'Monitoreo de agua y electricidad'
    TIPO3 = 'Deteccion de terremotos'
    TIPO4 = 'Semaforos inteligentes'
    TIPO5 = 'Contaminacion del aire'
    TIPO6 = 'Otros dispositivos mMTC'
    TIPO7 = 'Dispositivos URLLC'


    def __init__(self,id,tipo, config, channel, x, y):
        """
        Constructor.
        Constructor.
        :param config: el conjunto de configuraciones cargadas | the set of configs loaded by the simulator
        :param channel: el canal al que las tramas son enviadas| the channel to which frames are sent
        :param x: x position
        :param y: y position
        """
        Module.__init__(self,id,tipo)
        # cola de paquetes a sser enviados
        # queue of packets to be sent
        self.queue = []
        # estado actual del nodo
        # current state
        self.state = Node.IDLE
        # se crea un log que indica la creación del dispositivo
        # a log indicating the creation of a device is added
        self.logger.log_state(self, Node.IDLE)
        # se guarda la posición del dispositivo
        # save position
        self.x = x
        self.y = y
        # se guarda el canal
        # save channel
        self.channel = channel
        # el paquete altual qeu esta siendo enviado o recibido
        # current packet being either sent or received
        self.current_pkt = None
        # cuenta el número de frames siendo recibidas
        # count the number of frames currently under reception
        self.receiving_count = 0
        self.tasa_tx=0 # bits/s
        self.paquete_restante=0
        self.ultimo_proc_noma = 0
        self.evento_end_tx = None
        self.cluster = -1


    def initialize(self):
        """
        Inicialización. Inicia la operación de un nodo UE calendarizando el primer paquete.
        Initialization. Starts node operation by scheduling the first packet.
        """
        self.schedule_next_arrival()

    def initialize_eNB(self):
        """
        Inicialización de eNB. Inicia la operación de las eNB calendarizando los periodos NOMA y NPRACH.
        Initialization. Starts eNB operation by scheduling the first NOMA and NPRACH operations.
        """
        #TODO ya no se hará esto de periodo noma ni nprach, poner nueva configuración
        #self.schedule_next_periodoNOMA()
        #self.schedule_next_periodoNPRACH()


    def handle_event(self, event, src):
        """
        Se hace cargo del evento notificado al nodo receptor.
        Handles events notified to the node.
        :param event: el evento | the event
        """

        if event.get_type() == Events.PACKET_ARRIVAL:
            self.handle_arrival(event)
        elif event.get_type() ==  Events.END_PROC_NOMA:
            self.handle_end_proc_noma(event, src)
        elif event.get_type() == Events.END_TX:
            self.handle_end_tx(event)
        elif event.get_type() == Events.END_PROC:
            self.handle_end_proc(event)
        else:
            print("Node %d has received a notification for event type %d which"
                  " can't be handled", (self.get_id(), event.get_type()))
            sys.exit(1)

    def schedule_next_arrival(self):
        """
        Calendariza el siguiente arribo de un paquete a partir de la lista de eventos
        Schedules a new tiempo_arribo event
        """

        # extraemos el siguiente evento correspodiente a este nodo
        # the next event corresponding to self in sim.eventos is added
        # Formato de sim.eventos | Format of sim.eventos
        #[0,0.02,7,Monitoreo de agua y electricidad,0,20.65,1] => [idalarma,tiempo,iddispositivo,tipodispositivo,tipoevento,tampaquete,modelotrafico]
        for evento in self.sim.eventos:
            # cuando se encuentre el siguiente evento en la lista correspondiente a este modulo
            # when the next event in the list corresponding to this module is found
            id_dispositivo=evento[2]
            if id_dispositivo==self.module_id:
                tiempo_arribo = evento[1]
                # se genera un evento y se establece a este nodo como el destino
                # generate an event setting this node as destination
                #TODO registrar si se trata de URRLLC o mMTC

                # se crea un paquete con la información de la lista eventos | we create a packet with the information in the list event
                tam_paquete=evento[5]
                paquete=Packet(tam_paquete)
                if tiempo_arribo<self.sim.get_time():
                    event = Event(self.sim.get_time(), Events.PACKET_ARRIVAL,
                                  self, self, paquete)
                else:
                    event = Event(tiempo_arribo, Events.PACKET_ARRIVAL,
                              self, self,paquete)
                self.sim.eventosaux.append([event.event_id, event.event_time, event.source.get_id()])
                # se calendariza el evento
                # the event is scheduled
                self.sim.schedule_event(event)
                # eliminamos el evento de la lista
                # the event is now deleted from the list sim.eventos
                self.sim.eventos.remove(evento)
                break


############ métodos handle

    def handle_arrival(self,event):
        """
        Se encarga de iniciar la transmisión de un paquete
        Handles a packet transmission
        """
        #TODO leer el tamaño del paquete y agregarlo al evento

        # se asigna al dispositivo el paquete como paquete actual
        # we asigne the packet from the event as the current pkg
        paquete_actual = event.get_obj()
        self.current_pkt = paquete_actual

        # log de arribo
        # log the arrival
        self.logger.log_arrival(self, paquete_actual.get_size())
        # Programamos la tx del preambulo
        # the tx of the preamble

        self.transmit_preamble()


    def handle_end_tx(self, event):
        """
        Se encarga del fin de la transmisión hecha por este nodo
        Handles the end of a transmission done by this node
        :param event: the END_TX event
        """
        assert(self.state == Node.TX)
        assert(self.current_pkt is not None)
        assert(self.current_pkt.get_id() == event.get_obj().get_id())
        self.current_pkt = None
        self.evento_end_tx = None
        self.paquete_restante = 0
        self.ultimo_proc_noma = 0
        self.tasa_tx = 0
        self.cluster = -1
        self.channel.nodes.remove(self)
        # se pasa a estado de procesamiento antes de volver a esta idle
        # the only thing to do here is to move to the PROC state
        self.switch_to_proc()

    def handle_end_proc(self, event):
        """
        Se encarga del final del periodo de processo y se reanuda la operación.
        Handles the end of the processing period, resuming operations.
        :param event: the END_PROC event
        """
        assert(self.state == Node.PROC)
        if len(self.queue) == 0:
            # si se reanuda la operación pero no hay nada que transmitir se cambia a estado IDLE
            # resuming operations but nothing to transmit. back to IDLE
            self.state = Node.IDLE
            self.logger.log_state(self, Node.IDLE)
        else:
            # si hay un paquete listo, se transmite
            # there is a packet ready, trasmit it
            packet_size = self.queue.pop(0)
            self.transmit_packet(packet_size)
            self.state = Node.TX
            self.logger.log_state(self, Node.TX)
            self.logger.log_queue_length(self, len(self.queue))
        # se calendariza el siguiente arribo
        # schedule next arrival
        self.schedule_next_arrival()

        # calendarizamos un proceso NOMA
        # schedule end of transmission
        proc_noma = Event(self.sim.get_time() + self.sim.tiempoMinimo, Events.END_PROC_NOMA, self.sim.node_eNB,
                          self, None)
        if (self.sim.node_eNB.get_state() == Node.IDLE and len(self.sim.channel.nodes)>0):  # sólo se agenda proceso noma una vez si mas paquetes se transmiten al mismo tiempo
            self.sim.node_eNB.state = Node.NOMA
            self.sim.eventosaux.append([proc_noma.event_id, proc_noma.event_time, proc_noma.source.get_id()])
            self.sim.schedule_event(proc_noma)

    def handle_end_proc_noma(self, event, src):
        #assert (self.state == Node.PREAMBULO)
        #TODO Lógica NOMA y ajustar su tasa o no transmitir si no alcanzó cluster

        self.logger.log_state(self, Node.NOMA)
        self.state = Node.IDLE
        self.sim.channel.algoritmo_NOMA(self)
        #TODO cambiar porqeu está hardcoded
        self.logger.log_fin_NOMA(self)


##########

    def transmit_packet(self):
        """
        Genera, envia y calendariza el final de la transmisión del paquete
        Generates, sends, and schedules end of transmission of a new packet
        :param packet_size: size of the packet to send in bytes
        """
        # imprimimos el nuevo cluster
        self.logger.log_nuevo_cluster(self.sim.node_eNB,self, self.cluster, self.tasa_tx)

        self.state = Node.TX
        self.logger.log_state(self, Node.TX)


        packet = self.current_pkt
        # TODO podemos transmitir el paquete por el canal

        # transmit packet
        #self.channel.start_transmission(self, packet)
        # una vez se comienza la transmisión del paquete se toma en cuenta para el proceso NOMA
        #self.sim.universoNOMA.append(self)
        # calendarizamos el final de la transmisión hasta antes de que inicie el siguiente periodo NOMA
        # schedule end of transmission
        #end_tx = Event(self.sim.get_time() + 1, Events.END_TX, self,
        #               self, packet)
        end_tx = self.evento_end_tx
        self.sim.eventosaux.append([end_tx.event_id, end_tx.event_time, end_tx.source.get_id()])
        self.sim.schedule_event(end_tx)




    def transmit_preamble(self):
        """
        Genera, envia y calendariza el final de la transmisión del paquete
        Generates, sends, and schedules end of transmission of a new packet
        :param packet_size: size of the packet to send in bytes
        """
        #TODO cambiar por el paquete real
        packet = self.current_pkt
        # TODO podemos transmitir el paquete por el canal


        # calendarizamos el final de la transmisión hasta antes de que inicie el siguiente periodo NOMA
        # schedule end of transmission
        proc_noma = Event(self.sim.get_time() + self.sim.tiempoMinimo, Events.END_PROC_NOMA, self.sim.node_eNB,
                          self, packet)
        if(self.sim.node_eNB.get_state() == Node.IDLE): # sólo se agenda proceso noma una vez si mas paquetes se transmiten al mismo tiempo
            self.sim.node_eNB.state = Node.NOMA
            self.sim.eventosaux.append([proc_noma.event_id, proc_noma.event_time, proc_noma.source.get_id()])
            self.sim.schedule_event(proc_noma)

        # transmitimos el preambulo
        self.channel.start_transmission(self, packet)
        self.current_pkt = packet
        self.state = Node.PREAMBULO
        self.logger.log_estado(proc_noma, Node.PREAMBULO)

    def switch_to_proc(self):
        """
        Cambio a estado procesando y calendariza el fin del proceso
        Switches to the processing state and schedules the end_proc event
        """
        proc_time = 0
        proc = Event(self.sim.get_time() + proc_time, Events.END_PROC, self,
                     self)
        self.sim.eventosaux.append([proc.event_id, proc.event_time, proc.source.get_id()])
        self.sim.schedule_event(proc)
        self.state = Node.PROC

    # def handle_periodo_nprach(self):
    #     """
    #     Calendariza el siguiente proceso NPRACH
    #     Schedules the next NPRACH process
    #     """
    #     self.logger.log_periodoNPRACH(self,len(self.sim.universoNPRACH))
    #     throughputNPRACH=self.sim.algoritmo_RA()
    #     self.logger.log_periodoNPRACH_fin(self, throughputNPRACH)
    #     self.schedule_next_periodoNPRACH()

    # def handle_periodo_noma(self):
    #     """
    #     Calendariza el siguiente proceso NOMA
    #     Schedules the next NOMA process
    #     """
    #     self.logger.log_periodoNOMA(self, len(self.sim.universoNOMA))
    #     aleatorio = int(np.random.uniform(0, len(self.sim.universoNOMA), 1))
    #     throughput = [1] * aleatorio
    #     self.sim.universoNOMA = throughput
    #     throughputNOMA = len(self.sim.universoNOMA)
    #     self.logger.log_periodoNOMA_fin(self, throughputNOMA)
    #     self.schedule_next_periodoNOMA()
    #     self.sim.universoNOMA = []

    # def handle_end_tx_msg1(self, event):
    #     """
    #     Se encarga del fin de transmisión del msg1
    #     handle the end of tx_msg1
    #     """
    #     assert (self.state == Node.TX_MSG1)
    #     assert (self.current_pkt is not None)
    #     assert (self.current_pkt.get_id() == event.get_obj().get_id())
    #     self.switch_to_proc_msg1()

    # def schedule_next_periodoNPRACH(self):
    #     """
    #     Calendariza el siguiente proceso NPRACH
    #     Schedules the next NPRACH process
    #     """
    #     Ts = self.sim.TsNPRACH
    #     self.sim.sig_periodo_NPRACH= self.sim.sig_periodo_NPRACH + Ts
    #     # el cómputo del proceso se realizará al terminar la transmisión de los preámbulos
    #     # the RA compute will happen after the duration of the preamble
    #     sig_periodo_NPRACHaux= self.sim.sig_periodo_NPRACH + self.sim.duracion_preambulo
    #
    #     event = Event(sig_periodo_NPRACHaux, Events.PERIODO_NPRACH,self, self)
    #     self.sim.eventosaux.append([event.event_id,event.event_time,event.source.get_id()])
    #     self.sim.schedule_event(event)

    # def schedule_next_periodoNOMA(self):
    #     """
    #     Calendariza el siguiente proceso NOMA
    #     Schedules the next NOMA process
    #     """
    #     Ts = self.sim.TsNOMA
    #     self.sim.sig_periodo_NOMA = self.sim.sig_periodo_NOMA + Ts
    #     # se agrega sim.tiempoMinimo en caso de qeu NPRACH y NOMA pasen al mismo tiempo, para asegurarnos que noma pase después
    #     # self.sim.tiempoMinimo is added to assure that NPRACH is computed before in case they happend at the same time
    #     event = Event(self.sim.sig_periodo_NOMA + self.sim.duracion_preambulo, Events.PERIODO_NOMA, self, self)
    #     self.sim.eventosaux.append([event.event_id, event.event_time, event.source.get_id()])
    #     self.sim.schedule_event(event)

    # def transmit_msg1(self, paquete):
    #     """
    #     Genera, envia y calendariza el final de la transmisión del msg1
    #     Generates, sends, and schedules end of transmission of msg1
    #     :param packet_size: size of the packet to send in bytes
    #     """
    #

    #
    #     # transmit packet
    #     #self.channel.start_transmission(self, packet)
    #     # calendarizamos el final de tx del msg1 al final de la duración del preambulo
    #     # schedule end of transmission
    #     end_tx_msg1 = Event(self.sim.get_time() + self.sim.duracion_preambulo, Events.END_TX_MSG1, self,
    #                         self, paquete)
    #     self.sim.eventosaux.append([end_tx_msg1.event_id, end_tx_msg1.event_time, end_tx_msg1.source.get_id()])
    #     self.sim.schedule_event(end_tx_msg1)
    #     # se agrega el preambulo a la lista del universo NPRACH y se cambia el estado del UE
    #     # the preamble is added to the list universoNPRACH
    #     self.sim.universoNPRACH.append(end_tx_msg1)
    #     self.current_pkt = paquete

    # def switch_to_proc_msg1(self):
    #     """
    #     Cambio a estado procesando_msg1 y calendariza el fin del proceso
    #     Switches to the processing_msg1 state and schedules the end_proc event
    #     """
    #     proc = Event(self.sim.sig_periodo_NPRACH + self.sim.duracion_preambulo + self.sim.time_slot, Events.END_PROC_MSG1, self,
    #                  self)
    #     self.sim.eventosaux.append([proc.event_id, proc.event_time, proc.source.get_id()])
    #     self.sim.schedule_event(proc)
    #     self.state = Node.PROC_RA
    #     self.logger.log_state(self, Node.PROC_RA)

    # def handle_start_rx(self, event):
    #     """
    #     Handles beginning of a frame reception
    #     :param event: the RX event including the frame being received
    #     """
    #     new_packet = event.get_obj()
    #     if self.state == Node.IDLE:
    #         if self.receiving_count == 0:
    #             # node is idle: it will try to receive this packet
    #             assert(self.current_pkt is None)
    #             new_packet.set_state(Packet.PKT_RECEIVING)
    #             self.current_pkt = new_packet
    #             self.state = Node.RX
    #             assert(self.timeout_event is None)
    #             # create and schedule the RX timeout
    #             self.timeout_event = Event(self.sim.get_time() +
    #                                        self.timeout_time, Events.RX_TIMEOUT,
    #                                        self, self, None)
    #             self.sim.schedule_event(self.timeout_event)
    #             self.logger.log_state(self, Node.RX)
    #         else:
    #             # there is another signal in the air but we are IDLE. this
    #             # happens if we start receiving a frame while transmitting
    #             # another. when we are done with the transmission we assume we
    #             # are not able to detect that there is another frame in the air
    #             # (we are not doing carrier sensing). In this case we assume we
    #             # are not able to detect the new one and set that to corrupted
    #             new_packet.set_state(Packet.PKT_CORRUPTED)
    #     else:
    #         # node is either receiving or transmitting
    #         if self.state == Node.RX and self.current_pkt is not None:
    #             # the frame we are currently receiving is corrupted by a
    #             # collision, if we have one
    #             self.current_pkt.set_state(Packet.PKT_CORRUPTED)
    #         # the same holds for the new incoming packet. either if we are in
    #         # the RX, TX, or PROC state, we won't be able to decode it
    #         new_packet.set_state(Packet.PKT_CORRUPTED)
    #     # in any case, we schedule a new event to handle the end of this frame
    #     end_rx = Event(self.sim.get_time() + new_packet.get_duration(),
    #                    Events.END_RX, self, self, new_packet)
    #     self.sim.schedule_event(end_rx)
    #     # count this as currently being received
    #     self.receiving_count = self.receiving_count + 1

    # def handle_end_rx(self, event):
    #     """
    #     Handles the end of a reception
    #     :param event: the END_RX event
    #     """
    #     packet = event.get_obj()
    #     # if the packet that ends is the one that we are trying to receive, but
    #     # we are not in the RX state, then something is very wrong
    #     if self.current_pkt is not None and \
    #        packet.get_id() == self.current_pkt.get_id():
    #         assert(self.state == Node.RX)
    #     if self.state == Node.RX:
    #         if packet.get_state() == Packet.PKT_RECEIVING:
    #             # the packet is not in a corrupted state: we succesfully
    #             # received it
    #             packet.set_state(Packet.PKT_RECEIVED)
    #             # just to be sure: we can only correctly receive the packet we
    #             # were trying to decode
    #             assert(packet.get_id() == self.current_pkt.get_id())
    #         # we might be in RX state but have no current packet. this can
    #         # happen when a packet overlaps with the current one being received
    #         # and the one being received terminates earlier. we assume to stay
    #         # in the RX state because we are not able to detect the end of the
    #         # frame
    #         if self.current_pkt is not None and \
    #            packet.get_id() == self.current_pkt.get_id():
    #             self.current_pkt = None
    #         if self.receiving_count == 1:
    #             # this is the only frame currently in the air, move to PROC
    #             # before restarting operations
    #             self.switch_to_proc()
    #             # delete the timeout event
    #             self.sim.cancel_event(self.timeout_event)
    #             self.timeout_event = None
    #     self.receiving_count = self.receiving_count - 1
    #     # log packet
    #     self.logger.log_packet(event.get_source(), self, packet)


    # def handle_rx_timeout(self, event):
    #     """
    #     Handles RX timeout
    #     :param event: the RX_TIMEOUT event
    #     """
    #     # when this event happens, we can only be in RX state, otherwise
    #     # something is wrong
    #     assert(self.state == Node.RX)
    #     # in addition, the timeout should be longer than any possible packet,
    #     # meaning that we must not be receiving a packet when the timeout occurs
    #     assert(self.current_pkt is None)
    #     # the timeout forces us to switch to the PROC state
    #     self.switch_to_proc()
    #     self.timeout_event = None
    # def handle_start_tx_msg1(self, event):
    #     """
    #     Se encarga de iniciar la transmisión del msg1
    #     Handles the transmission of msg1
    #     """
    #     paquete = event.get_source().current_pkt
    #     if self.state == Node.IDLE:
    #         assert (paquete != None)
    #
    #
    #         # si estamos en un estado idle, entonces nuestra cola debe estar vacia
    #         # if we are in a idle state, then there must be no packets in the queue
    #         assert (len(self.queue) == 0)
    #         # si nuestro estado actual es 0 y la cola está vacia, se puede transmitir
    #         # if current state is IDLE and there are no packets in the queue, we can start transmitting
    #         self.transmit_msg1(paquete)
    #
    #         # se cambia el estado del UE
    #         # the state of the UE is changed
    #         self.state = Node.TX_MSG1
    #         self.logger.log_state(self, Node.TX_MSG1)
    #     else:
    #         # si se está ya sea transmitiendo o recibiendo, el paquete debe ser puesto en cola
    #         # if we are either transmitting or receiving, packet must be queued
    #         if self.queue_size == 0 or len(self.queue) < self.queue_size:
    #             # si el tamaño de la cola es infinito o aún hay espacio
    #             # if queue size is infinite or there is still space
    #             self.queue.append(paquete.get_size())
    #             self.logger.log_queue_length(self, len(self.queue))
    #         else:
    #             # si ya no hay espacio, depreciamos y agregamos un log
    #             # if there is no space left, we drop the packet and log
    #             self.logger.log_queue_drop(self, paquete.get_size())


    # def handle_end_proc_msg1(self, event):
    #     """
    #     Se inicia la tx del paquete una vez concluido el proceso de RA
    #     Handles the transmission of pkg once the RA has finished
    #     """
    #     assert (self.state == Node.PROC_RA)
    #     self.transmit_packet(packet_size=500)
    #     self.state = Node.TX
    #     self.logger.log_state(self, Node.TX)

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

    def get_state(self):
        """
        Returns y position
        :returns: y position in meters
        """
        return self.state
