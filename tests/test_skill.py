import json
from unittest import TestCase
from mock import mock, patch

from snipshue.snipshue import SnipsHue


class SnipsHueGetRequests(TestCase):
    @patch.object(SnipsHue, '_get_rooms_lights')
    def setUp(self, mock_rooms_lights):
        self.hostname = "192.168.1.1"
        self.username = "username"
        self.lights_id = range(1, 5)

        mock_rooms_lights.return_value = dict()

        self.skill = SnipsHue(self.hostname, self.username, self.lights_id)

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch('requests.put')
    def test_post_state(self, mock_put, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])
        skill._post_state(dict(), 1)

        mock_put.assert_called_with(self.skill.lights_endpoint + "/1/state", data=json.dumps(dict()), headers=None)

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch('requests.put')
    def test_post_state_room_none(self, mock_put, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        self.skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])

        self.skill._post_state(dict(), None)
        self.assertFalse(mock_put.called)

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch('requests.put')
    def test_post_state_dict_none(self, mock_put, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        self.skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])

        self.skill._post_state(None, 1)
        self.assertFalse(mock_put.called)

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch('requests.put')
    def test_post_state_dict_none_room_none(self, mock_put, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        self.skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])

        self.skill._post_state(None, None)
        self.assertFalse(mock_put.called)

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch.object(SnipsHue, '_post_state')
    def test_post_state_to_ids(self, mock_post_state, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])
        lights_id = range(1, 3)
        skill._post_state_to_ids(dict(), lights_id)

        self.assertEqual(mock_post_state.call_count, len(lights_id))

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch.object(SnipsHue, '_post_state')
    def test_post_state_to_ids(self, mock_post_state, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])
        skill._post_state_to_ids(dict(), None)

        self.assertFalse(mock_post_state.called)

    @patch.object(SnipsHue, '_get_rooms_lights')
    def test_get_hue_saturation(self, mock_get_rooms_lights):
        mock_get_rooms_lights.return_value = dict()

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3])
        self.assertIsNotNone(skill._get_hue_saturation(None))

    class false_response():
        def __init__(self, content):
            self.content = content
        def json(self):
            return self.content


    @patch('requests.get')
    def test_get_rooms_lights_simple(self, mock_request_get):
        mock_request_get.return_value = self.false_response({
            '1': {
                'name': 'room_name',
                'class': 'Office',
                'lights': ['1', '2', '3', '4', '5', '6']
            },
            '2': {'class': 'Bedroom', 'lights': []},
            '3': {'class': 'Kitchen', 'lights': ['1']}
        })

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])

        result = skill._get_rooms_lights()

        self.assertTrue(mock_request_get.called)
        self.assertEqual(result["Office"], ['1', '2', '3', '4', '5', '6'])
        self.assertEqual(result["Bedroom"], [])
        self.assertEqual(result["Kitchen"], ['1'])

    @patch('requests.get')
    def test_get_rooms_lights_empty(self, mock_request_get):
        mock_request_get.return_value = self.false_response({})

        skill = SnipsHue("192.168.1.1", "username", [1, 2, 3, 4, 5])
        result = skill._get_rooms_lights()
        self.assertTrue(mock_request_get.called)

    @patch('requests.get')
    def test_get_lights_ids_from_rooms(self, mock_request_get):
        mock_request_get.return_value = self.false_response({
            '1': {
                'name': 'room_name',
                'class': 'Office',
                'lights': ['1', '2', '3', '4', '5', '6']
            },
            '2': {'class': 'Bedroom', 'lights': []},
            '3': {'class': 'Kitchen', 'lights': ['1']}
        })

        skill = SnipsHue("192.168.1.1", "username", [1, 2, '3', 4, '5'])
        self.assertEqual(skill._get_light_ids_from_room("Bedroom"), []) 
        self.assertEqual(skill._get_light_ids_from_room("Office"), ['1', '2', '3', '4', '5', '6']) 
        self.assertEqual(skill._get_light_ids_from_room("Kitchen"), ['1']) 
        self.assertEqual(skill._get_light_ids_from_room("Unknown"), ['1', '2', '3', '4', '5']) 

    @patch.object(SnipsHue, '_get_rooms_lights')
    @patch('requests.get')
    def test_get_lights_config(self, mock_request_get, mock_get_rooms_lights):
        response_state = {
            u'on': True,
            u'hue': 9509,
            u'colormode': u'hs',
            u'effect': u'none',
            u'alert': u'none',
            u'xy': [0.0, 0.0],
            u'reachable': False,
            u'bri': 254,
            u'ct': 432,
            u'sat': 254
        }
        mock_request_get.return_value = self.false_response({u'state': response_state})

        skill = SnipsHue("192.168.1.1", "username", ['1', '2', '3'])
        self.assertEqual(skill._get_lights_config(['1']), {'1': response_state})
        self.assertEqual(skill._get_lights_config(['1', '2']), {'1': response_state, '2': response_state})
        self.assertEqual(skill._get_lights_config(['xx']), {'xx': response_state})

    @patch.object(SnipsHue, '_get_rooms_lights')
    def test_color_map(self, mock_get_rooms_lights):
        skill = SnipsHue("192.168.1.1", "username", ['1', '2', '3'])

        self.assertEqual(skill._get_hue_saturation('red'), {'hue': 2869, 'sat': 255})
        self.assertEqual(skill._get_hue_saturation('blue'), {'hue': 44161, 'sat': 255})
        self.assertEqual(skill._get_hue_saturation('green'), {'hue': 21845, 'sat': 255})

    def tearDown(self):
        pass

class SnipsHuePostRequests(TestCase):
    def tearDown(self):
        pass

