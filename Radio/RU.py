# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-10-20

"""
import sys
sys.path.append(r'D:\code\visa_tutorials\Station')
sys.path.append(r'D:\code\visa_tutorials\Lib')

import Com
import PS
import time
import re
import math
from threading import Thread
#from Lib import PS

class RU:
    def __init__(self, com_id, baud_rate, t):
        self._mycom = Com.Com(3, 115200, 0.5)

            # answer = mycom.receive_data()
            # answer = answer.rstrip()
            #print(answer)
            # print([ord(c) for c in answer])
            # print([ord(c) for c in 'root@ORU4419:~#'])
        answer = self._mycom.send_read_cmd('')
        terminator = 'root@ORU1226:~#'

        search_obj = re.search(terminator, answer, re.M | re.I)
        while (not search_obj):
            print('RU Connecting...')
            time.sleep(1)
            answer = self._mycom.send_read_cmd('')
            search_obj = re.search(terminator, answer, re.M | re.I)
        print('RU connected successful')
        self.TX_ALG_DSA_MAX_GAIN = 0
        self.TX_ALG_DSA_MIN_GAIN = 30
        self.TX_ALG_DSA_STEP = 1
        self.TX_DPD_POST_VCA_MAX_GAIN = 3.0
        self.TX_DPD_POST_VCA_MIN_GAIN = -3.0
        self.TX_DPD_POST_VCA_STEP = 0.01
        self.TOR_ALG_DSA_MAX_GAIN = 0
        self.TOR_ALG_DSA_MIN_GAIN = -16
        self.TOR_ALG_DSA_STEP = 1
        self.RX_ALG_DSA_MAX_GAIN = 0
        self.RX_ALG_DSA_MIN_GAIN = -28
        self.RX_ALG_DSA_STEP = 1
        self.RX_DDC_VCA_MAX_GAIN = 3
        self.RX_DDC_VCA_MIN_GAIN = -3
        self.RX_DDC_VCA_STEP = 0.01
        self.set_init(branch_set = ['A','B'])
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
        branch = self.__branch_def_alp(branch)
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
        time.sleep(0.2)

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
        #print(pll_D)
        temp = self._mycom.send_read_cmd('spi afe r 0x003f')
        pll_op_div = round(int(re.findall(r"3f] =(.+?)\n", temp)[0].strip()[2:], 16)) & 7

        #print(pll_op_div)
        self._mycom.send_cmd('spi afe w 0x0014 0x0')

        fact = (pll_N + pll_F/pll_D)/pll_op_div
        freq = fact*245.76/2

        self._mycom.send_cmd('spi afe w 0x0015 0x80')
        self._mycom.send_cmd('spi afe w 0x01d4 0x00')
        self._mycom.send_cmd('spi afe w 0x0374 0x00')
        self._mycom.send_cmd('spi afe w 0x0015 0x00')
        time.sleep(0.2)

        return freq

    def __branch_def_alp(self, branch_id):
        branch_id = str(branch_id)
        branch_def = {'0':'A','1':'B','2':'C','3':'D','A':'A','B':'B','C':'C','D':'D','a':'A','b':'B','c':'C','d':'D','all':'all','ALL':'all'}
        return branch_def[branch_id]

    def __branch_def_num(self, branch_id):
        branch_id = str(branch_id)
        branch_def = {'0':'0','1':'1','2':'2','3':'3','A':'0','B':'1','C':'2','D':'3','a':'0','b':'1','c':'2','d':'3','all':'all','ALL':'all'}
        return branch_def[branch_id]

    def __tor_branch_def(self, branch_id):
        branch_id = str(branch_id)
        branch_def = {'0': '0', '1': '0', '2': '1', '3': '1', 'A': '0', 'B': '0', 'C': '1', 'D': '1', 'a': '0',
                      'b': '0', 'c': '1', 'd': '1'}
        return branch_def[branch_id]

    def read_temp_PA(self, branch):
        temp = self._mycom.send_read_cmd(f' spi paCtrl temp {self.__branch_def_alp(branch)}')
        PA_temp = float(re.findall(r"Reading PA temperature :(.+?)\n", temp)[0].strip())
        return PA_temp

    def read_temp_AFE(self):
        temp = self._mycom.send_read_cmd(f'spi temperature')
        AFE_temp = float(re.findall(r"of AFE is: (.+?)\n", temp)[0].strip())
        return AFE_temp

    def read_temp_FPGA(self):
        temp = self._mycom.send_read_cmd(f'fpga temperature')
        FPGA_temp = float(re.findall(r"of FPGA is: (.+?)\n", temp)[0].strip())
        return FPGA_temp


    def get_sw_status(self, branch, component):
        # branch: A|B|C|D
        # compoent: pa|tx|hpsw|lna
        branch = self.__branch_def_alp(branch)
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
        branch = self.__branch_def_alp(branch)
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

    def get_tor_pm(self, branch, aver_cnt = 1):
        aver_cnt = round(int(aver_cnt))
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga torpwr {branch}'
        tmp= self._mycom.send_read_cmd(cmd)
        torpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
        torpm = 0
        # there is sw bug in read tor pm and 2rd read to workaround
        if aver_cnt == 1:
            tmp= self._mycom.send_read_cmd(cmd)
            torpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
            return torpm
        else:
            for i in range(aver_cnt):
                tmp = self._mycom.send_read_cmd(cmd)
                torpm = torpm + float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
            return float(torpm/aver_cnt)

    def get_DUC_pm(self, branch):
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga ducpwr {branch}'
        tmp= self._mycom.send_read_cmd(cmd)
        ducpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
        return ducpm

    def get_DPD_pm(self, branch):
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga dpdpwr {branch}'
        tmp= self._mycom.send_read_cmd(cmd)
        dpdpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
        return dpdpm

    def get_DDC_pm(self, branch):
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga ddcpwr {branch}'
        tmp= self._mycom.send_read_cmd(cmd)
        dpdpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
        return dpdpm

    def get_ADC_pm(self, branch):
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga adcpwr {branch}'
        tmp= self._mycom.send_read_cmd(cmd)
        adcpm= float(re.findall(r"dbfs is (.+?)\n", tmp)[0].strip())
        return adcpm

    def set_pa_bias(self, branch, bias=[]):
        branch = self.__branch_def_alp(branch)
        #cmd = f'ztest pabias {branch}'
        #tmp = self._mycom.send_read_cmd(cmd)
        #return re.search(r'config PA BIAS OK!', tmp, re.M|re.I) != None
        if branch == A:
            cmd_set = ['fpga w 0x1910 0x0', 'fpga w 0x1911 0x04', 'spi paCtrl w 0x2 0x2', 'spi paCtrl w 0x16 0x5',
                       'spi paCtrl w 0x4E 0xBB8', 'spi paCtrl w 0x4F 0xBB8', 'spi paCtrl w 0x30 0x689',
                       'spi paCtrl w 0x32 0x2e1', 'spi paCtrl w 0x34 0x731', 'spi paCtrl w 0x36 0x54a',
                       'spi paCtrl w 0x17 0x0']
        elif branch == B:
            cmd_set = ['fpga w 0x1910 0x0', 'fpga w 0x1911 0x04', 'spi paCtrl w 0x2 0x2', 'spi paCtrl w 0x16 0x5',
                       'spi paCtrl w 0x4E 0xBB8', 'spi paCtrl w 0x4F 0xBB8', 'spi paCtrl w 0x31 0x67a',
                       'spi paCtrl w 0x33 0x2e1', 'spi paCtrl w 0x35 0x731', 'spi paCtrl w 0x37 0x54a',
                       'spi paCtrl w 0x17 0x0']

        elif branch == C:
            cmd_set = ['fpga w 0x1910 0x1', 'fpga w 0x1911 0x14', 'spi paCtrl w 0x2 0x2', 'spi paCtrl w 0x16 0x5',
                       'spi paCtrl w 0x4E 0xBB8', 'spi paCtrl w 0x4F 0xBB8', 'spi paCtrl w 0x30 0x699',
                       'spi paCtrl w 0x32 0x2f1', 'spi paCtrl w 0x34 0x741', 'spi paCtrl w 0x36 0x731',
                       'spi paCtrl w 0x17 0x0']

        else:
            cmd_set = ['fpga w 0x1910 0x1', 'fpga w 0x1911 0x14', 'spi paCtrl w 0x2 0x2', 'spi paCtrl w 0x16 0x5',
                       'spi paCtrl w 0x4E 0xBB8', 'spi paCtrl w 0x4F 0xBB8', 'spi paCtrl w 0x31 0x684',
                       'spi paCtrl w 0x33 0x2e1',
                       'spi paCtrl w 0x35 0x5e9', 'spi paCtrl w 0x37 0x5c9', 'spi paCtrl w 0x17 0x0']

        for cmd in cmd_set:
            tmp = self._mycom.send_read_cmd(cmd)

def set_pa_on(self, branch):
        # turn on driver and final, HPSW switch to VSWR, turn off LNA
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga paCtrl turnOn {branch}'
        self._mycom.send_cmd(cmd)
    def set_txlow_on(self, branch):
        # turn on predriver, Tor
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga paCtrl dlLinkup {branch}'
        self._mycom.send_cmd(cmd)

    def set_tx_off(self,branch):
        # branch = A|B|C|D|all
        # turn of DUC->driver&final->Tor->predriver, turn on LNA, HPSW switch to Rx
        branch = self.__branch_def_alp(branch)
        if branch !='all':
            cmd = f'fpga paCtrl turnOff tx {branch}'
        else:
            cmd = f'fpga paCtrl turnOffAll tx'
        self._mycom.send_cmd(cmd)

    def set_off_all(self):
        cmd = f'fpga paCtrl turnOffAll tx'
        self._mycom.send_cmd(cmd)

    def set_rx_on(self, branch):
        # branch = A|B|C|D
        branch = self.__branch_def_alp(branch)
        cmd = f'fpga turnonrx {branch}'
        self._mycom.send_cmd(cmd)

    def get_tx_alg_dsa_gain(self, branch):
        branch = self.__branch_def_num(branch)
        cmd = f'spi DSA getTxA {branch}'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'Analog Attenuation for TX Channel {branch}:(.+?)\n'
        gain = 0 - float(re.findall(search, tmp)[0].strip())
        return gain

    def get_tx_dig_dsa_gain(self, branch):
        branch = self.__branch_def_num(branch)
        cmd = f'spi DSA getTxA {branch}'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'Dig Attenuation for TX Channel {branch}:(.+?)\n'
        gain = float(re.findall(search, tmp)[0].strip())
        return gain

    def set_tx_alg_dsa_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain: 0dB to -39dB

        branch = self.__branch_def_num(branch)
        if gain >0 or gain < -39:
            print(f'tx branch {branch} {str(gain)} is out of range')
            sys.exit(sys.exit('stop running'))
        gain = str(round(-gain))
        cmd = f'spi DSA setTxAnal {branch} {gain}'
        #print(cmd)
        self._mycom.send_cmd(cmd)

    def set_tx_dig_dsa_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain: 3dB to -20.875dB
        branch = self.__branch_def_num(branch)

        if gain >3 or gain < -20.875:
            print(f'tx branch {branch} {str(gain)} is out of range')
            sys.exit(sys.exit('stop running'))
        gain = str(round(-gain*100))
        cmd = f'spi DSA setTxDigt {branch} {gain}'
        print(cmd)
        self._mycom.send_cmd(cmd)

    def get_tor_alg_dsa_gain(self, branch):
        # branch: A|B|C|D
        # tordsa unit: dB
        branch = self.__tor_branch_def(branch)
        cmd = f'spi DSA getFbA {branch}'
        #print(cmd)
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'Current Attenuation for FB Channel {branch}:(.+?)\n'
        gain = -1* int(re.findall(search, tmp)[0].strip())
        return gain

    def set_tor_alg_dsa_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain: 0dB to -16dB
        branch = self.__tor_branch_def(branch)
        if gain >0 or gain < -16:
            print(f'tor branch {branch} {str(gain)} is out of range')
            sys.exit(sys.exit('stop running'))
        gain = str(round(-gain))
        cmd = f'spi DSA setFbA {branch} {gain}'
        #print(cmd)
        self._mycom.send_cmd(cmd)

    def get_dpd_post_vca_gain(self, branch):
        # branch: A|B|C|D
        # dpdPost_vca_gain unit: dB

        # branch = self.__branch_def_num(branch)
        # branch_alp = self.__branch_def_alp(branch)
        # cmd = f'ztest getDpdPostGain {branch}'
        # #print(cmd)
        # tmp = self._mycom.send_read_cmd(cmd)
        # #print(tmp)
        # search = f'{branch_alp}dpd post gain =(.+?)\n'
        # dpd_post_vca_gain = float(re.findall(search, tmp)[0].strip())

        # branch = self.__branch_def_num(branch)
        # if branch =='A' or branch == 'B':
        #     tmp = self._mycom.send_read_cmd('fpga r 0x1824')
        #     search = f'24] =(.+?)\n'
        #     if branch == 'A':
        #         tmp = re.findall(search, tmp)[0].strip()[6:10]
        #     else:
        #         tmp = re.findall(search, tmp)[0].strip()[2:6]
        # else:
        #     tmp = self._mycom.send_read_cmd('fpga r 0x1825')
        #     search = f'25] =(.+?)\n'
        #     if branch == 'C':
        #         tmp = re.findall(search, tmp)[0].strip()[6:10]
        #     else:
        #         tmp = re.findall(search, tmp)[0].strip()[2:6]
        tmp = self.get_dpd_post_vca_gain_reg(branch)
        dpd_post_vca_gain = 20*math.log10(int(tmp, 16)/16384)
        #print(dpd_post_vca_gain)
        return dpd_post_vca_gain

    def get_dpd_post_vca_gain_reg(self, branch):
        branch = self.__branch_def_alp(branch)
        if branch == 'A' or branch == 'B':
            tmp = self._mycom.send_read_cmd('fpga r 0x1824')
            search = f'24] =(.+?)\n'
            if branch == 'A':
                dpd_post_vca_gain_reg = re.findall(search, tmp)[0].strip()[6:10]
            else:
                dpd_post_vca_gain_reg = re.findall(search, tmp)[0].strip()[2:6]
        else:
            tmp = self._mycom.send_read_cmd('fpga r 0x1825')
            search = f'25] =(.+?)\n'
            if branch == 'C':
                dpd_post_vca_gain_reg = re.findall(search, tmp)[0].strip()[6:10]
            else:
                dpd_post_vca_gain_reg = re.findall(search, tmp)[0].strip()[2:6]
        #print(dpd_post_vca_gain_reg)
        return  dpd_post_vca_gain_reg

    def get_dpd_pre_vca_gain_reg(self, branch):
        branch = self.__branch_def_alp(branch)
        if branch =='A' or branch == 'B':
            tmp = self._mycom.send_read_cmd('fpga r 0x1820')
            search = f'20] =(.+?)\n'
            if branch == 'B':
                dpd_pre_vca_gain_reg = re.findall(search, tmp)[0].strip()[2:6]
            else:
                dpd_pre_vca_gain_reg = re.findall(search, tmp)[0].strip()[6:10]
        else:
            tmp = self._mycom.send_read_cmd('fpga r 0x1821')
            search = f'21] =(.+?)\n'
            if branch == 'D':
                dpd_pre_vca_gain_reg = re.findall(search, tmp)[0].strip()[2:6]
            else:
                dpd_pre_vca_gain_reg = re.findall(search, tmp)[0].strip()[6:10]
        #print(dpd_pre_vca_gain_reg)
        return dpd_pre_vca_gain_reg

    def get_dpd_pre_vca_gain(self, branch):
        # branch = self.__branch_def_num(branch)
        # if branch =='A' or branch == 'B':
        #     tmp = self._mycom.send_read_cmd('fpga r 0x1820')
        #     search = f'20] =(.+?)\n'
        #     if branch == 'A':
        #         gain = re.findall(search, tmp)[0].strip()[2:6]
        #     else:
        #         gain = re.findall(search, tmp)[0].strip()[6:10]
        # else:
        #     tmp = self._mycom.send_read_cmd('fpga r 0x1821')
        #     search = f'21] =(.+?)\n'
        #     if branch == 'C':
        #         gain = re.findall(search, tmp)[0].strip()[2:6]
        #     else:
        #         gain =  re.findall(search, tmp)[0].strip()[6:10]

        tmp = self.get_dpd_post_vca_gain_reg(branch)
        dpd_pre_vca_gain = 20 * math.log10(int(tmp, 16) / 16384)
        return dpd_pre_vca_gain

    def set_dpd_pre_vca_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain unit: dB -3dB to 3dB
        branch = self.__branch_def_alp(branch)
        tmp = round(math.sqrt(math.pow(10, float(gain) / 10.0)) * 16384)
        if branch == 'A' or branch == 'B':
            previous_A = int(self.get_dpd_pre_vca_gain_reg('A'), 16)
            previous_B = int(self.get_dpd_pre_vca_gain_reg('B'), 16)
            if branch == 'B':
                new = previous_A + (tmp << 16)
            else:
                new = (previous_B << 16) + tmp
            new = hex(new)
            cmd = f'fpga w 0x1820 {new}'
        else:
            previous_C = int(self.get_dpd_post_vca_gain_reg('C'), 16)
            previous_D = int(self.get_dpd_post_vca_gain_reg('D'), 16)
            if branch == 'D':
                new = previous_C + (tmp << 16)
            else:
                new = (previous_D << 16 ) + tmp
            new = hex(new)
            cmd = f'fpga w 0x1821 {new}'

        self._mycom.send_cmd(cmd)


    def set_dpd_post_vca_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain unit: dB -3dB to 3dB
        branch = self.__branch_def_alp(branch)
        tmp = round(math.sqrt(math.pow(10, float(gain) / 10.0)) * 16384)
        if branch == 'A' or branch == 'B':
            previous_A = int(self.get_dpd_post_vca_gain_reg('A'), 16)
            previous_B = int(self.get_dpd_post_vca_gain_reg('B'), 16)
            if branch == 'B':
                new = previous_A + (tmp << 16)
            else:
                new = (previous_B << 16 ) + tmp
            new = hex(new)
            cmd = f'fpga w 0x1824 {new}'
        else:
            previous_C = int(self.get_dpd_post_vca_gain_reg('C'), 16)
            previous_D = int(self.get_dpd_post_vca_gain_reg('D'), 16)
            if branch == 'D':
                new = previous_C + (tmp << 16)
            else:
                new = (previous_D << 16 ) + tmp
            new = hex(new)
            cmd = f'fpga w 0x1825 {new}'
        #print(cmd)
        self._mycom.send_cmd(cmd)

    def get_rx_alg_dsa_gain(self, branch):
        branch = self.__branch_def_num(branch)
        cmd = f'spi DSA getRxA {branch}'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'Current Attenuation for RX Channel {branch}:(.+?)\n'
        alg_dsa = -1* float(re.findall(search, tmp)[0].strip())
        return alg_dsa

    def set_rx_alg_dsa_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain: 0dB to -28dB

        branch = self.__branch_def_num(branch)
        if gain >0 or gain < -28:
            print(f'rx branch {branch} {str(gain)} is out of range')
            sys.exit(sys.exit('stop running'))
        gain = str(round(-gain))
        cmd = f'spi DSA setRxA {branch} {gain}'
        #print(cmd)
        self._mycom.send_cmd(cmd)

    def get_rx_vca_gain(self, branch):
        branch = self.__branch_def_num(branch)
        branch_alp = self.__branch_def_alp(branch)
        cmd = f'ztest getDdcGain {branch}'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'channel{branch_alp}ddc gain =(.+?)\n'
        dig_vca = float(re.findall(search, tmp)[0].strip())
        return dig_vca

    def set_rx_vca_gain(self, branch, gain):
        # branch: A|B|C|D
        # gain: -3dB to +3

        branch = self.__branch_def_num(branch)
        if gain >3 or gain < -3:
            print(f'rx branch {branch} vca gain {str(gain)} is out of range')
            sys.exit(sys.exit('stop running'))
        gain = str(round(gain*100))
        cmd = f'ztest setDdcGain {branch} {gain}'
        #print(cmd)
        self._mycom.send_cmd(cmd)

    def set_dpd_init(self):
        cmd = f'dpd init'
        tmp = self._mycom.send_read_cmd(cmd)
        return re.search('Xilinx Dpd Init OK!', tmp, re.M | re.I) != None

    def set_data_on(self, bandwidth = 100):
        #bandwidth:　100 for 100MHz data\filter\cfr, 20 for 20MHz data\filter\cfr
        bandwidth = str(bandwidth)
        # parameter check
        if  not (bandwidth == '100' or bandwidth == '20'):
            return False
        else:
            cmd = f'senddata s{bandwidth}'
            tmp = self._mycom.send_read_cmd(cmd)
            return re.search('I/Q data OK', tmp, re.M | re.I) != None

    def get_dpd_status(self):
        cmd = f'cat /proc/interrupts'
        tmp = self._mycom.send_read_cmd(cmd)
        #print(tmp)
        search = f'45:(.+?)          '
        previous = re.findall(search, tmp)[0].strip()
        #previous = re.findall(search, tmp)
        #print(previous)
        tmp = self._mycom.send_read_cmd(cmd)
        #print(tmp)
        current = re.findall(search, tmp)[0].strip()
        #current = re.findall(search, tmp)
        #print(current)
        if previous == current:
            return False
        else:
            return True

    def set_duc_off(self, branch):
        branch= self.__branch_def_alp(branch)
        cmd ={'A': 'fpga w 0x4010 0x000', 'B': 'fpga w 0x4011 0x000', 'C': 'fpga w 0x4012 0x000','D': 'fpga w 0x4013 0x000'}
        if branch != 'all':
            self._mycom.send_cmd(cmd[branch])
        else:
            self._mycom.send_cmd(cmd['A'])
            self._mycom.send_cmd(cmd['B'])
            self._mycom.send_cmd(cmd['C'])
            self._mycom.send_cmd(cmd['D'])

    def set_duc_on(self, branch):
        branch = self.__branch_def_alp(branch)
        cmd = {'A': 'fpga w 0x4010 0x4000', 'B': 'fpga w 0x4011 0x4000', 'C': 'fpga w 0x4012 0x4000',
               'D': 'fpga w 0x4013 0x4000'}
        if branch != 'all':
            self._mycom.send_cmd(cmd[branch])
        else:
            self._mycom.send_cmd(cmd['A'])
            self._mycom.send_cmd(cmd['B'])
            self._mycom.send_cmd(cmd['C'])
            self._mycom.send_cmd(cmd['D'])

    def get_pa_vdd_target(self):
        #vol unit: V
        cmd = 'spi readpavdd'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'pavdd voltage is:(.+?)\n'
        vol = float(re.findall(search, tmp)[0].strip())
        return vol

    def get_pa_vdd(self, stage='final'):
        # stage: final or driver
        #vol unit: V
        stage = str(stage)
        if stage == 'final':
            cmd = 'fpga get pavdd'
        else:
            cmd = 'fpga get dpavdd'
        tmp = self._mycom.send_read_cmd(cmd)
        search = f'=(.+?),'
        vol = float(re.findall(search, tmp)[0].strip())
        return vol

    def set_init(self, branch_set = ['A', 'B']):
        print('init check:')

        # print sw release date

        self.get_sw_rev()

        # check clk status
        if self.get_clk_status():
            print('clk locked')
        else:
            print('clk unlocked')

        # check jesd status
        if True:
            if self.get_jesd_status():
                print('jesd link up')
            else:
                print('jesd linkdown')

        print('turning off all')
        self.set_off_all()

        if True:
            for branch in branch_set:
                temp = self.read_temp_PA(branch)
                print(f'branch {branch} PA temperature is {round(temp)}°')

        if True:
            for branch in branch_set:
                for component in ['pa', 'tx','lna']:
                    if self.get_sw_status(branch, component):
                        print(f'branch {branch} {component} is on')
                    else:
                        print(f'branch {branch} {component} is off')
        if True:
            for branch in branch_set:
                for stage in ['final', 'driver']:
                    for main_or_peak in ['main','peak']:
                        tmp = self.get_bias( branch, stage, main_or_peak)
                        print(f'Branch {branch} PA {stage} {main_or_peak} bias is {tmp}')

        # check fb nco freq
        if True:
            for branch in branch_set:
                freq = self.get_fb_nco_freq(branch)
                print(f'branch {branch} fb nco frequency = {freq} MHz')

        print(f'LO frequency is {self.get_lo_freq()}MHz')

        # read torpm

        if True:
            for branch in branch_set:
                torpm = self.get_tor_pm(branch)
                print(f'branch {branch} tor power  = {torpm} dBm')
                adcpm = self.get_ADC_pm(branch)
                print(f'branch {branch} adc power  = {adcpm} dBm')
                dpdpm = self.get_DPD_pm(branch)
                print(f'branch {branch} dpd power  = {dpdpm} dBm')

                self.set_tx_alg_dsa_gain(branch, -20)
                tx_alg_dsa_gain = self.get_tx_alg_dsa_gain(branch)
                print(f'Branch {branch} Tx analog dsa  gain is {tx_alg_dsa_gain} dB')

                tx_dig_dsa_gain = self.get_tx_dig_dsa_gain(branch)
                print(f'Branch {branch} Tx digital dsa  gain is {tx_dig_dsa_gain} dB')

                self.set_dpd_post_vca_gain(branch, 3)
                tx_vca_dpd_post_gain = self.get_dpd_post_vca_gain(branch)
                print(f'Branch {branch} dpd post vca gain is {tx_vca_dpd_post_gain } dB')

                #tx_vca_dpd_pre_gain = self.get_dpd_pre_vca_gain_reg(branch)
                #print(f'Branch {branch} dpd pre vca gain is {tx_vca_dpd_pre_gain}')
                self.set_dpd_pre_vca_gain(branch, 3)
                tx_vca_dpd_pre_gain = self.get_dpd_pre_vca_gain(branch)
                print(f'Branch {branch} dpd pre vca gain is {tx_vca_dpd_pre_gain}')

                self.set_tor_alg_dsa_gain(branch, -10)
                tor_alg_dsa_gain = self.get_tor_alg_dsa_gain(branch)
                print(f'Branch {branch} tor dsa gain is {tor_alg_dsa_gain} dB')

                self.set_rx_alg_dsa_gain(branch, -10)
                rx_alg_dsa_gain = self.get_rx_alg_dsa_gain(branch)
                print(f'Branch {branch} rx dsa gain is {rx_alg_dsa_gain} dB')

                self.set_rx_vca_gain(branch, -2)
                rx_vca_gain = self.get_rx_vca_gain(branch)
                print(f'Branch {branch} rx vca gain is {rx_vca_gain} dB')

        # if(self.set_dpd_init()):
        #     print('dpd init successfully')
        # else:
        #     print('dpd init failed')

        pavdd = self.get_pa_vdd('final')
        print(f'final pa vdd = {pavdd}V')
        dpavdd = self.get_pa_vdd('driver')
        print(f'driver pa vdd = {dpavdd}V')
    def __del__(self):
        print('RU has been disconnected')

if __name__ == '__main__':
    myRU = RU(com_id = 3 , baud_rate = 115200 , t = 1)
    myps = PS.PS('TCPIP0::172.16.1.57::inst0::INSTR')
    #active = True
    try:
        while True:
            myRU.set_init()
            print(f'total consumption is {round(myps.get_consumption())} W')
    except KeyboardInterrupt:
        pass
