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

        # self._mycom.send_cmd('fpga w 0x1910 0x0')
        # self._mycom.send_cmd('fpga w 0x1911 0x04')
        # final_main = self._mycom.send_read_cmd('spi paCtrl r 0x30')
        # final_main_A = int(re.findall(r"30] =(.+?)\n", final_main)[0].strip()[2:],16)
        # final_peak = self._mycom.send_read_cmd('spi paCtrl r 0x32')
        # final_peak_A = int(re.findall(r"32] =(.+?)\n", final_peak)[0].strip()[2:],16)
        # driver_main = self._mycom.send_read_cmd('spi paCtrl r 0x34')
        # driver_main_A = int(re.findall(r"34] =(.+?)\n", driver_main)[0].strip()[2:],16)
        # driver_peak = self._mycom.send_read_cmd('spi paCtrl r 0x36')
        # driver_peak_A = int(re.findall(r"36] =(.+?)\n", driver_peak)[0].strip()[2:],16)
        #
        # final_main = self._mycom.send_read_cmd('spi paCtrl r 0x31')
        # final_main_B = int(re.findall(r"31] =(.+?)\n", final_main)[0].strip()[2:],16)
        # final_peak = self._mycom.send_read_cmd('spi paCtrl r 0x33')
        # final_peak_B = int(re.findall(r"33] =(.+?)\n", final_peak)[0].strip()[2:],16)
        # driver_main = self._mycom.send_read_cmd('spi paCtrl r 0x35')
        # driver_main_B = int(re.findall(r"35] =(.+?)\n", driver_main)[0].strip()[2:],16)
        # driver_peak = self._mycom.send_read_cmd('spi paCtrl r 0x37')
        # driver_peak_B = int(re.findall(r"37] =(.+?)\n", driver_peak)[0].strip()[2:],16)
        #
        #
        # self._mycom.send_cmd('fpga w 0x1910 0x1')
        # self._mycom.send_cmd('fpga w 0x1911 0x14')
        #
        # final_main = self._mycom.send_read_cmd('spi paCtrl r 0x30')
        # final_main_C = int(re.findall(r"30] =(.+?)\n", final_main)[0].strip()[2:], 16)
        # final_peak = self._mycom.send_read_cmd('spi paCtrl r 0x32')
        # final_peak_C = int(re.findall(r"32] =(.+?)\n", final_peak)[0].strip()[2:], 16)
        # driver_main = self._mycom.send_read_cmd('spi paCtrl r 0x34')
        # driver_main_C = int(re.findall(r"34] =(.+?)\n", driver_main)[0].strip()[2:], 16)
        # driver_peak = self._mycom.send_read_cmd('spi paCtrl r 0x36')
        # driver_peak_C = int(re.findall(r"36] =(.+?)\n", driver_peak)[0].strip()[2:], 16)
        #
        # final_main = self._mycom.send_read_cmd('spi paCtrl r 0x31')
        # final_main_D = int(re.findall(r"31] =(.+?)\n", final_main)[0].strip()[2:], 16)
        # final_peak = self._mycom.send_read_cmd('spi paCtrl r 0x33')
        # final_peak_D = int(re.findall(r"33] =(.+?)\n", final_peak)[0].strip()[2:], 16)
        # driver_main = self._mycom.send_read_cmd('spi paCtrl r 0x35')
        # driver_main_D = int(re.findall(r"35] =(.+?)\n", driver_main)[0].strip()[2:], 16)
        # driver_peak = self._mycom.send_read_cmd('spi paCtrl r 0x37')
        # driver_peak_D = int(re.findall(r"37] =(.+?)\n", driver_peak)[0].strip()[2:], 16)
        #
        # bias = {'A': {'final':{'main':final_main_A, 'peak':final_peak_A},'driver':{'main': driver_main_A, 'peak':driver_peak_A}}, \
        #         'B': {'final':{'main':final_main_B, 'peak':final_peak_B},'driver':{'main': driver_main_B, 'peak':driver_peak_B}}, \
        #         'C': {'final': {'main': final_main_C, 'peak': final_peak_C},'driver': {'main': driver_main_C, 'peak': driver_peak_C}}, \
        #         'D': {'final': {'main': final_main_D, 'peak': final_peak_D}, 'driver': {'main': driver_main_D, 'peak': driver_peak_D}} }
        #
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
        temp = myRU.read_temp_PA('A')
        print(f'branch A PA temperature is {round(temp)}°')
        temp = myRU.read_temp_PA('B')
        print(f'branch B PA temperature is {round(temp)}°')
        temp = myRU.read_temp_PA('C')
        print(f'branch C PA temperature is {round(temp)}°')
        temp = myRU.read_temp_PA('D')
        print(f'branch D PA temperature is {round(temp)}°')

        if myRU.get_sw_status('A', 'pa'):
            print(f'branch A PA is on')
        else:
            print(f'branch A PA is off')
        if myRU.get_sw_status('B', 'pa'):
            print(f'branch B PA is on')
        else:
            print(f'branch B PA is off')
        if myRU.get_sw_status('C', 'pa'):
            print(f'branch C PA is on')
        else:
            print(f'branch C PA is off')
        if myRU.get_sw_status('D', 'pa'):
            print(f'branch D PA is on')
        else:
            print(f'branch D PA is off')

        if myRU.get_sw_status('A', 'lna'):
            print(f'branch A lna is on')
        else:
            print(f'branch A lna is off')
        if myRU.get_sw_status('B', 'lna'):
            print(f'branch B lna is on')
        else:
            print(f'branch B lna is off')
        if myRU.get_sw_status('C', 'lna'):
            print(f'branch C lna is on')
        else:
            print(f'branch C lna is off')
        if myRU.get_sw_status('D', 'lna'):
            print(f'branch D lna is on')
        else:
            print(f'branch D lna is off')
        #
        # tmp = self.get_bias('A','final','main')
        # print(f'Branch A PA final main bias is {tmp} ')
        # tmp = self.get_bias('A','final','peak')
        # print(f'Branch A PA final peak bias is {tmp} ')
        # tmp = self.get_bias('A','driver','main')
        # print(f'Branch A PA driver main bias is {tmp} ')
        # tmp = self.get_bias('A','driver','peak')
        # print(f'Branch A PA driver peak bias is {tmp} ')
        # tmp = self.get_bias('B','final','main')
        # print(f'Branch B PA final main bias is {tmp} ')
        # tmp = self.get_bias('B','final','peak')
        # print(f'Branch B PA final peak bias is {tmp} ')
        # tmp = self.get_bias('B','driver','main')
        # print(f'Branch B PA driver main bias is {tmp} ')
        # tmp = self.get_bias('B','driver','peak')
        # print(f'Branch B PA driver peak bias is {tmp} ')
        # tmp = self.get_bias('C','final','main')
        # print(f'Branch C PA final main bias is {tmp} ')
        # tmp = self.get_bias('C','final','peak')
        # print(f'Branch C PA final peak bias is {tmp} ')
        # tmp = self.get_bias('C','driver','main')
        # print(f'Branch C PA driver main bias is {tmp} ')
        # tmp = self.get_bias('C','driver','peak')
        # print(f'Branch C PA driver peak bias is {tmp} ')
        # tmp = self.get_bias('D','final','main')
        # print(f'Branch D PA final main bias is {tmp} ')
        # tmp = self.get_bias('D','final','peak')
        # print(f'Branch D PA final peak bias is {tmp} ')
        # tmp = self.get_bias('D','driver','main')
        # print(f'Branch D PA driver main bias is {tmp} ')
        # tmp = self.get_bias('D','driver','peak')
        # print(f'Branch D PA driver peak bias is {tmp} ')

        for branch in ['A', 'B', 'C', 'D']:
            for stage in ['final', 'driver']:
                for main_or_peak in ['main','peak']:
                    tmp = self.get_bias( branch, stage, main_or_peak)
                    print(f'Branch {branch} PA {stage} {main_or_peak} bias is {tmp}')

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
