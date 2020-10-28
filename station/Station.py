# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import numpy as np
import pandas as pd

class Station(object):

    def __init__(self):
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

        # for key, value in IL_TX.items():
        #     self.freq_list.append(key)
        #     self.IL_list.append(value)

    def __del__(self):
        print('')
    def get_tx_IL(self, freq):

        return np.interp(freq*1e6, self.tx_freq_list, self.tx_IL_list)

    def get_rx_IL(self, freq):

        return np.interp(freq*1e6, self.rx_freq_list, self.rx_IL_list)

if __name__ == '__main__':
    mybench = Station()
    print(mybench.get_tx_IL(3700))
    #print(mybench.freq_list)
    #print(mybench.IL_list)

    print(mybench.get_rx_IL(3700))