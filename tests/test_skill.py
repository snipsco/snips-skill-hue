from unittest import TestCase

from snipshue.snipshue import SnipsHue


class TestSkill(TestCase):

    def setUp(self):
        self.skill = SnipsHue("192.168.163.96",
                              "XyWT7TlG3RkMAzbKRt4fWpHEo1TudukIgH2OKz79",
                              [])

    def test_skill(self):
        self.skill.turn_on()
        self.assertEqual(1, 1)
