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
import copy
from module import Module
from event import Event
from events import Events

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
