from unittest import TestCase

from snipshue.snipshue import SnipsHue


class HueConfig():

    def __init__(self, hostname, username, light_ids):
        self.hostname = hostname
        self.username = username
        self.light_ids = light_ids


class TestSkill(TestCase):

    def setUp(self):
        config = HueConfig("192.168.163.96",
                           "XyWT7TlG3RkMAzbKRt4fWpHEo1TudukIgH2OKz79",
                           []
                           )
        self.skill = SnipsHue(config)

    def test_skill(self):
        self.skill.turn_on()
        self.assertEqual(1, 1)
