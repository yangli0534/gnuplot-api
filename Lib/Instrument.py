# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import pyvisa


class Instrument(object):
    def __init__(self, instr_addr):
        #self.instr_name = instr_name
        # self.ctrl_mode = ctrl_mode
        # self.ip_addr = ip_addr
        # self.gpib_addr = gpib_addr
        # check GPIB or LAN?
        # if self.ctrl_mode == 'GPIB':
        #     self.addr = 'GPIB0::' + self.gpib_addr + '::INSTR'
        # else:
        #     self.addr = 'TCPIP0' + self.ip_addr + 'inst0::INSTR'
        #self.instr_addr = instr_addr
        # def create(self, ctrl_mode, ip_addr, gpib_addr):
        rm = pyvisa.ResourceManager()
        self._instr = rm.open_resource(instr_addr)
        # instr.write('*IDN')
        # print(instr.read())
        # return instr
        self.name = self._instr.query('*IDN?')[:-1]
        self.init()

    def write_value(self, cmd):
        self._instr.write(cmd)

    def read_value(self, cmd):
        self.write_value(cmd)
        return self._instr.read()

    def cal(self):
        self.write_value(':CAL')

    def cls(self):
        self.write_value(':CLS')

    def rst(self):
        self.write_value('*RST')

    def stb(self):
        return self.read_value('*STB?')

    def init(self):
        self.rst()
        self.cls()
        self.cls()
        self.cal()


class SA(Instrument):
    def __init__(self, instr_addr):
        Instrument.__init__(self,instr_addr)
        self._sa = Instrument._instr
        self.init()

    def mode_sa(self):
        self._sa.write_value('INST SA')
    def conf_acp(self):
        self._sa.write_value('CONF: ACP')

    def init(self):
        self.mode_sa()
        self.conf_acp()