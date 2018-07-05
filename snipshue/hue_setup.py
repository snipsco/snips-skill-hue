import requests
import json
import os
import errno
import sys

cache_file_name = 'credentials.json'
path_cache_folder = os.path.expanduser('~/.snips/philips_hue/')

class HueSetup:
    """ Get or create infos to connect to Philips Hue """

    bridge_url = None
    username = None

    def __init__(self, bridge_ip=None, username=None):
        if bridge_ip is None:
            bridge_ip = self._get_bridge_ip()
            username = None
        if username is None or not self._is_connected(bridge_ip, username):
            username = self._connect_user(bridge_ip)
        self.bridge_url = self._create_url(bridge_ip, username)
        self.username = username
        self.bridge_ip = bridge_ip

    def get_username(self):
        return self.username

    def get_bridge_ip(self):
        return self.bridge_ip

    def _get_bridge_ip(self):
        response = requests.get('http://www.meethue.com/api/nupnp').json()
        if type(response) is list:
            return response[0]["internalipaddress"]
        else:
            return response["internalipaddress"]

    def _is_connected(self, bridge_ip, username):
        is_connected = False
        resource = {'which':'system'}
        response = requests.get(self._create_url(bridge_ip, username)).json()
        if 'lights' in response:
            print 'Connected to the Hub'
            is_connected = True
        elif 'error' in response[0]:
            error = response[0]['error']
            if error['type'] == 1:
                is_connected = False
        return is_connected

    def _connect_user(self, bridge_ip):
        created = False
        print '/!\ Please, press the button on the Hue bridge'
        while not created:
            payload = json.dumps({'devicetype': 'snipshue'})
            response = requests.post("http://" + bridge_ip + "/api", data=payload).json()
            if 'error' in response[0]:
                if response[0]['error']['type'] != 101:
                    print 'Unhandled error creating configuration on the Hue'
                    sys.exit(response)
            else:
                username = response[0]['success']['username']
                created = True
        print 'User connected'
        return (username)

    def _create_url(self, bridge_ip, username):
        return 'http://{}/api/{}'.format(bridge_ip, username)
