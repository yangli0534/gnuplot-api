# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:22:56 2020

@author: Leon
"""

import sys

sys.path.append(r'..\Station')
sys.path.append(r'..\Lib')
sys.path.append(r'..\Radio')
sys.path.append(r'..\Common')


import pyvisa
import time
import datetime
import threading
import numpy as np
import matplotlib.pyplot as plt
import cmath
from pathlib import Path
import os

import Station
import logging

class SG:
    def __init__(self, address):
        self.logger = logging.getLogger('root')
        rm = pyvisa.ResourceManager()
        # instr = rm.open_resource('GPIB0::18::INSTR')
        self._instr = rm.open_resource(address)
        self._instr.timeout = 10000
        self._instr.chunk_size = 102400
        self.name = self._instr.query('*IDN?')[:-1]
        #self.set_init()
        print(f'{self.name} has been connected successfully')


    def write_value(self, cmd):
        self._instr.write(cmd)


    def read_value(self, cmd):
        self._instr.write_value(cmd)
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

    def read_waveform(self, filename):
        waveform =[]
        #filename ="LTE_FDD_10MHz_TM3p1_fs15360000_nrb50.txt"
        #path = Path(__file__).parent / "../waveform/LTE_FDD_10MHz_TM3p1_fs15360000_nrb50.txt"
        with open(filename, 'r') as file:
            #waveform = f.readlines
            for line in file:
                waveform.append(float(line.replace('\n','')))
        #waveform = waveform.split("\n")
        file.close()
        return waveform

    def test_wv_mtone(self, sample_rate = 125e6, bandwith = 3.84e6, step = 0.5e6, rf_freq = 3000, amp = -30 ):
        # sample_rate Hz
        # bandwidth Hz
        # step　MHz
        # rf_freq MHz
        # amp dBm
        #sample_rate =125e6
        fs = sample_rate
        T = 1.0 / fs
        N = round(2.0e-3*fs)
        t = np.linspace(1, N, N) * T
        # t.transpose()
        # t = t.reshape(1,t.size)

        
        mtone_step = step
        mtone_bw = bandwith
        IQData = np.zeros(t.size)
        
        for f in np.linspace(-mtone_bw/2, mtone_bw/2, round(mtone_bw/mtone_step)):
            #print(f)
             IQData = IQData+np.exp(t.dot(2j * np.pi * f))
             
        #IQData = exp(j * 2 * pi * f1 * t) + exp(j * 2 * pi * f2 * t)
        #IQData = np.exp(t.dot(2j * np.pi * f1)) + np.exp(t.dot(2j * np.pi * f2))+ np.exp(t.dot(2j * np.pi * f3))
        #IQData = np.exp(t.dot(2j * np.pi * f1)) 
        maximum = np.max(np.concatenate((IQData.real, IQData.imag), axis=0))
        IQData = IQData / maximum * 0.7
        # IQData = IQData.reshape(1,IQData.size)
        # return IQData

        # plt.plot(t[1:100], IQData.real[1:100])
        # plt.title('waveform')
        # plt.xlabel('time:s')
        # plt.ylabel('amplitude:V  ')
        # plt.show()

        Markers = np.zeros((2, len(IQData)))
        # Markers[0,:] = np.sign(IQData.real)
        # Markers[1,:] = np.sign(IQData.imag)
        Markers = (np.vstack((np.sign(IQData.real), np.sign(IQData.imag))) + 1) / 2
        # tmp = Markers
        # Markers = np.sign(Markers)
        # Markers = (Markers + 1)/2.0
        #return Markers
        #self.write_value('SOURce:FREQuency 3000000000')
        #self.write_value('POWer -30')

        self.load_wv( IQData, 'agtsample', str(sample_rate), 'play', 'no_normscale', Markers)
        #self.write_value('OUTP:STAT ON')
        self.set_sg(rf_freq, amp)
        #return tmp

    def load_waveform(self, waveform = 'LTE20', rf_freq=3000, amp=-30):

        # rf_freq MHz
        # amp dBm
        #sample_rate = 15360000
        #print(os.getcwd())
        waveform_file = {'LTE20':'../waveform/LTE_FDD_20MHz_TM3.1_fs30720000_NDLRB100.txt',
                    'LTE5':'../waveform/LTE_FDD_5MHz_TM3.1_fs7680000_NDLRB25.txt',
                    'NR20':'../waveform/NR-FR1-TM3.1_FDD_20MHz_fs30720000.txt',
                    'NR100':'../waveform/NR-FR1-TM3.1_FDD_100MHz_fs122880000.txt'
                    }
        
        filename = waveform_file[waveform]
        waveform = self.read_waveform(filename)
        sample_rate = waveform.pop(0)
        waveform_real = np.array(waveform[::2])
        waveform_imag = np.array(waveform[1::2])
        IQData  = waveform_real + 1j * waveform_imag
        #IQData = np.array(waveform)
        #IQData = np.zeros((1, round(len(waveform)/2)))

        Markers = np.zeros((2, len(IQData)))
        # Markers[0,:] = np.sign(IQData.real)
        # Markers[1,:] = np.sign(IQData.imag)
        Markers = (np.vstack((np.sign(IQData.real), np.sign(IQData.imag))) + 1) / 2
        # tmp = Markers
        # Markers = np.sign(Markers)
        # Markers = (Markers + 1)/2.0
        # return Markers
        # self.write_value('SOURce:FREQuency 3000000000')
        # self.write_value('POWer -30')
        self.logger.info('loading waveform to SG')
        self.load_wv(IQData, filename[12:35], str(sample_rate), 'play', 'no_normscale', Markers)
        # self.write_value('OUTP:STAT ON')
        self.logger.info(' finish loading waveform to SG')
        self.set_sg(rf_freq, amp)

    def load_wv(self, IQData, ArbFileName, sample_rate, play_flag, normscale_flag, markers):

        # Input:
        #   IQData         IQ data array. This should be a 1D complex array. I+jQ.
        #   ArbFileName    Optional parameter.  The Arb file name (string).  If nothing is specified
        #                  the default is 'Untitled'
        #   sample_rate    Optional parameter.  If nothing is specified, the default sample rate is what
        #                  the signal generator is currently set to.
        #   play_flag      Optional parameter.  This parameter either plays or does not play a
        #                  waveform on the signal generator.  If a waveform shouldn't be played
        #                  specify 'no_play'.  Default is 'play'.
        #   normscale_flag Optional parameter.  Specify 'normscale' if the data is to be normalized to +/- 1 and
        #                  scaled at 70#.  Specify 'no_normscale' if the data will not be normalized and scaled
        #                  within this function.
        #   Markers        Optional parameter.  Marker is a 2D array with the size of nMarker x nIQDataLenth. Each
        #                  marker can be either 0 or 1. Default is that no markers will be set.

        if (normscale_flag.lower() == 'no_normscale'.lower()):
            maxval = np.max(abs(np.concatenate((IQData.real, IQData.imag), axis=0)))
            # return maxval
            if (maxval > 1):
                print('IQData must be in the range [ -1:1 ]')
                return

        # (m, n) = IQData.shape
        m = IQData.ndim
        n = IQData.size
        if (m != 1):
            print('IQData should be an 1xN complex array ')

        IQDataLen = IQData.size

        # Check for invalid input
        if (markers.size != 0):
            markerDim = markers.ndim
            if (markerDim != 2):
                print('markers should be a 2 D array')

            (rowMarker, colMarker) = markers.shape
            if (rowMarker == IQDataLen):
                markers = markers.transpose()
                (rowMarker, colMarker) = markers.shape

            if (colMarker != IQDataLen):
                print('markers should have the same length as IQData');
            #  Create the markers
            for i in range(IQDataLen):
                tmp = markers[:, i]
                if ((tmp == [1, 1]).all()):
                    markers[1, i] = 3
                elif ((tmp == [0, 1]).all()):
                    markers[1, i] = 2
                elif ((tmp == [1, 0]).all()):
                    markers[1, i] = 1
                else:
                    markers[1, i] = 0

            markers = markers[1, :]
        else:
            # Default markers are all zeros
            markers = np.zeros(1, IQDataLen)
        # np.sum(wave ==0)
        markers = np.uint8(markers)
        markers = list(markers.reshape(markers.size))
        
        #return markers
    
        if (not play_flag.isalpha()):
            print('play_flag should be a string')

        # Turn off the ARB so we don't damage it
        self.write_value(':SOURce:RADio:ARB:STATE OFF')

        tmp = np.column_stack((IQData.real, IQData.imag))
        wave = tmp.reshape(1, tmp.size)  # transpose and interleave the waveform

        tmp = 1  # default normalization factor = 1
        if (normscale_flag.lower() == 'normscale'.lower()):
            # select the normalization factor
            tmp = np.abs((wave.max(), wave.min())).max()
            if (tmp == 0):
                tmp = 1

        # ARB binary range is 2's Compliment -32768 to + 32767
        # So scale the waveform to +/- 32767 not 32768
        modval = 2 ** 16
        scale = 2 ** 15 - 1
        scale = scale / tmp
        wave = np.round(wave * scale)

        #  Get it from double to unsigned int and let the driver take care of Big
        #  Endian to Little Endian for you  Look at ESG in Workspace.  It is
        #  property of the VISA driver (at least Agilent's
        #  if your waveform is skrewy, suspect the NI driver of not changeing
        #  BIG ENDIAN to LITTLE ENDIAN.  The PC is BIG ENDIAN.  ESG is LITTLE
        wave = np.uint16(np.mod(modval + wave, modval))
        wave = list(wave.reshape(wave.size))
        #return wave
        # write the waveform data
        #binblockwrite(connection,wave,'uint16',[':MEMory:DATa:UNProtected "WFM1:' ArbFileName '", ']);
        cmd = f'MEMory:DATa:UNProtected "WFM1:{ArbFileName}",'
        self._instr.write_binary_values(cmd, wave, datatype ='H', is_big_endian =True)
        status = self._instr.query(':SYSTEM:ERROR?')
        if status != '+0,"No error"\n':
            print(status)
            return

        # write the marker data
        #binblockwrite(connection, markers, 'uint8', [':MEMory:DATa:UNProtected "MKR1:' ArbFileName '",']);
        cmd = f':MEMory:DATa:UNProtected "MKR1:{ArbFileName}",'
        self._instr.write_binary_values(cmd, markers, datatype ='B', is_big_endian = True)

        # query for instrument error
        status = self._instr.query(':SYSTEM:ERROR?')
        if status != '+0,"No error"\n':
            print(status)
            return

        # set the sample rate
        cmd = f':SOURce:RADio:ARB:CLOCk:SRATe {str(sample_rate)}'
        self.write_value(cmd)

        # select the source file
        cmd = f':SOURce:RAD:ARB:WAV "ARBI:{ArbFileName}"'
        self.write_value(cmd)

        # turn on ARB
        cmd = f':SOURce:RADio:ARB:STATE ON'
        self.write_value(cmd)

    def __del__(self):
        self.set_close()
        print('SG has been disconnected')



if __name__ == '__main__':
    #mysg = SG('GPIB0::20::INSTR')
    Station = Station.Station()
    print(Station.get_instr_addr('SG'))
    mysg = SG(Station.get_instr_addr('SG'))
    print(mysg.name)
    #mysg.set_sg(freq = 3720, amp = -50)
    #mysg.set_sg_list(3680, 3720, 10, 0.5, -5)
    #timer = threading.Timer(10, mysg.tmp)
    #print(mysg.gen_wv())
    #mysg.test_wv_mtone(sample_rate=125e6, bandwith=4.5e6, step = 0.5e6, rf_freq= 3000, amp = -20)
    mysg.load_waveform(waveform='LTE20', rf_freq = 3700, amp = -40)
    #mysg.set_close()

