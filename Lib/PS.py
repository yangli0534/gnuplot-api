# -*- coding: utf-8 -*-
"""
Created on Tue Oct  20 14:22:56 2020

@author: Integration
"""

import pyvisa
import time
import datetime

class PS:
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # instr = rm.open_resource('GPIB0::18::INSTR')
        self._instr = rm.open_resource(address)
        self._instr.timeout = 10000
        self.name = self._instr.query('*IDN?')[:-1]
        self.set_init()
        print(f'{self.name} has been connected successfully' )


    def write_value(self, cmd):
        self._instr.write(cmd)

    def read_value(self, cmd):
        self.write_value(cmd)
        return self._instr.read_ascii_values()

    def set_cal(self):
        self.write_value(f':CAL')

    def set_cls(self):
        self.write_value(f'*CLS')

    def set_rst(self):
        self.write_value(f'*RST')

    def get_stb(self):
        return self.read_value(f'*STB?')

    def set_init(self):
        #self.set_rst()

        #self.set_cal()
        #self.take_one_sweep()
        self.set_cls()
        #self.set_unit()
        self.set_vol(48)
        self.set_curr(8)
        self.set_ovp(55)

    def set_close(self):
        self._instr.close()

    def get_staus(self):

        cmd = f'*OPC?'
        return self.read_value(cmd)
    def turn_on(self):
        cmd = f'OUTPut:STATe ON'
        self.write_value(cmd)

    def turn_off(self):
        cmd = f'OUTPut:STATe OFF'
        self.write_value(cmd)

    def set_vol(self, target = 48):
        cmd = f'VOLT:AMPL {target}V'
        self.write_value(cmd)

    def set_curr(self, target = 8):
        cmd = f'CURR:AMPL {target}'
        self.write_value(cmd)

    def set_ovp(self, target = 55):
        cmd = f'VOLT:PROT {target}'
        self.write_value(cmd)

    def get_vol(self):
        cmd = f'MEAS:VOLT?'
        return self.read_value(cmd)[0]

    def get_curr(self):
        cmd = f'MEAS:CURR?'
        return self.read_value(cmd)[0]

    def get_consumption(self):
        # print(self.get_vol())
        # print(self.get_curr())
        # print(type(self.get_vol()))
        # print(type(self.get_curr()))
        return self.get_vol()* self.get_curr()

    def __del__(self):
        self.set_close()
        print('PS has been disconnected')

if __name__ == '__main__':
    myps = PS('TCPIP0::172.16.1.57::inst0::INSTR')
    print(myps.name)
    #myps.turn_on()
    #time.sleep(10)
    print(myps.get_consumption())
    myps.set_close()