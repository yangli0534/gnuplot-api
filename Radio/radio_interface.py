# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-19-20

"""
import sys
sys.path.append(r'D:\code\visa_tutorials\Station')
sys.path.append(r'D:\code\visa_tutorials\Lib')

import Com
import PS
import time
import re
from threading import Thread
#from Lib import PS

class RU:
    def __init__(self, com_id, baud_rate, t):
        self._mycom = Com.Com(3, 115200, 0.5)
        connect_status = 0
        while connect_status == 0:
            time.sleep(1)
            answer = self._mycom.send_read_cmd('')
            # answer = mycom.receive_data()
            # answer = answer.rstrip()
            #print(answer)
            # print([ord(c) for c in answer])
            # print([ord(c) for c in 'root@ORU4419:~#'])
            terminator = 'root@ORU1226:~#'
            search_obj = re.search(terminator, answer, re.M | re.I)
            if search_obj:
                connect_status = 1
                print('RU connected successful')
            else:
                print('Connecting...')

    #def write(self):

    def get_sw_rev(self):
        cmd = 'fpga r 0x1808'
        tmp = self._mycom.send_read_cmd(cmd)
        sw_rev = re.findall(r"= (.+?)\n", tmp)[0].strip()[-4:]
        print(f'This sw release data is {sw_rev}')

    def get_clk_status(self):
        cmd = 'fpga r 0x2c06'
        tmp = self._mycom.send_read_cmd(cmd)
        status = (re.findall(r"= 0x(.+?)\n", tmp)[0].strip())=='c000000e'
        # status = True, locked
        # status = False, unlocked
        return status

    def get_jesd_status(self):
        cmd = 'fpga r 0x2e06'
        tmp = self._mycom.send_read_cmd(cmd)
        status = (re.findall(r"= 0x(.+?)\n", tmp)[0].strip())=='0'
        # status = True, link up
        # status = False, link down
        return status

    def get_fb_nco_freq(self, branch):
        # freq unit: MHz
        branch = self.__branch_def(branch)
        cmd = 'fpga w 0x1910 0x2'
        self._mycom.send_cmd(cmd)
        cmd = 'fpga w 0x1913 0x24'
        self._mycom.send_cmd(cmd)
        cmd = 'spi afe w 0x0013 0x02'
        self._mycom.send_cmd(cmd)
        if branch == 'A' or branch == 'B':

            byte0 = self._mycom.send_read_cmd('spi afe r 0x343c')
            byte0 = re.findall(r"3c] =(.+?)\n", byte0)[0].strip()[2:]

            byte1 = self._mycom.send_read_cmd('spi afe r 0x343d')
            byte1 = re.findall(r"3d] =(.+?)\n", byte1)[0].strip()[2:]

            byte2 = self._mycom.send_read_cmd('spi afe r 0x343e')
            byte2 = re.findall(r"3e] =(.+?)\n", byte2)[0].strip()[2:]

            byte3 = self._mycom.send_read_cmd('spi afe r 0x343f')
            byte3 = re.findall(r"3f] =(.+?)\n", byte3)[0].strip()[2:]
            #freq = byte3 + byte2 + byte1 + byte0
        else:
            byte0 = self._mycom.send_read_cmd('spi afe r 0x3444')
            byte0 = re.findall(r"44] =(.+?)\n", byte0)[0].strip()[2:]

            byte1 = self._mycom.send_read_cmd('spi afe r 0x3445')
            byte1 = re.findall(r"45] =(.+?)\n", byte1)[0].strip()[2:]

            byte2 = self._mycom.send_read_cmd('spi afe r 0x3446')
            byte2 = re.findall(r"46] =(.+?)\n", byte2)[0].strip()[2:]

            byte3 = self._mycom.send_read_cmd('spi afe r 0x3447')
            byte3 = re.findall(r"47] =(.+?)\n", byte3)[0].strip()[2:]

        freq = byte3 + byte2 + byte1 + byte0
        #print(freq)
        freq = int(freq, 16)/1000
        return freq

    def get_lo_freq(self):
        #freq unit: MHz
        self._mycom.send_cmd('spi afe w 0x0015 0x80')
        self._mycom.send_cmd('spi afe w 0x01d4 0x01')
        self._mycom.send_cmd('spi afe w 0x0374 0x00')
        self._mycom.send_cmd('spi afe w 0x0015 0x00')
        time.sleep(0.1)

        self._mycom.send_cmd(f'spi afe w 0x0014 0x08')
        temp=self._mycom.send_read_cmd('spi afe r 0x0028')
        pll_N = round(int(re.findall(r"28] =(.+?)\n", temp)[0].strip()[2:],16))

        temp = self._mycom.send_read_cmd('spi afe r 0x002e')
        pll_F = round(int(re.findall(r"2e] =(.+?)\n", temp)[0].strip()[2:], 16))<<16
        temp = self._mycom.send_read_cmd('spi afe r 0x002d')
        pll_F = (round(int(re.findall(r"2d] =(.+?)\n", temp)[0].strip()[2:], 16)) << 8) + pll_F
        temp = self._mycom.send_read_cmd('spi afe r 0x002c')
        pll_F = round(int(re.findall(r"2c] =(.+?)\n", temp)[0].strip()[2:], 16))+pll_F

        temp = self._mycom.send_read_cmd('spi afe r 0x0032')
        pll_D = (round(int(re.findall(r"32] =(.+?)\n", temp)[0].strip()[2:], 16)) & 15) << 16
        temp = self._mycom.send_read_cmd('spi afe r 0x0031')
        pll_D = (round(int(re.findall(r"31] =(.+?)\n", temp)[0].strip()[2:], 16)) << 8) + pll_D
        temp = self._mycom.send_read_cmd('spi afe r 0x0030')
        pll_D = round(int(re.findall(r"30] =(.+?)\n", temp)[0].strip()[2:], 16)) + pll_D

        temp = self._mycom.send_read_cmd('spi afe r 0x003f')
        pll_op_div = round(int(re.findall(r"3f] =(.+?)\n", temp)[0].strip()[2:], 16)) & 7

        self._mycom.send_cmd('spi afe w 0x0014 0x0')

        fact = (pll_N + pll_F/pll_D)/pll_op_div
        freq = fact*245.76/2

        self._mycom.send_cmd('spi afe w 0x0015 0x80')
        self._mycom.send_cmd('spi afe w 0x01d4 0x00')
        self._mycom.send_cmd('spi afe w 0x0374 0x00')
        self._mycom.send_cmd('spi afe w 0x0015 0x00')
        time.sleep(0.1)

        return freq

    def __branch_def(self, branch_id):
        branch_id = str(branch_id)
        branch_def = {'0':'A','1':'B','2':'C','3':'D','A':'A','B':'B','C':'C','D':'D','a':'A','b':'B','c':'C','d':'D'}
        return branch_def[branch_id]

    def read_temp_PA(self, branch):
        temp = self._mycom.send_read_cmd(f' spi paCtrl temp {self.__branch_def(branch)}')
        PA_temp = float(re.findall(r"Reading PA temperature :(.+?)\n", temp)[0].strip())
        return PA_temp

    def get_sw_status(self, branch, component):
        # branch: A|B|C|D
        # compoent: pa|tx|hpsw|lna
        branch = self.__branch_def(branch)
        status = self._mycom.send_read_cmd(f' fpga r 0x2403 ')
        status = int(re.findall(r"=(.+?)\n", status)[0].strip()[2:],16)
        pa_A = not (status & 1)
        pa_B = not (status & 1<<1)
        pa_C = not (status & 1<<2)
        pa_D = not (status & 1<<3)
        tx_AB = not (status & 1<<4)
        tx_CD = not (status & 1<<5)
        hpsw_AB = not (status & 1<<8)
        hpsw_CD = not (status & 1 << 9)
        lna_AB = not (status & 1 << 10)
        lna_CD = not (status & 1 << 11)
        status = {'A':{'pa': pa_A, 'tx': tx_AB, 'hpsw': hpsw_AB, 'lna': lna_AB}, \
                 'B': {'pa': pa_B, 'tx': tx_AB, 'hpsw': hpsw_AB, 'lna': lna_AB}, \
                 'C': {'pa': pa_C, 'tx': tx_CD, 'hpsw': hpsw_CD, 'lna': lna_CD}, \
                 'D': {'pa': pa_D, 'tx': tx_CD, 'hpsw': hpsw_CD, 'lna': lna_CD}}
        return status[branch][component]

    def get_bias(self, branch, stage, main_or_peak):
        # branch: A|B|C|D
        # state: driver|final
        # main_or_peak: main|peak
        branch = self.__branch_def(branch)
        cmd = {'A': {'final': {'main': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x30'}, \
                               'peak': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x32'}}, \
                      'driver': {'main': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x34'}, \
                                 'peak': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x36'}}}, \
                'B': {'final': {'main': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x31'}, \
                               'peak': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x33'}}, \
                      'driver': {'main': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x35'}, \
                                 'peak': {'cs0':'fpga w 0x1910 0x0','cs1':'fpga w 0x1911 0x04','read': 'spi paCtrl r 0x37'}}}, \
                'C': {'final': {'main': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x30'}, \
                               'peak': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x32'}}, \
                      'driver': {'main': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x34'}, \
                                 'peak': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x36'}}}, \
                'D': {'final': {'main': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x31'}, \
                               'peak': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x33'}}, \
                      'driver': {'main': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x35'}, \
                                 'peak': {'cs0':'fpga w 0x1910 0x1','cs1':'fpga w 0x1911 0x14','read': 'spi paCtrl r 0x37'}}}}

        cs0_cmd = cmd[branch][stage][main_or_peak]['cs0']
        self._mycom.send_cmd(cs0_cmd)
        cs1_cmd = cmd[branch][stage][main_or_peak]['cs1']
        self._mycom.send_cmd(cs1_cmd)
        read_cmd = cmd[branch][stage][main_or_peak]['read']
        bias = self._mycom.send_read_cmd(read_cmd)
        tmp = cmd[branch][stage][main_or_peak]['read'][-2:]
        search =f'{tmp}] =(.+?)\\n'
        bias = int(re.findall(search, bias)[0].strip()[2:], 16)
        return bias

    def init_check(self):
        print('init check:')

        # print sw release date
        myRU.get_sw_rev()

        # check clk status
        if myRU.get_clk_status():
            print('clk locked')
        else:
            print('clk unlocked')

        # check jesd status
        if False:
            if myRU.get_jesd_status():
                print('jesd link up')
            else:
                print('jesd linkdown')

        if False:
            for branch in ['A', 'B', 'C', 'D']:
                temp = myRU.read_temp_PA(branch)
                print(f'branch {branch} PA temperature is {round(temp)}°')

        if False:
            for branch in ['A', 'B', 'C', 'D']:
                for component in ['pa','lna']:
                    if myRU.get_sw_status(branch, component):
                        print(f'branch {branch} {component} is on')
                    else:
                        print(f'branch {branch} {component} is off')
        if False:
            for branch in ['A', 'B', 'C', 'D']:
                for stage in ['final', 'driver']:
                    for main_or_peak in ['main','peak']:
                        tmp = self.get_bias( branch, stage, main_or_peak)
                        print(f'Branch {branch} PA {stage} {main_or_peak} bias is {tmp}')

        # check fb nco freq
        if False:
            for branch in ['A', 'B', 'C', 'D']:
                freq = self.get_fb_nco_freq(branch)
                print(f'branch {branch} fb nco frequency = {freq} MHz')

        print(f'LO frequency is {self.get_lo_freq()}MHz')

    def __del__(self):
        print('RU has been disconnected')

if __name__ == '__main__':
    myRU = RU(com_id = 3 , baud_rate = 115200 , t = 1)
    myps = PS.PS('TCPIP0::172.16.1.57::inst0::INSTR')
    #active = True
    try:
        while True:
            myRU.init_check()
            print(f'total consumption is {round(myps.get_consumption())} W')
    except KeyboardInterrupt:
        pass
