# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import pyvisa

class VisaInstrument():
    def __init__(self, instr_name, ctrl_mode, ip_addr, gpib_addr):
        self.instr_name = instr_name
        self.ctrl_mode = ctrl_mode
        self.ip_addr = ip_addr
        self.gpib_addr = gpib_addr
        #check GPIB or LAN?
        if self.ctrl_mode == 'GPIB':
            self.addr = 'GPIB0::' + self.gpib_addr + '::INSTR'
        else:
            self.addr = 'TCPIP0' + self.ip_addr + 'inst0::INSTR'

    #def create(self, ctrl_mode, ip_addr, gpib_addr):
        rm = pyvisa.ResourceManager()
        instr = rm.open_resource(self.addr)
        instr.write('*IDN')
        print(instr.read())
        return instr



