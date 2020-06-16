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

from events import Events


class Event:
    """
    Define la estructura básica de un evento
    Defines the basic structure of an event
    """
    # contador utilizado para asignar id's únicos a cada evento
    # counter used for assigning unique IDs to events
    event_counter = 0

    def __init__(self, event_time, event_type, destination, source, obj=None):
        """
        Crea un evento.
        Creates an event.
        :param event_time: momento en el que el evento debe calendarizarse| time at which the event should be scheduled
        :param event_type: tipo de evento | type of event
        :param destination: módulo destino que debe ser notificado| destination module that should be notified
        :param source: módulo que genera el evento |  module generating the event
        :param obj: objeto opcional a ser asignado al evento | optional object to be attached to the event
        """
        self.event_id = Event.event_counter
        Event.event_counter += 1
        self.event_time = event_time
        self.event_type = event_type
        self.destination = destination
        self.source = source
        self.obj = obj

    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        if other.event_id == self.event_id:
            return True
        return False

    def __lt__(self, other):
        # si el evento es el mismo, no es menor a si mismo
        # if the event is the same, it is not lower than itself
        if other.event_id == self.event_id:
            return False
        if self.event_time < other.event_time:
            return True
        if self.event_time > other.event_time:
            return False
        # si el tiempo es exactamente el mismo, aquel con el id menor es el menor de los dos
        # if the time is exactly the same, the one with the lower id is the
        # lowest of the two
        return self.event_id < other.event_id

    def get_time(self):
        """
        Retorna el tiempo del evento.
        Returns event time.
        """
        return self.event_time

    def get_type(self):
        """
        Retorna el tipo del evento.
        Returns event type.
        """
        return self.event_type

    def get_destination(self):
        """
        Retorna el destino del evento.
        Returns event destination.
        """
        return self.destination

    def get_source(self):
        """
        Retorna la fuente del evento.
        Returns event generator.
        """
        return self.source

    def get_obj(self):
        """
        Retorna el objeto agregado al evento.
        Returns the object attached to the event.
        """
        return self.obj

    def dump_event(self):
        """
        Imprime el evento en un formato para lectores
        Prints the event in a human readable format
        """
        print("Event time: %f" % self.event_time)
        t = ""
        if self.event_type == Events.PACKET_ARRIVAL:
            t = "ARRIVAL"
        elif self.event_type == Events.START_TX:
            t = "START_TX"
        elif self.event_type == Events.START_RX:
            t = "START_RX"
        elif self.event_type == Events.END_TX:
            t = "END_TX"
        elif self.event_type == Events.END_RX:
            t = "END_RX"
        elif self.event_type == Events.END_PROC:
            t = "END_PROC"
        print("Event type: %s" % t)
        print("Source node: %d" % self.source.get_id())
        print("Destination node: %d\n" % self.destination.get_id())
