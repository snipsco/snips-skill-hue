#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
from snipshue.snipshue import SnipsHue
from snipshelpers.thread_handler import ThreadHandler
from snipshelpers.config_parser import SnipsConfigParser
import Queue

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


class Skill:

    def __init__(self):
        config = SnipsConfigParser.read_configuration_file(CONFIG_INI)

        hostname = None
        code = None
        if config.get('secret') is not None:
            if config.get('secret').get('hostname') is not None:
                hostname = config.get('secret').get('hostname')
        else:
            print('No configuration')

        self.snipshue = SnipsHue(hostname, code)
        self.queue = Queue.Queue()

        self.thread_handler = ThreadHandler()
        self.thread_handler.run(target=self.start_blocking)
        self.thread_handler.start_run_loop()

    def start_blocking(self, run_event):
        while run_event.is_set():
            try:
                self.queue.get(False)
            except Queue.Empty:
                with Hermes(MQTT_ADDR) as h:
                    h.subscribe_intents(self.callback).start()

    def extract_house_rooms(self, intent_message):
        house_rooms = []
        if intent_message.slots.house_room is not None:
            for room in intent_message.slots.house_room:
                house_rooms.append(room.slot_value.value.value)
        return house_rooms

    def callback(self, hermes, intent_message):
        rooms = self.extract_house_rooms(intent_message)
        if intent_message.intent.intent_name == 'lightsTurnOff':
            self.queue.put(self.lights_turn_off(hermes, intent_message, rooms))
        if intent_message.intent.intent_name == 'lightsSet':
            self.queue.put(self.lights_turn_on_set(hermes, intent_message, rooms))

    def lights_turn_off(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_off(room)
        else:
            self.snipshue.light_off(None)

        hermes.publish_end_session(intent_message.session_id, None)

    def lights_turn_down(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_down(20, room)
        else:
            self.snipshue.light_down(20, None)

        hermes.publish_end_session(intent_message.session_id, None)

    def lights_turn_on_set(self, hermes, intent_message, rooms):
        number = intent_message.slots.number.first().value if intent_message.slots.number else None

        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_on_set(None, number, room)
        else:
            self.snipshue.light_on_set(None, number, None)

            hermes.publish_end_session(intent_message.session_id, None)

    def lights_turn_up(self, hermes, intent_message, rooms):
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_up(20, room)
        else:
            self.snipshue.light_up(20, None)

        hermes.publish_end_session(intent_message.session_id, None)



                


if __name__ == "__main__":
    Skill()
