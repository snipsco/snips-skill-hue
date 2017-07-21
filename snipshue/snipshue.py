#!/usr/bin/env python3
# encoding: utf-8

import requests
import json


class SnipsHue:

    def __init__(self, hostname, username, light_ids):
        self.light_ids = light_ids
        self.endpoint = 'http://{}/api/{}/lights'.format(hostname, username)

    def turn_on(self):
        self.send_params({"on": True})

    def turn_off(self):
        self.send_params({"on": False})

    def set_color(self, color):
        self.send_params({"on": False})

    def send_params(self, params):
        p = dict((k, v) for k, v in params.iteritems() if v != None)
        for light in self.light_ids:
            self.set_light_state(p, light_id)
            time.sleep(0.2)

    # def get_HSR(self, intent):
    #     color = intent.objectColor
    #     if color == 'red':
    #         return {'hue': 65535, 'sat': 254, 'bri': 254}
    #     elif color == 'green':
    #         return {'hue': 25500, 'sat': 254, 'bri': 254}
    #     elif color == 'blue':
    #         return {'hue': 46920, 'sat': 254, 'bri': 254}
    #     return {'hue': 0, 'sat': 0, 'bri': 254}

    def set_light_state(self, params, light_id):
        print("[HUE] Setting state for light " +
              str(light_id) + ": " + str(params))
        try:
            requests.put("{0}/{1}/state".format(self.endpoint,
                                                light_id), data=json.dumps(params), headers=None)
        except:
            print("[HUE] Request timeout. Is the Hue Bridge reachable?")
            pass
