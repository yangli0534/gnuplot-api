# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append(r'.\ui')
sys.path.append(r'.\Calibration')
sys.path.append(r'.\Lib')
sys.path.append(r'.\Radio')
sys.path.append(r'.\Common')

import os
import random
import numpy as np
import Calib


from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi(r"./ui/RuVue.ui", self)
        #self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])
        self.rbn_run.clicked.connect(self.run)
        self.rbn_plot.clicked.connect(self.update)

        self.RuCalib = Calib()
        freq = self.RuCalib.RU.DL_CENT_FREQ
        ul_freq_center = self.RuCalib.RU.UL_CENT_FREQ
        offs = -self.RuCalib.Station.get_tx_IL(freq)
        self.stimuli = -50
        self.rx_cable_IL = self.RuCalib.Station.get_rx_IL(ul_freq_center)
        chp1 = self.RuCalib.SA.set_chp(center=freq, sweep_time=0.05, sweep_count=10, rbw=100, int_bw=18,
                                  rlev=-10, offs=offs, scale=5)
        # RuCalib.SG.load_waveform(waveform='LTE20', rf_freq=ul_freq_center, amp=stimuli-rx_cable_IL)
        backoff = 6
        self.arp_target = float(self.RuCalib.RU.MAX_POWER_PER_ANT / 100) - backoff
        self.tor_target = -15 - backoff

    def update(self):
        r = random.random()*np.pi
        t = np.linspace(r, 2*np.pi+r, 100)
        y = np.sin(t)
        self.graphWidget.plot(t,y)

    def run(self):
        str = ''
        mode = ''
        if self.rbn_Tx.isChecked():
            mode = 'Tx'
            str = 'You have choose Tx'
            if self.rbn_A.isChecked():
                str = str + ' Branch A'
                branch = 'A'
            elif self.rbn_B.isChecked():
                str = str + ' Branch B'
                branch = 'B'
            elif self.rbn_C.isChecked():
                str = str + ' Branch C'
                branch = 'C'
            elif self.rbn_D.isChecked():
                str = str + ' Branch D'
                branch = 'D'
            else:
                branch = ''
                str = 'you should choose a branch'
        elif self.rbn_Rx.isChecked():
            mode = 'Rx'
            str = 'You have choose Rx'
            if self.rbn_A.isChecked():
                str = str + ' Branch A'
                branch = 'A'
            elif self.rbn_B.isChecked():
                str = str + ' Branch B'
                branch = 'B'
            elif self.rbn_C.isChecked():
                str = str + ' Branch C'
                branch = 'C'
            elif self.rbn_D.isChecked():
                str = str + ' Branch D'
                branch = 'D'
            else:
                branch = ''
                str = 'you should choose a branch'
        else:
            mode = ''
            branch = ''
            str = 'you should choose tx or rx firstly'
        self.label.setText(str)

        if (mode == 'Tx' and branch in ['A', 'B', 'C', 'D']):
            # # torpm = RuCalib.RU.get_tor_pm(branch)
            # # RuCalib.logger.debug(f'branch {branch} tor power  = {torpm} dBm')
            # adcpm = RuCalib.RU.get_ADC_pm(branch)
            # RuCalib.logger.debug(f'branch {branch} adc power  = {adcpm} dBFS')
            # # dpdpm = RuCalib.RU.get_DPD_pm(branch)
            # # RuCalib.logger.debug(f'branch {branch} dpd power  = {dpdpm} dBm')
            # ddcpm = RuCalib.RU.get_rx_pm(branch)
            # RuCalib.logger.debug(f'branch {branch} rx power  = {ddcpm} dBFS')

            # # pa bias calib
            self.RuCalib.logger.critical(f'##############START　PA BIAS CALIBRATION BRANCH {branch} ##################')
            bias = self.RuCalib.calib_pa_bias(branch)
            # bias = [hex(1704), hex(747), hex(1654), hex(1354)]
            #bias = ['0x684', '0x2e1', '0x5e9', '0x5c9']
            self.RuCalib.logger.critical(f'The calc DAC value in main of final of branch  {branch} is  {int(bias[0], 16)}')
            self.RuCalib.logger.critical(f'The calc DAC value in peak of final of branch  {branch} is  {int(bias[1], 16)}')
            self.RuCalib.logger.critical(f'The calc DAC value in main of driver of branch {branch} is {int(bias[2], 16)}')
            self.RuCalib.logger.critical(f'The calc DAC value in peak of driver of branch  {branch} is {int(bias[3], 16)}')
            self.RuCalib.logger.critical(f'##############　PA BIAS CALIBRATION BRANCH {branch} FINISHED ###############')

            self.RuCalib.logger.critical(f'##############START　CONFIG PA BIAS  BRANCH {branch} ####################')

            self.RuCalib.RU.set_pa_bias(branch, bias)
            self.RuCalib.RU.read_pa_bias(branch)
            self.RuCalib.RU.set_pa_branch(branch)
            self.RuCalib.RU.set_pa_on(branch)
            driver_bias_curr = self.RuCalib.RU.pa_driver_bias_read_curr(branch)
            self.RuCalib.logger.info(f'pa driver bias current = {driver_bias_curr} mA')
            final_bias_curr = self.RuCalib.RU.pa_final_bias_read_curr(branch)
            self.RuCalib.logger.info(f'pa final bias current = {final_bias_curr} mA')
            self.RuCalib.RU.set_off_all()
            self.RuCalib.logger.critical(f'###############FINISH　CONFIG PA BIAS  BRANCH {branch} ##################')

            self.RuCalib.tx_carrier_setup(branch, cbw=20, freq=self.RuCalib.RU.DL_CENT_FREQ)
            (tx_alg_dsa_gain_set, tx_dpd_post_vca_gain_set) = self.RuCalib.tx_power_adjustment(branch, target=40, error=0.2)

            # start tor dsa lin
            self.RuCalib.logger.critical('#################### START TOR DSA VLIN AND NORMALIZED##################')
            tor_dsa_norm_gain = self.RuCalib.tor_dsa_lin(branch, normalized_zero=-7)
            self.RuCalib.RU.set_tor_alg_dsa_gain(branch, tor_dsa_norm_gain)

            # start freq comp calib
            (tor_pm_list, arp_pm_list) = self.RuCalib.tx_sweep_read_tor_pm(branch, self.arp_target, self.tor_target)
            self.RuCalib.logger.critical(f'ARP Power is {arp_pm_list}')
            self.RuCalib.logger.critical(f'Tor power is {tor_pm_list}')
        elif (mode == 'Rx'and branch in ['A', 'B', 'C', 'D']):
            self.RuCalib.logger.info('##############START RX CALIB##################')
            self.RuCalib.rx_carrier_setup(branch=branch, freq=self.ul_freq_center)
            dsa_set = self.RuCalib.rx_dsa_vlin(branch, self.stimuli, self.RuCalib.RU.RX_GAIN_TARGET)
            (rx_vca_set, actual_gain) = self.RuCalib.rx_gain_calib(branch, dsa_set, self.stimuli)
            self.RuCalib.rx_freq_calib(self.stimuli, branch, dsa_set, rx_vca_set)

            self.RuCalib.logger.critical(f'Rx actual gain = {actual_gain}')
        else:
            sys.exit()





def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

