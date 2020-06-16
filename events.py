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


class Events:
    """
    Define los tipos de eventos para la simulación
    Defines event types for the simulation
    """

    # comienza la transmisión de un paquete
    # start transmission event
    START_TX = 0
    # finaliza la transmisión de un paquete
    # end transmission event
    END_TX = 1
    # comienza el event de recepción
    # start reception event
    START_RX = 2
    # finaliza el evento de recepción
    # end reception event
    END_RX = 3
    # evento de arribo de paquete
    # packet arrival event
    PACKET_ARRIVAL = 4
    # finalia el procesamiento despues de la recepción de un paquete. puede comenzar a operar nuevamente
    # end of processing after reception or transmission. can start operations again
    END_PROC = 5
    # finalia el procesamiento despues de la recepción del msg1. puede comenzar a operar nuevamente
    # end of processing after reception or MSG1. can start operations again
    END_PROC_MSG1 = 5
    # expiración para el tiempo de recepción, evitando esperar por siempre
    # timeout for RX state avoiding getting stuck into RX indefinitely
    RX_TIMEOUT = 6
    # proceso de RA en el canal NPRACH
    # processing RA
    PERIODO_NPRACH = 7
    # proceso NOMA
    # processing NOMA in the corrent Ts
    PERIODO_NOMA = 8
    # comienza la transmisión del msg1
    # start the transmision of the msg1
    START_TX_MSG1 = 9
    # finaliza la transmisión del msg1
    # end tx of msg1
    END_TX_MSG1 = 10
    END_PROC_MSG1 = 11
