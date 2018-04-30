#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
from snipshue.snipshue import SnipsHue
import ConfigParser
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "conf.ini"

MQTT_IP_ADDR = "192.168.174.33"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

snipshue = None


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        print(e)
        return dict()


def lights_turn_off(hermes, intent_message):
    if len(intent_message.slots):
        for room in intent_message.slots.house_room.first().value.value:
            snipshue.light_off(room)
    else:
        snipshue.light_off(None)

    hermes.publish_end_session(intent_message.session_id, None)


def lights_turn_down(hermes, intent_message):
    if len(intent_message.slots.house_room):
        for room in intent_message.slots.house_room.first().value.value:
            snipshue.light_down(20, room)
    else:
        snipshue.light_down(20, None)

    hermes.publish_end_session(intent_message.session_id, None)


def lights_turn_on_set(hermes, intent_message):
    number = intent_message.slots.number.first().value.value if intent_message.slots.number else None

    print('turnon')
    if len(intent_message.slots.house_room):
        for room in intent_message.slots.house_room.first().value.value:
            snipshue.light_on_set(None, number, room)
    else:
        snipshue.light_on_set(None, number, None)

    hermes.publish_end_session(intent_message.session_id, None)


def lights_turn_up(hermes, intent_message):
    if len(intent_message.slots.house_room):
        for room in intent_message.slots.house_room.first().value.value:
            snipshue.light_up(20, room)
    else:
        snipshue.light_up(20, None)

    hermes.publish_end_session(intent_message.session_id, None)


if __name__ == "__main__":
    with Hermes(MQTT_ADDR) as h:
        conf = read_configuration_file(CONFIG_INI)

        if 'hostname' in conf.values() is False:
            print('No hostname specified in the conf.ini')
        if 'username' in conf.values() is False:
            print('No username specified in the conf.ini')

        hostname = conf['secret']['hostname']
        username = conf['secret']['username']
        print(username)

        global snipshue
        try:
            snipshue = SnipsHue(hostname, None)
        except Exception as e:
            print('error: ' + e)

        h.subscribe_intent('lightsTurnOff', lights_turn_off) \
            .subscribe_intent('lightsTurnOnSet', lights_turn_on_set) \
            .subscribe_intent('lightsTurnDown', lights_turn_down) \
            .subscribe_intent('lightsTurnUp', lights_turn_up) \
            .start()
