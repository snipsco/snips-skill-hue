#!/usr/bin/env python3
# encoding: utf-8

import requests
import json
import time


class SnipsHue:

    def __init__(self, hostname, username, light_ids):
        """
        :param hostname: Philips Hue hostname
        :param username: Philips Hue username
        :param light_ids: Philips Hue light ids
        """
        self.endpoint = 'http://{}/api/{}/lights'.format(hostname, username)
        self.light_ids = light_ids

    def turn_on(self):
        """ Turn on all Philips Hue lights. """
        self.post_state_all({"on": True})

    def turn_off(self):
        """ Turn off all Philips Hue lights. """
        self.post_state_all({"on": False})

    def set_color_name(self, color):
        """ Set the light color for all lights.
        
        :param color: A color name, e.g. "red" or "blue"
        """
        params = self.get_HSR(color)
        params["on"] = True
        self.post_state_all(params)

    def post_state_all(self, params):
        """ Post a state update to all Philips Hue lights.
        
        :param params: Philips Hue request parameters.
        """
        p = dict((k, v) for k, v in params.iteritems() if v != None)
        for light_id in self.light_ids:
            self.post_state(p, light_id)
            time.sleep(0.2)

    def post_state(self, params, light_id):
        """ Post a state update to a given light.
        
        :param params: Philips Hue request parameters.
        :param light_id: Philips Hue light ID.
        """
        print("[HUE] Setting state for light " +
              str(light_id) + ": " + str(params))
        try:
            requests.put("{0}/{1}/state".format(self.endpoint,
                                                light_id), data=json.dumps(params), headers=None)
        except:
            print("[HUE] Request timeout. Is the Hue Bridge reachable?")
            pass

    def get_HSR(self, color_name):
        """ Transform a color name into a dictionary represenation
            of a color, as expected by the Philips Hue API.
        
        :param color_name: A color name, e.g. "red" or "blue"
        :return: A dictionary represenation of a color, as expected
            by the Philips Hue API, e.g. {'hue': 65535, 'sat': 254, 'bri': 254}
        """
        if color_name == 'red':
            return {'hue': 65535, 'sat': 254, 'bri': 254}
        elif color_name == 'green':
            return {'hue': 25500, 'sat': 254, 'bri': 254}
        elif color_name == 'blue':
            return {'hue': 46920, 'sat': 254, 'bri': 254}
        return {'hue': 0, 'sat': 0, 'bri': 254}
