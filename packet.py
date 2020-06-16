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


class Packet:
    """
    Clase definiendo un paquete que se asocia a la transisión de un evento
    Class defining a packet to be associated with a transmission event
    """

    # usado para crear un único ID para cada paquete
    # used to create a unique ID for the packet
    __packets_count = 0

    # posibles estados para cada paquete
    # possible packet states


    # packet currently under reception
    PKT_RECEIVING = 0
    # packet has been correctly received
    PKT_RECEIVED = 1
    # packet has been corrupted due to, for example, a collision
    PKT_CORRUPTED = 2
    estados=['recibiendo','recibido','corrupto']

    def __init__(self, size, duration):
        """
        Crea un paquete asignando automáticamente un ID único.
        Creates a packet automatically assigning a unique ID to it.
        :param size: tamaño del paquete en bytes | size of the packet in bytes
        :param duration: duración del paquete en segundos | packet duration in seconds
        """
        self.size = size
        self.duration = duration
        self.state = Packet.PKT_RECEIVING
        self.id = Packet.__packets_count
        Packet.__packets_count = Packet.__packets_count + 1

    def get_id(self):
        """
        Retorna el id del paquete.
        Returns packet id.
        :returns: id del paquete | id of the packet
        """
        return self.id

    def get_state(self):
        """
        Retorna estado de un paquete.
        Returns state of a packet.
        :returns: estado del paquete | state of the packet
        """
        return self.state

    def set_state(self, state):
        """
        Establece estado del paquete.
        Sets packet state.
        :param state: puede ser PKT_RECEIVING, PKT_RECEIVED, o PKT_CORRUPTED | either PKT_RECEIVING, PKT_RECEIVED, or PKT_CORRUPTED
        """
        self.state = state

    def get_size(self):
        """
        Retorna el tamaño del paquete.
        Returns packet size.
        :returns: tamaño del paquete en bytes | packet size in bytes
        """
        return self.size

    def get_duration(self):
        """
        Retorna duración del paquete.
        Returns packet duration.
        :returns: duración del paquete en segundos | packet duration in seconds
        """
        return self.duration

    def dump_packet(self):
        """
        Imprime el paquete en un formato entendible para los lectores.
        Prints the packet in a human readable format.
        """
        if self.state == Packet.PKT_RECEIVING:
            t = "UNDER RECEPTION"
        elif self.state == Packet.PKT_RECEIVED:
            t = "CORRECTLY RECEIVED"
        elif self.state == Packet.PKT_CORRUPTED:
            t = "CORRUPTED"
        print("Packet state: %s\n\n" % t)
