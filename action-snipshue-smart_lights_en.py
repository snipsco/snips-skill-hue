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

API_KEY = "api_key"

class Skill:

    def __init__(self):
        config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        hostname = None
        code = None
        if config.get('secret') is not None:
            if config.get('secret').get('hostname') is not None:
                hostname = config.get('secret').get('hostname')
                if hostname == "":
                    hostname = None
            if config.get('secret').get(API_KEY) is not None:
                code = config.get('secret').get(API_KEY)
                if code == "":
                    code = None
        if hostname is None or code is None:
            print('No configuration')
        self.snipshue = SnipsHue(hostname, code)
        hostname = self.snipshue.hostname
        code  = self.snipshue.username
        self.update_config(CONFIG_INI, config, hostname, code)
        self.queue = Queue.Queue()
        self.thread_handler = ThreadHandler()
        self.thread_handler.run(target=self.start_blocking)
        self.thread_handler.start_run_loop()

    def update_config(self, filename, data, hostname, code):
        data['secret']['hostname'] = hostname
        data['secret'][API_KEY] = code
        SnipsConfigParser.write_configuration_file(filename, data)

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
    def extract_number(self, intent_message, default_number):
        number = default_number
        if intent_message.slots.intensity_number:
            number = intent_message.slots.intensity_number.first().value
        if intent_message.slots.intensity_percent:
            number = intent_message.slots.intensity_percent.first().value
        return number

    def extract_up_down(self, intent_message):
        res = "down"
        if intent_message.slots.up_down:
            res = intent_message.slots.up_down.first().value
        return res

    def callback(self, hermes, intent_message):
        rooms = self.extract_house_rooms(intent_message)
        if intent_message.intent.intent_name == 'lightsTurnOff':
            self.queue.put(self.lights_turn_off(hermes, intent_message, rooms))
        if intent_message.intent.intent_name == 'lightsTurnOnSet':
            self.queue.put(self.lights_turn_on_set(hermes, intent_message, rooms))
        if intent_message.intent.intent_name == 'lightsShift':
            self.queue.put(self.lights_shift(hermes, intent_message, rooms))
        if intent_message.intent.intent_name == 'lightsSet':
            self.queue.put(self.lights_turn_on_set(hermes, intent_message, rooms))

    def lights_turn_off(self, hermes, intent_message, rooms):
        hermes.publish_end_session(intent_message.session_id, None)
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_off(room)
        else:
            self.snipshue.light_off(None)

    def lights_turn_on_set(self, hermes, intent_message, rooms):
        hermes.publish_end_session(intent_message.session_id, None)
        number = self.extract_number(intent_message, 100)
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_on_set(None, number, room)
        else:
            self.snipshue.light_on_set(None, number, None)

    def lights_shift(self, hermes, intent_message, rooms):
        hermes.publish_end_session(intent_message.session_id, None)
        number = self.extract_number(intent_message, 20)
        if "down" == self.extract_up_down(intent_message):
            self.lights_turn_down(number, rooms);
        else:
            self.lights_turn_up(number, rooms);

    def lights_turn_down(self, number, rooms):
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_down(number, room)
        else:
            self.snipshue.light_down(number, None)

    def lights_turn_up(self, number, rooms):
        if len(rooms) > 0:
            for room in rooms:
                self.snipshue.light_up(number, room)
        else:
            self.snipshue.light_up(number, None)

if __name__ == "__main__":
    Skill()
