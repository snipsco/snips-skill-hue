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

    def __init__(self):
        print "init...: "
        bridge_ips = self._get_bridge_ips()

        username = None
        for bridge_ip in bridge_ips:
            username = self._get_cached_username(bridge_ip)
            if username is not None:
                break

        print "Cached username: " + str(username)

        if username is None or not self._is_connected(bridge_ip, username):
            username = self._connect_user(bridge_ip)

        self.bridge_url = self._create_url(bridge_ip, username)

        self._set_cache(bridge_ip, username)

    def _get_bridge_ips(self):
        response = requests.get('http://www.meethue.com/api/nupnp').json()
        bridge_ips = []
        for ip in response:
            bridge_ips.append(ip["internalipaddress"])

        print "bridge ips {}".format(bridge_ips)

        return bridge_ips

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

    def _get_cached_username(self, bridge_ip):
        username = None
        print "path to cache: {}{}".format(path_cache_folder, cache_file_name)
        try:
            f = open(path_cache_folder + cache_file_name, 'rw')

            content = f.read()
            try:
                content = json.loads(content)
            except ValueError, e:
                content = {}

            username = content.get(bridge_ip)
            f.close()
        except IOError:
            print "No cached data were found" 
        return username

    def _create_file_if_not_exist(self, path, filename):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        open(path + filename, 'w+').close()

    def _set_cache(self, bridge_ip, username):
        self._create_file_if_not_exist(path_cache_folder, cache_file_name)
        f = open(path_cache_folder + cache_file_name, 'r+')
        content = f.read()

        if type(content) == dict:
            content = json.loads(content)
        else:
            content = {}

        content[bridge_ip] = username

        content = json.dumps(content)
        f.write(content)
        f.close()

    def _connect_user(self, bridge_ip):
        created = False

        print '/!\ Please, press the button on the Hue bridge'

        while not created:
            payload = json.dumps({'devicetype': 'snipshue'})
            # response = requests.Post(resource)['resource']
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

HueSetup()
