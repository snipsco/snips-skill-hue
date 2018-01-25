# -*-: coding utf-8 -*-
""" Leds service for handling visual feedback for various states of
    the system. """

import time
import struct
import random

from usb.core import USBError

from usb_utils import USB

try:
    import respeaker.usb_hid as usb_hid
except USBError:
    print("Error accessing microphone: insufficient permissions. " +
          "You may need to replug your microphone and restart your device.")


class ReSpeakerAnimator(object):
    class State:
        """ Leds states.- """
        waiting_to_connect = range(1)

    def __init__(self):
        self.hid = usb_hid.get()

        def value(led, frame):
            if led == frame:
                return 255
            else:
                return 0

        self.animation_waiting_to_connect = []
        N = 15
        for frame in range(0, N):
            state = {}
            for led_index in range(0, N):
                color = self.color_to_int((value(led_index, frame) + 255) % 256, value(led_index, frame), 0)
                state.update({led_index + 3 : color})
            self.animation_waiting_to_connect.append(state)

        # Set the ReSpeaker in the right mode
        try:
            init_addr = 0  # 0x0
            init_data = 6  # 0x00000006

            self.write(init_addr, init_data)
        except Exception as e:
            print(e.message)

    def write(self, address, data):
        if data > 0xFFFF:
            data = struct.pack('<I', data)
        elif data > 0xFF:
            data = struct.pack('<H', data)

        data = self.to_bytearray(data)
        length = len(data)
        if self.hid:
            packet = bytearray([address & 0xFF, (address >> 8) &
                                0x7F, length & 0xFF, (length >> 8) & 0xFF]) + data
            packet = list(packet)
            self.hid.write(packet)

    def read(self, address, length):
        if self.hid:
            self.hid.write(list(bytearray(
                [address & 0xFF, (address >> 8) & 0xFF | 0x80, length & 0xFF, (length >> 8) & 0xFF])))
            for _ in range(6):
                data = self.hid.read()
                # skip VAD data
                if int(data[0]) != 0xFF and int(data[1]) != 0xFF:
                    return data[4:(4 + length)]

    @staticmethod
    def color_to_int(r, g, b):
        return (r << 16) | (g << 8) | b
    @staticmethod
    def to_bytearray(data):
        if type(data) is int:
            array = bytearray([data & 0xFF])
        elif type(data) is bytearray:
            array = data
        elif type(data) is str:
            array = bytearray(data)
        elif type(data) is list:
            array = bytearray(data)
        else:
            raise TypeError('%s is not supported' % type(data))

        return array

    def run(self, animation):
        if animation == self.State.waiting_to_connect:
            for item in self.animation_waiting_to_connect:
                for k, v in item.items():
                    self.write(k, v)
                time.sleep(0.1)

if __name__ == "__main__":
    led_service = ReSpeakerAnimator()
    led_device = USB.get_boards()
    # if led_device == USB.Device.respeaker:
    #     animator = ReSpeakerAnimator()
    # else:
    #     animator = None
    while True:
        led_service.run(led_service.State.waiting_to_connect)
        time.sleep(0.8)
