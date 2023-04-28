#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1

class ina219:

    def __init__(self):
        self.ina = INA219(SHUNT_OHMS)
        self.ina.configure()

    def get_voltage(self):
        try:
            return "%.3f V" % self.ina.voltage()
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            return "ERROR"

    def get_current(self):
        try:
            return "%.3f mA" % self.ina.current()
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            return "ERROR"

    def get_power(self):
        try:
            return "%.3f mW" % self.ina.power()
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            return "ERROR"

    def get_shunt_voltage(self):
        try:
            return "%.3f mV" % self.ina.shunt_voltage()
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)
            return "ERROR"