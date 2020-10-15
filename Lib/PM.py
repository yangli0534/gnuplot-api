# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:22:56 2020

@author: Integration
"""
import pyvisa
import time
import datetime

class PM:
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # instr = rm.open_resource('GPIB0::18::INSTR')
        self._instr = rm.open_resource(address)
        self._instr.timeout = 10000
        self.name = self._instr.query('*IDN?')[:-1]
        self.set_init()


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
        self.set_rst()

        #self.set_cal()
        #self.take_one_sweep()
        self.set_cls()
        #self.set_unit()

    def set_close(self):
        self._instr.close()

    def get_staus(self):

        cmd = f'*OPC?'
        return self.read_value(cmd)

    def set_zero(self):
        cmd = f'CAL:ZERO:AUTO ONCE'
        self.write_value(cmd)

    def get_power(self):
        cmd = f'MEAS?'
        return self.read_value(cmd)

if __name__ == '__main__':
    mypm = PM('GPIB0::13::INSTR')
    print(mypm.name)
    #mypm.set_zero()
    power = mypm.get_power()
    print(power)
    print(f'The power is {power} dBm')
    if(mypm.get_staus() == [1]):
        print('Job finished')
    else:
        print('Job ongoing')
    #print(mypm.get_staus())