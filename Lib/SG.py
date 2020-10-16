# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:22:56 2020

@author: Integration
"""
import pyvisa
import time
import datetime
import threading

class SG:
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

    def set_freq(self, freq=3700):
        #freq unit MHz
        cmd = f'FREQ {freq} MHz'
        self.write_value(cmd)

    def get_freq(self):
        cmd = f'FREQ:CW?'
        return self.read_value(cmd)

    def set_amp(self, amp = -60):
        # amp unit dBm
        cmd = f'POW:AMPL {amp} dBm'
        self.write_value(cmd)

    def get_amp(self):
        cmd = f'POW:AMPL?'
        return self.read_value(cmd)

    def turn_on(self):
        cmd = f'OUTP:STAT ON'
        self.write_value(cmd)

    def turn_off(self):
        cmd = f'OUTP:STAT OFF'
        self.write_value(cmd)

    def get_staus(self):
        cmd = f'OUTP?'
        return self.read_value(cmd)

    def set_fm2(self, freq=5, dev=100):
        cmd = f'FM2:INT:FREQ {freq} KHz'
        self.write_value(cmd)
        cmd = f'FM2:DEV {dev} KHz'
        self.write_value(cmd)
        cmd = f'FM2:STAT ON'
        self.write_value(cmd)
    #def set_mode(self):
    def set_sg_list(self, freq_start, freq_stop, freq_step, dwell_time, amp):
        cmd = f'FREQ:MODE LIST'
        self.write_value(cmd)
        cmd = f'LIST:TYPE STEP'
        self.write_value(cmd)
        cmd = f'FREQ:STAR {freq_start} MHz'
        self.write_value(cmd)
        cmd = f'FREQ:STOP {freq_stop} MHz'
        self.write_value(cmd)
        cmd = f'SWE:POIN {freq_step} '
        self.write_value(cmd)
        cmd = f'SWE:DWEL {dwell_time} MHz'
        self.write_value(cmd)
        self.set_amp(amp)
        self.turn_on()
        cmd = f'INIT:CONT ON'
        self.write_value(cmd)

    def set_sg(self, freq, amp):
        self.set_freq(freq)
        self.set_amp(amp)
        #self.set_fm2(freq = 5, dev = 300)
        self.turn_on()
    def tmp(self):
        self.turn_off()
        print('SG is turning off')

if __name__ == '__main__':
    mysg = SG('GPIB0::20::INSTR')
    print(mysg.name)
    #mysg.set_sg(freq = 3720, amp = -20)
    mysg.set_sg_list(3680, 3720, 10, 0.5, -5)
    timer = threading.Timer(10, mysg.tmp)

    mysg.set_close()

