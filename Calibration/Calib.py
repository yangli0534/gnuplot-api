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

import PS
import SA
import PM
import RU
import matplotlib.pyplot as plt
import time
import math
from datetime import datetime
import log


# import submodule


# def tor_dsa_sweep(myRU)

# def set_tx_init_power(mySA, myRU,  backoff = 6):

class Calib(object):

    def __init__(self):
        dt = datetime.now()
        filename = dt.strftime("../../../Result/ORU1126 calibration and test log_%Y%m%d_%H%M%S.txt")
        # set up logging to file - see previous section for more details
        self.logger = log.setup_custom_logger('root', filename)

        self.PS = PS.PS('TCPIP0::172.16.1.252::inst0::INSTR')
        self.SA = SA.SA('TCPIP0::172.16.1.66::inst0::INSTR')
        self.RU = RU.RU(com_id=3, baud_rate=115200, t=1)

    def __del__(self):
        print('Calibration stopped')

    def tor_dsa_lin(self):
        self.logger.info('****************TOR DSA VLIN***********************************')
        tor_pm_list = []
        tor_dsa_list = []
        for tor_dsa_set in range(self.RU.TOR_ALG_DSA_MIN_GAIN, self.RU.TOR_ALG_DSA_MAX_GAIN + 1,
                                 self.RU.TOR_ALG_DSA_STEP):
            self.RU.set_tor_alg_dsa_gain('A', tor_dsa_set)
            tor_dsa_list.append(tor_dsa_set)
            self.logger.info(f' branch A dsa is set to {tor_dsa_set} dB')
            tor_pm = self.RU.get_tor_pm(branch='A', aver_cnt=10)
            self.logger.info(f' branch A tor pm is  {tor_pm} dBfs')
            # torpm = RU.get_tor_pm('A')
            # print(f' branch A tor pm is  {torpm} dBfs')
            tor_pm_list.append(tor_pm)
        plt.plot(tor_dsa_list, tor_pm_list)
        plt.xlabel('Tor alg DSA set: dB')
        plt.ylabel('Tor power meter: dBFs. average cnt = 10')
        plt.grid()
        # for x, y in zip(tor_dsa_list, tor_pm_list):
        # plt.text(x, y+0.001, '%.2f' % y, ha='center', va= 'bottom',fontsize=9)
        plt.title("Tor DSA vs Tor PM")
        dt = datetime.now()
        filename = dt.strftime("Tor DSA vs Tor PM_%Y%m%d_%H%M%S.png")
        plt.savefig(filename)

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
            time.sleep(1)
            #last_output = self.SA.get_chp()
            last_output = self.SA.get_chp(aver=3)
        self.logger.info(f'branch {branch} output has reached target={target}dBm, now it is {last_output} dBm')

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


if __name__ == '__main__':
    RuCalib = Calib()

    chp1 = RuCalib.SA.set_chp(center=RuCalib.RU.DL_CENT_FREQ, sweep_time=0.05, sweep_count=10, rbw=100, int_bw=18,
                              rlev=-10, offs=41.7, scale= 5)
    # RU = RU.RU(com_id=3, baud_rate=115200, t=1)
    # active = True
    try:

        record = ()
        for branch in ['B']:
            torpm = RuCalib.RU.get_tor_pm(branch)
            RuCalib.logger.debug(f'branch {branch} tor power  = {torpm} dBm')
            adcpm = RuCalib.RU.get_ADC_pm(branch)
            RuCalib.logger.debug(f'branch {branch} adc power  = {adcpm} dBm')
            dpdpm = RuCalib.RU.get_DPD_pm(branch)
            RuCalib.logger.debug(f'branch {branch} dpd power  = {dpdpm} dBm')

            # pa bias calib
            RuCalib.logger.critical(f'##############START　PA BIAS CALIBRATION BRANCH {branch} ##################')
            #bias = RuCalib.calib_pa_bias(branch)
            bias = [hex(1704), hex(747), hex(1654), hex(1354)]
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
            RuCalib.tx_power_adjustment(branch, target=41.2, error=0.2)
        while True:
            # myRU.init_check()
            RuCalib.logger.info(f'total consumption is {round(RuCalib.PS.get_consumption())} W')
            chp = RuCalib.SA.get_chp()
            RuCalib.logger.info(f' carrier power is {chp} dBm')
            temp = RuCalib.RU.read_temp_pa('A')
            RuCalib.logger.info(f'branch A PA temperature is {round(temp)}°')
            time.sleep(0.3)
            # if myRU.get_dpd_status():
            #     print('dpd is running')
            # else:
            #     print('dod has stopped')



    except KeyboardInterrupt:
        # logger_info.removeHandler(console)
        # del logger_info, console
        pass
