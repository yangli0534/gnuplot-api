# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-10-24

"""

import sys

sys.path.append(r'..\Station')
sys.path.append(r'..\Lib')
sys.path.append(r'..\Radio')
sys.path.append(r'..\Common')

#import PS
import SA
import PM
import RU
import SG
import matplotlib.pyplot as plt
import time
import math
from datetime import datetime
import log
import Station


# import submodule


# def tor_dsa_sweep(myRU)

# def set_tx_init_power(mySA, myRU,  backoff = 6):

class Calib(object):

    def __init__(self):
        dt = datetime.now()
        filename = dt.strftime("../../../Result/ORU1126 calibration and test log_%Y%m%d_%H%M%S.txt")
        # set up logging to file - see previous section for more details
        self.logger = log.setup_custom_logger('root', filename)
        self.Station = Station.Station()
        #self.PS = PS.PS(self.Station.get_instr_addr('PS'))
        self.SA = SA.SA(self.Station.get_instr_addr('SA'))
        self.SG = SG.SG(self.Station.get_instr_addr('SG'))
        self.RU = RU.RU(com_id=self.Station.get_instr_addr('RU'), baud_rate=115200, t=1)

    def __del__(self):
        print('Calibration stopped')

    def tor_dsa_lin(self, branch, normalized_zero = -7):
        self.logger.info('****************TOR DSA VLIN***********************************')
        tor_pm_list = []
        tor_dsa_list = []
        for tor_dsa_set in range(self.RU.TOR_ALG_DSA_MIN_GAIN, self.RU.TOR_ALG_DSA_MAX_GAIN + 1,
                                 self.RU.TOR_ALG_DSA_STEP):
            self.RU.set_tor_alg_dsa_gain(branch, tor_dsa_set)
            tor_dsa_list.append(tor_dsa_set)
            self.logger.info(f' branch A dsa is set to {tor_dsa_set} dB')
            tor_pm = self.RU.get_tor_pm(branch, aver_cnt=10)
            self.logger.info(f' branch {branch} tor pm is  {tor_pm} dBfs')
            # torpm = RU.get_tor_pm('A')
            # print(f' branch A tor pm is  {torpm} dBfs')
            tor_pm_list.append(tor_pm)
        tor_pm_norm = [ x -  max(tor_pm_list) for x in tor_pm_list]
        #tor_pm_norm[:] = [x - normalized_zero for x in tor_pm_norm]
        pos= round(min(range(len(tor_pm_norm)), key=lambda i: abs(tor_pm_norm[i] - (normalized_zero))))
        #tor_dsa_norm_gain = tor_dsa_list[pos]
        tor_dsa_norm_gain = normalized_zero
        self.logger.critical(f'Tor DSA gain {tor_dsa_norm_gain} will be normalized as zero and written to database ')
        arp_power = self.SA.get_chp()
        plt.plot(tor_dsa_list, tor_pm_list)
        plt.xlabel('Tor alg DSA set: dB')
        plt.ylabel('Tor power meter: dBFs. average cnt = 10')
        plt.grid()
        # for x, y in zip(tor_dsa_list, tor_pm_list):
        # plt.text(x, y+0.001, '%.2f' % y, ha='center', va= 'bottom',fontsize=9)
        plt.title(f"Tor DSA vs Tor PM Branch {branch}@ ARP power = {arp_power}dBm")
        dt = datetime.now()
        filename = dt.strftime(f"../../../Result/Tor DSA vs Tor PM Branch {branch}_%Y%m%d_%H%M%S.png")
        plt.savefig(filename)
        plt.close()
        return tor_dsa_norm_gain

    def rx_dsa_vlin(self, branch, stim_amp, target):
        self.logger.info('****************RX DSA VLIN***********************************')
        self.SG.set_freq(self.RU.UL_CENT_FREQ)
        rx_pm_list = []
        rx_dsa_list = []
        self.RU.set_rx_vca_gain(branch, self.RU.RX_DDC_VCA_GAIN_INIT[branch])
        for rx_dsa_set in range(self.RU.RX_ALG_DSA_MIN_GAIN, self.RU.RX_ALG_DSA_MAX_GAIN + 1,
                                 self.RU.RX_ALG_DSA_STEP):
            self.RU.set_rx_alg_dsa_gain(branch, rx_dsa_set)
            rx_dsa_list.append(rx_dsa_set)
            self.logger.info(f' Rx branch A dsa is set to {rx_dsa_set} dB')
            rx_pm = self.RU.get_rx_pm(branch=branch, aver_cnt=10)
            self.logger.info(f' branch A rx pm is  {rx_pm} dBfs')
            rx_pm_list.append(rx_pm)
        self.logger.critical(f'Rx DSA has been set to{rx_dsa_list}')
        self.logger.critical(f'Rx PM = {rx_pm_list}')
        #rx_pm_norm = [x - max(rx_pm_list) for x in rx_pm_list]
        # tor_pm_norm[:] = [x - normalized_zero for x in tor_pm_norm]
        #pos = round(min(range(len(rx_pm_norm)), key=lambda i: abs(rx_pm_norm[i] - (normalized_zero))))
        #rx_dsa_norm_gain = rx_dsa_list[pos]
        #self.logger.critical(f'Rx DSA gain {rx_dsa_norm_gain} will be normalized as zero and written to database ')
        plt.plot(rx_dsa_list, rx_pm_list)
        plt.xlabel('Rx alg DSA set: dB')
        plt.ylabel('Rx power meter: dBFs. average cnt = 10')
        plt.grid()
        # for x, y in zip(tor_dsa_list, tor_pm_list):
        # plt.text(x, y+0.001, '%.2f' % y, ha='center', va= 'bottom',fontsize=9)
        plt.title(f"Rx DSA vs Rx PM -Branch {branch}")
        dt = datetime.now()
        filename = dt.strftime(f"../../../Result/Rx DSA vs Rx PM Branch {branch}_%Y%m%d_%H%M%S.png")
        plt.savefig(filename)
        plt.close()

        gain_list = [rx_pm_list[i] - stim_amp for i in range(0, len(rx_pm_list))]
        pos = round(min(range(len(gain_list)), key=lambda i: abs(gain_list[i] - target)))
        dsa_set = rx_dsa_list[pos]
        self.logger.critical(f'Rx DSA will be set to {dsa_set}')
        return dsa_set
        #return tor_dsa_norm_gain

    def next_gain_adjustment(self, last_coarse, last_fine, last_output, coarse_high, coarse_low, fine_high, fine_low,
                             coarse_step, fine_step, target, error):
        last_coarse = float(last_coarse)
        last_fine = float(last_fine)
        last_output = float(last_output)
        coarse_high = float(coarse_high)
        coarse_low = float(coarse_low)
        fine_high = float(fine_high)
        fine_low = float(fine_low)
        coarse_step = float(coarse_step)
        fine_step = float(fine_step)
        target = float(target)
        self.logger.critical(f'last coarse dsa is set to {last_coarse}')
        self.logger.critical(f'last fine dsa is set to {last_fine}')
        if last_output + coarse_high - last_coarse + fine_high - last_fine < target:
            self.logger.critical('!!!out of range to get the target1 !!!')
            new_coarse = last_coarse
            new_fine = last_fine
        elif (abs(target - last_output) > coarse_step / 2) and (last_coarse + coarse_step < coarse_high) and (
                last_coarse - coarse_step > coarse_low):
            self.logger.critical('tx alg dsa will be changed')
            if target > last_output:
                new_coarse = last_coarse + coarse_step
                new_fine = last_fine
            else:
                new_coarse = last_coarse - coarse_step
                new_fine = last_fine
        elif (last_fine + target - last_output < fine_high) and (last_fine + target - last_output > fine_low):
            new_coarse = last_coarse
            new_fine = last_fine + target - last_output
            self.logger.critical('tx dig dsa will be changed')
        else:
            self.logger.critical('!!!tx dig dsa out of range to get the target2 !!!')
            new_coarse = last_coarse
            new_fine = last_fine
        self.logger.critical(f'coarse dsa is set to {new_coarse}')
        self.logger.critical(f'fine dsa is set to {new_fine}')
        return new_coarse, new_fine

    def tx_power_adjustment(self, branch, target=40, error=0.3):
        # target: dBm
        # error: dB
        time.sleep(1)
        #last_output = self.SA.get_chp()
        last_output = self.SA.get_chp(aver= 3)
        while abs(last_output - target) > error:
            self.logger.critical(f'target output power is {target} dBm, actual is {last_output} dBm')
            last_tx_alg_dsa_gain = self.RU.get_tx_alg_dsa_gain(branch)
            last_dpd_post_vca_gain = self.RU.get_dpd_post_vca_gain(branch)
            #last_tx_dig_dsa_gain = self.RU.get_tx_dig_dsa_gain(branch)
            self.logger.critical(f'last tx alg dsa is {last_tx_alg_dsa_gain}dB')
            self.logger.critical(f'last dpd post vca gain is {last_dpd_post_vca_gain}dB')
            #self.logger.critical(f'last tx dig gain is {last_tx_dig_dsa_gain}dB')
            (new_tx_alg_dsa_gain, new_dpd_post_vca_gain)=self.next_gain_adjustment(last_tx_alg_dsa_gain, last_dpd_post_vca_gain, last_output,
                                      float(self.RU.TX_ALG_DSA_MAX_GAIN), float(self.RU.TX_ALG_DSA_MIN_GAIN),
                                      float(self.RU.TX_DPD_POST_VCA_MAX_GAIN), float(self.RU.TX_DPD_POST_VCA_MIN_GAIN),
                                      float(self.RU.TX_ALG_DSA_STEP), float(self.RU.TX_DPD_POST_VCA_STEP), target, error)

            # (new_tx_alg_dsa_gain, new_tx_dig_dsa_gain) = self.next_gain_adjustment(last_tx_alg_dsa_gain,
            #                                                                          last_tx_dig_dsa_gain,
            #                                                                          last_output,
            #                                                                          float(self.RU.TX_ALG_DSA_MAX_GAIN),
            #                                                                          float(self.RU.TX_ALG_DSA_MIN_GAIN),
            #                                                                          float(
            #                                                                              self.RU.TX_DIG_DSA_MAX_GAIN),
            #                                                                          float(
            #                                                                              self.RU.TX_DIG_DSA_MIN_GAIN),
            #                                                                          float(self.RU.TX_ALG_DSA_STEP),
            #                                                                          float(
            #                                                                              self.RU.TX_DIG_DSA_STEP),
            #                                                                          target=40, error=error)

            if new_dpd_post_vca_gain != last_dpd_post_vca_gain:
                self.RU.set_dpd_post_vca_gain(branch, new_dpd_post_vca_gain)
            #     time.sleep(3)
            # if new_tx_dig_dsa_gain != last_tx_dig_dsa_gain:
            #     self.RU.set_tx_dig_dsa_gain(branch, new_tx_dig_dsa_gain)
            if new_tx_alg_dsa_gain != last_tx_alg_dsa_gain:
                self.RU.set_tx_alg_dsa_gain(branch, new_tx_alg_dsa_gain)
            #time.sleep(1)
            #last_output = self.SA.get_chp()
            last_output = self.SA.get_chp(aver=2)
        last_tx_alg_dsa_gain = self.RU.get_tx_alg_dsa_gain(branch)
        last_dpd_post_vca_gain = self.RU.get_dpd_post_vca_gain(branch)
        self.logger.info(f'branch {branch} output has reached target={target}dBm, now it is {last_output} dBm')

        self.RU.db_write_single(self.RU._DB.TX_ALG_DSA_INIT_KEY[branch], round(-last_tx_alg_dsa_gain*10))

        return last_tx_alg_dsa_gain, last_dpd_post_vca_gain

    def rx_gain_calib(self, branch, dsa_set, stim_amp):
        target = self.RU.RX_GAIN_TARGET
        error = 0.3
        self.RU.set_rx_alg_dsa_gain(branch, dsa_set)
        vca_gain_set = self.RU.get_rx_vca_gain(branch)
        while True:
            actual_gain = self.RU.get_rx_pm(branch, aver_cnt=5) - stim_amp
            self.logger.critical(f'actual gain is {actual_gain}')
            vca_gain_set = self.RU.get_rx_vca_gain(branch)
            if abs(target - actual_gain) < error:
                break
            elif (target - actual_gain + vca_gain_set) < self.RU.RX_DDC_VCA_MAX_GAIN:
                vca_gain_set = target - actual_gain + vca_gain_set
                self.RU.set_rx_vca_gain(branch, vca_gain_set)
            elif (target - actual_gain) > self.RU.RX_DDC_VCA_MAX_GAIN:
                self.logger.critical(f'Rx branch {branch} dynamic range is not enough reach target')
                break
            self.logger.critical(f'vca will be set to {vca_gain_set}')
        actual_gain = self.RU.get_rx_pm(branch, aver_cnt=5) - stim_amp
        return vca_gain_set, actual_gain
        #return False



    def pa_driver_bias_calib(self, branch):
        # revise from Jim version
        self.RU.reset_pa_driver()
        self.RU.set_pa_branch(branch)
        self.RU.pre_set_bias()
        self.RU.set_lowest_pa_bias()
        main_init_value = self.RU.DRIVER_MAIN_INIT_VALUE
        peak_init_value = self.RU.DRIVER_PEAK_INIT_VALUE
        self.RU.pa_driver_bias_calc_write_dac(branch, 1, main_init_value)
        self.RU.pa_driver_bias_calc_write_dac(branch, 2, peak_init_value)
        self.RU.pa_bias_calc_en_dac()
        self.RU.pa_bias_calc_pa_on(branch)
        (driver_main_bias_dac_calib, driver_peak_bias_dac_calib) = self.RU.pa_driver_bias_calc_tune(branch,
                                                                                                    main_init_value,
                                                                                                    self.RU.DRIVER_BIAS_TARGET)
        return driver_main_bias_dac_calib, driver_peak_bias_dac_calib

    def pa_final_bias_calc(self, branch):
        self.RU.reset_pa_driver()
        self.RU.set_pa_branch(branch)
        self.RU.pre_set_bias()
        self.RU.set_lowest_pa_bias()
        main_init_value = self.RU.FINAL_MAIN_INIT_VALUE
        self.RU.pa_final_bias_calc_write_dac(branch, 1, main_init_value)
        self.RU.pa_bias_calc_en_dac()
        self.RU.pa_bias_calc_pa_on(branch)
        target = self.RU.FINAL_BIAS_TARGET
        final_main_bias_dac_calib = self.RU.pa_final_bias_calc_tune(branch, 1, main_init_value, target)
        self.RU.pa_bias_calc_pa_off()
        self.RU.set_lowest_pa_bias()
        peak_init_value = self.RU.FINAL_PEAK_INIT_VALUE
        self.RU.pa_final_bias_calc_write_dac(branch, 2, peak_init_value)
        self.RU.pa_bias_calc_en_dac()
        self.RU.pa_bias_calc_pa_on(branch)
        final_peak_bias_dac_calib = self.RU.pa_final_bias_calc_tune(branch, 2, peak_init_value, target)
        # self.RU.pa_bias_calc_pa_off()
        self.RU.set_off_all()
        final_peak_bias_dac_calib = int(final_peak_bias_dac_calib, 16)
        final_peak_bias_dac_calib -= 900
        final_peak_bias_dac_calib = hex(final_peak_bias_dac_calib)
        return final_main_bias_dac_calib, final_peak_bias_dac_calib

    def calib_pa_bias(self, branch):
        [driver_main_bias_dac_calib, driver_peak_bias_dac_calib] = self.pa_driver_bias_calib(branch)
        [final_main_bias_dac_calib, final_peak_bias_dac_calib] = self.pa_final_bias_calc(branch)
        bias = [final_main_bias_dac_calib, final_peak_bias_dac_calib, driver_main_bias_dac_calib,
                driver_peak_bias_dac_calib]
        return bias

    def tx_carrier_setup(self, branch='A', cbw=20, freq=3700):
        # cbw:carrier bandwidth MHz
        # set carrier and pa on
        # if self.RU.set_data_on(bandwidth=100):
        if self.RU.set_data_on(bandwidth=cbw):
            if self.RU.set_carrier(type='tx', freq=freq, bandwidth=100):
                self.RU.set_pa_on(branch=branch)
                self.RU.set_txlow_on(branch=branch)
                self.logger.critical(f'branch {branch} carrier setup @ freq = {freq} MHz')
                return True
            else:
                return False
        else:
            return False

    def rx_carrier_setup(self, branch='A', freq=3700):
        # cbw:carrier bandwidth MHz
        # set carrier and pa on
        # if self.RU.set_data_on(bandwidth=100):
        freq = int(freq)
        self.RU.set_off_all()
        if self.RU.set_carrier(type='rx', freq=freq, bandwidth=100):
            self.RU.set_rx_on()
            return True
        else:
            self.logger.critical('rx carrier setup failed')
            return False
    def rx_freq_calib(self, stimuli, branch, dsa_set, vca_set):
        self.RU.set_rx_alg_dsa_gain(branch, dsa_set)
        self.RU.set_rx_vca_gain(branch, vca_set)
        freq_ref = self.RU.UL_CENT_FREQ
        gain_ref = self.RU.get_rx_pm(branch, aver_cnt=5) - stimuli
        self.logger.critical(f'Reference gain = {gain_ref}dB at frequency {freq_ref} MHz')
        IL_ref = self.Station.get_rx_IL(freq_ref)
        temp_previous = self.RU.read_temp_pa(branch)
        self.logger.info(f'reference temp = {temp_previous} degree before calibration')
        rx_pm_list = []
        freq_list = []
        gain_list = []
        self.logger.critical('#######START RX GAIN FREQ COMP##############')
        for freq in self.RU.UL_FREQ_COMP_LIST:
            self.SG.set_freq(freq)
            self.rx_carrier_setup(branch, freq)
            time.sleep(0.5)
            rx_pm = self.RU.get_rx_pm(branch, aver_cnt = 5)
            gain = rx_pm -(stimuli+self.Station.get_rx_IL(freq)-IL_ref)
            gain_norm = gain -gain_ref
            rx_pm_list.append(rx_pm)
            freq_list.append(freq)
            gain_list.append(gain_norm)
            self.logger.info(f'Rx PM = {rx_pm} dBFs, gain = {gain}dB on freq = {freq} MHz')
        temp_after = self.RU.read_temp_pa(branch)
        self.logger.info(f'reference temp = {temp_after} degree after calibration')
        plt.plot(freq_list, gain_list)
        plt.xlabel('Frequency: MHz')
        plt.ylabel('Gain Flatness ')
        # plt.grid()
        plt.title(f"Rx frequency compensation- branch {branch}")
        dt = datetime.now()
        filename = dt.strftime(f"../../../Result/Rx frequency compensation-Branch {branch} _%Y%m%d_%H%M%S.png")
        plt.savefig(filename)
        plt.close()
        self.logger.critical('############save database#########################')
        if abs (temp_after -temp_previous) < 2:
            # write ref temp
            #ref_temp_key = {'A':self.RU._DB.RX_40W_PWR_TEMPREF_A_KEY, 'B': self.RU._DB.RX_40W_PWR_TEMPREF_B_KEY, 'C'self.RU._DB.RX_40W_PWR_TEMPREF_C_KEY, 'D'self.RU._DB.RX_40W_PWR_TEMPREF_D_KEY}
            self.RU.db_write_single(self.RU._DB.RX_TEMP_REF_KEY[branch], round((temp_after+temp_previous)/2*10))
            # ref gain
            self.RU.db_write_single(self.RU._DB.RX_REF_GAIN_KEY[branch], round(gain_ref*10))
            # init dsa
            self.RU.db_write_single(self.RU._DB.RX_ALG_DSA_INIT_KEY[branch], round(abs(dsa_set)*10))
            # init ddc
            self.RU.db_write_single(self.RU._DB.RX_DDC_VCA_INIT_KEY[branch], round(vca_set*10))
            # freq com
            freq_tab = [ round(-gain*10) for gain in gain_list]
            self.logger.critical(f'freq tab = {freq_tab}')
            self.RU.db_write_table(self.RU._DB.RX_FREQ_TAB_KEY[branch], freq_tab)
            self.RU.db_save()
        self.logger.critical('#######Finish RX GAIN FREQ COMP##############')



    def tx_sweep_read_tor_pm(self, branch, arp_target, tor_target):
        self.RU.set_off_all()
        tor_pm_list = []
        arp_pm_list = []
        temp_previous = self.RU.read_temp_pa(branch)
        self.logger.critical(f'Branch {branch} PA temperature is {temp_previous}° before tor freq calib')
        for freq in self.RU.DL_FREQ_COMP_LIST:
            self.SA.set_center(freq)
            self.tx_carrier_setup(branch = branch, cbw=20, freq=freq)
            tor_pm = self.RU.get_tor_pm(branch=branch, aver_cnt=10)
            tor_pm_list.append(tor_pm)
            arp_pm = self.SA.get_chp(aver=2)
            arp_pm_list.append(arp_pm)
            self.RU.set_off_all()
            self.logger.critical(f' ARP power = {arp_pm} dBm while Tor PM = {tor_pm} dBFs')
        temp_current = self.RU.read_temp_pa(branch)
        self.logger.critical(f'Branch {branch} PA temperature is {temp_current}° after tor freq calib')
        #tor_freq_comp_list = [tor_pm - tor_target for tor_pm in tor_pm_list] -[arp_pm - arp_target for arp_pm in arp_pm_list]
        tor_freq_comp_list = [tor_target-tor_pm_list[i] -(arp_target-arp_pm_list[i]) for i in range(0, len(arp_pm_list))]
        self.logger.critical(f'tor frequency compensation table = {tor_freq_comp_list }')
        freq_list = self.RU.DL_FREQ_COMP_LIST
        freq_list = [freq_list[i] - self.RU.DL_CENT_FREQ for i in range(0, len(freq_list))]
        self.logger.critical(f'tor frequency list = {freq_list}')
        plt.plot(freq_list, tor_freq_comp_list)
        plt.xlabel('Frequency: MHz')
        plt.ylabel('Tor gain: dB ')
        #plt.grid()
        plt.title(f"Tor gain frequency compensation branch {branch}@ ARP power = {arp_target}dBm")
        dt = datetime.now()
        filename = dt.strftime(f"../../../Result/Tor gain frequency compensation Branch {branch}_%Y%m%d_%H%M%S.png")
        plt.savefig(filename)
        plt.close()

        # write tor init dsa
        self.RU.db_write_single(self.RU._DB.TOR_ALG_DSA_INIT_KEY[branch], 70)
        # write ref temp
        self.RU.db_write_single(self.RU._DB.TOR_TEMP_REF_KEY[branch], round(temp_current*10))
        # write freq tab
        freq_tab = [round(gain * 10) for gain in tor_freq_comp_list]
        self.RU.db_write_table(self.RU._DB.TOR_FREQ_TAB_KEY[branch], freq_tab)
        self.RU.db.save()
        return tor_pm_list, arp_pm_list

if __name__ == '__main__':
    RuCalib = Calib()
    freq = RuCalib.RU.DL_CENT_FREQ
    ul_freq_center = RuCalib.RU.UL_CENT_FREQ
    offs = -RuCalib.Station.get_tx_IL(freq)
    stimuli = -50
    rx_cable_IL = RuCalib.Station.get_rx_IL(ul_freq_center)
    chp1 = RuCalib.SA.set_chp(center= freq, sweep_time=0.05, sweep_count=10, rbw=100, int_bw=18,
                              rlev=-10, offs= offs, scale= 5)
    #RuCalib.SG.load_waveform(waveform='LTE20', rf_freq=ul_freq_center, amp=stimuli-rx_cable_IL)
    backoff = 6
    arp_target = float(RuCalib.RU.MAX_POWER_PER_ANT/100)-backoff
    tor_target = -15-backoff

    # RU = RU.RU(com_id=3, baud_rate=115200, t=1)
    # active = True
    try:
        case_choice = input('''Please select calibration case, you have to input exactly 'Rx' for RX case, 'Tx' for Tx case, otherwhile calibration will stop\n I choose ''')
        if (case_choice == 'Rx'):
            RuCalib.logger.info('Rx calibration will start\n')
        elif(case_choice == 'Tx'):
            RuCalib.logger.info('Tx calibration will start\n')
        else:
            RuCalib.logger.info('Calibration stop as no matched case\n')
            sys.exit()

        branch = input(
            '''Please select branch: A, B, C,D  otherwhile calibration will stop\n I choose branch ''')
        if (branch in ['A', 'B', 'C', 'D']):
            RuCalib.logger.info('You have choose \n')
        else:
            RuCalib.logger.info('Calibration stop as no matched branch\n')
            sys.exit()

        RuCalib.logger.info('START CALIBRATION')

        #for branch in ['D']:
        if(case_choice == 'Tx'):
            # # torpm = RuCalib.RU.get_tor_pm(branch)
            # # RuCalib.logger.debug(f'branch {branch} tor power  = {torpm} dBm')
            # adcpm = RuCalib.RU.get_ADC_pm(branch)
            # RuCalib.logger.debug(f'branch {branch} adc power  = {adcpm} dBFS')
            # # dpdpm = RuCalib.RU.get_DPD_pm(branch)
            # # RuCalib.logger.debug(f'branch {branch} dpd power  = {dpdpm} dBm')
            # ddcpm = RuCalib.RU.get_rx_pm(branch)
            # RuCalib.logger.debug(f'branch {branch} rx power  = {ddcpm} dBFS')

            # # pa bias calib
            RuCalib.logger.critical(f'##############START　PA BIAS CALIBRATION BRANCH {branch} ##################')
            #bias = RuCalib.calib_pa_bias(branch)
            #bias = [hex(1704), hex(747), hex(1654), hex(1354)]
            bias = ['0x684', '0x2e1', '0x5e9', '0x5c9']
            RuCalib.logger.critical(f'The calc DAC value in main of final of branch  {branch} is  {int(bias[0], 16)}')
            RuCalib.logger.critical(f'The calc DAC value in peak of final of branch  {branch} is  {int(bias[1], 16)}')
            RuCalib.logger.critical(f'The calc DAC value in main of driver of branch {branch} is {int(bias[2], 16)}')
            RuCalib.logger.critical(f'The calc DAC value in peak of driver of branch  {branch} is {int(bias[3], 16)}')
            RuCalib.logger.critical(f'##############　PA BIAS CALIBRATION BRANCH {branch} FINISHED ###############')

            RuCalib.logger.critical(f'##############START　CONFIG PA BIAS  BRANCH {branch} ####################')

            RuCalib.RU.set_pa_bias(branch, bias)
            RuCalib.RU.read_pa_bias(branch)
            RuCalib.RU.set_pa_branch(branch)
            RuCalib.RU.set_pa_on(branch)
            driver_bias_curr = RuCalib.RU.pa_driver_bias_read_curr(branch)
            RuCalib.logger.info(f'pa driver bias current = {driver_bias_curr} mA')
            final_bias_curr = RuCalib.RU.pa_final_bias_read_curr(branch)
            RuCalib.logger.info(f'pa final bias current = {final_bias_curr} mA')
            RuCalib.RU.set_off_all()
            RuCalib.logger.critical(f'###############FINISH　CONFIG PA BIAS  BRANCH {branch} ##################')

            RuCalib.tx_carrier_setup(branch, cbw=20, freq=RuCalib.RU.DL_CENT_FREQ)
            (tx_alg_dsa_gain_set, tx_dpd_post_vca_gain_set)=RuCalib.tx_power_adjustment(branch, target=40, error=0.2)

            # start tor dsa lin
            RuCalib.logger.critical('#################### START TOR DSA VLIN AND NORMALIZED##################')
            tor_dsa_norm_gain = RuCalib.tor_dsa_lin(branch,  normalized_zero=-7)
            RuCalib.RU.set_tor_alg_dsa_gain(branch, tor_dsa_norm_gain)

            # start freq comp calib
            (tor_pm_list, arp_pm_list) = RuCalib.tx_sweep_read_tor_pm(branch, arp_target, tor_target)
            RuCalib.logger.critical(f'ARP Power is {arp_pm_list}')
            RuCalib.logger.critical(f'Tor power is {tor_pm_list}')
        elif(case_choice == 'Rx'):
            RuCalib.logger.info('##############START RX CALIB##################')
            RuCalib.rx_carrier_setup(branch = branch, freq = ul_freq_center)
            dsa_set = RuCalib.rx_dsa_vlin(branch, stimuli, RuCalib.RU.RX_GAIN_TARGET)
            (rx_vca_set, actual_gain) = RuCalib.rx_gain_calib(branch, dsa_set, stimuli)
            RuCalib.rx_freq_calib(stimuli, branch, dsa_set, rx_vca_set)

            RuCalib.logger.critical(f'Rx actual gain = {actual_gain}')
        else:
            sys.exit()
        #while True:
            # myRU.init_check()
            #RuCalib.logger.info(f'total consumption is {round(RuCalib.PS.get_consumption())} W')
            #chp = RuCalib.SA.get_chp()
            #RuCalib.logger.info(f' carrier power is {chp} dBm')
            #temp = RuCalib.RU.read_temp_pa('A')
            #RuCalib.logger.info(f'branch A PA temperature is {round(temp)}°')
            #time.sleep(0.3)
            # if myRU.get_dpd_status():
            #     print('dpd is running')
            # else:
            #     print('dod has stopped')



    except KeyboardInterrupt:
        # logger_info.removeHandler(console)
        # del logger_info, console
        pass
