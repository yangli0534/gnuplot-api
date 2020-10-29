# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""



import sys

sys.path.append(r'..\Station')
sys.path.append(r'..\Lib')
sys.path.append(r'..\Radio')
sys.path.append(r'..\Common')

import PS
import SA
import PM
import RU
import matplotlib.pyplot as plt
import time
import math
from datetime import datetime
import logging
import Station


import numpy as np
import pandas as pd

class Station(object):

    def __init__(self):

        self.logger = logging.getLogger('root')
        tx_freq = pd.read_csv(r'../station/TX_CABLE_IL.csv', skiprows=[1, 2], usecols=[0])
        tx_IL = pd.read_csv(r'../station/TX_CABLE_IL.csv', skiprows=[1, 2], usecols=[1])
        tx_freq = np.array(tx_freq)
        tx_freq = tx_freq.reshape(tx_freq.size)
        self.tx_freq_list = tx_freq.tolist()
        tx_IL = np.array(tx_IL)+0.05
        tx_IL = tx_IL.reshape(tx_IL.size)
        self.tx_IL_list = tx_IL.tolist()

        rx_freq = pd.read_csv(r'../station/RX_CABLE_IL.csv', skiprows=[1, 2], usecols=[0])
        rx_IL = pd.read_csv(r'../station/RX_CABLE_IL.csv', skiprows=[1, 2], usecols=[1])
        rx_freq = np.array(rx_freq)
        rx_freq = rx_freq.reshape(rx_freq.size)
        self.rx_freq_list = rx_freq.tolist()
        rx_IL = np.array(rx_IL)+0.05
        rx_IL = rx_IL.reshape(rx_IL.size)
        self.rx_IL_list = rx_IL.tolist()

        instr = pd.read_csv(r'../station/STATION_CONFIG.csv', usecols=[0,1])
        self.__instr= dict(zip(list(instr.INSTR_ID), list(instr.INSTR_ADDR)))
        # instr_addr = pd.read_csv(r'../station/STATION_CONFIG.csv', usecols=[1])
        # instr_id = np.array(instr_id)
        # instr_id = instr_id.reshape(instr_id.size)
        # self.instr_id = instr_id.tolist()
        # instr_addr = np.array(instr_addr)
        # instr_addr = instr_addr.reshape(instr_addr.size)
        # self.instr_addr = instr_addr.tolist()

    def __del__(self):
        print('')
    def get_tx_IL(self, freq):

        return np.interp(freq*1e6, self.tx_freq_list, self.tx_IL_list)

    def get_rx_IL(self, freq):

        return np.interp(freq*1e6, self.rx_freq_list, self.rx_IL_list)

    def get_instr_addr(self, instr_id):
        if instr_id in self.__instr:
            addr = self.__instr[instr_id]
            if (addr != '#') and (addr !=''):
                return addr
            else:
                self.logger.critical(f'No {instr_id} is available')
        else:
            self.logger.critical(f'No {instr_id} is available')

if __name__ == '__main__':
    mybench = Station()
    print(mybench.get_tx_IL(3700))
    #print(mybench.freq_list)
    #print(mybench.IL_list)

    print(mybench.get_rx_IL(3700))
    print(mybench.get_instr_addr('SA'))