# -*-: coding utf-8 -*-
""" USB utilities. """

from __future__ import absolute_import
import os
import re
import subprocess

import usb.core
import usb.util


class USB:

    class Device:
        unknown, respeaker, conexant = range(3)

    @staticmethod
    def get_boards():
        try:
            all_devices = usb.core.find(find_all=True)
        except Exception as e:
            if str(e) != "No backend available":
                raise
            # When no USB port:
            return USB.Device.unknown



        if not all_devices:
            return USB.Device.unknown

        for board in all_devices:
            try:
                devices = board.product.lower()
                if devices.find("respeaker") >= 0:
                    return USB.Device.respeaker
                elif devices.find("conexant") >= 0:
                    return USB.Device.conexant
            except Exception as e:
                continue

        return USB.Device.unknown

    @staticmethod
    def get_usb_led_device():
        devices = USB.lsusb()
        if not devices:
            return None

        devices = devices.lower()

        if devices.find("respeaker") >= 0:
            return USB.Device.respeaker
        elif devices.find("conexant") >= 0:
            # TODO: check if this is the string to look for
            return USB.Device.conexant

        return USB.Device.unknown

    @staticmethod
    def lsusb():
        FNULL = open(os.devnull, 'w')
        try:
            # Raspberry
            return subprocess.check_output(["lsusb"])
        except:
            try:
                # OSX
                return subprocess.check_output(["system_profiler", "SPUSBDataType"])
            except:
                return None
