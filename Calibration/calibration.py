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
#import submodule


#def tor_dsa_sweep(myRU)

def tor_dsa_lin( myRU):

    print('****************TOR DSA VLIN***********************************')
    tor_pm_list = []
    tor_dsa_list = []
    for tor_dsa_set in range(myRU.TOR_ALG_DSA_MIN_GAIN, myRU.TOR_ALG_DSA_MAX_GAIN + 1, myRU.TOR_ALG_DSA_STEP):
        myRU.set_tor_alg_dsa_gain('A', tor_dsa_set)
        tor_dsa_list.append(tor_dsa_set)
        print(f' branch A dsa is set to {tor_dsa_set} dB')
        tor_pm = myRU.get_tor_pm(branch='A', aver_cnt=10)
        print(f' branch A tor pm is  {tor_pm} dBfs')
        # torpm = myRU.get_tor_pm('A')
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


def pa_driver_bias_calib(myRU, branch):
    # revise from Jimmy version
    myRU.reset_pa_driver()
    myRU.set_pa_branch(branch)
    myRU.pre_set_bias()
    myRU.set_lowest_pa_bias()
    main_init_value = myRU.DRIVER_MAIN_INIT_VALUE
    peak_init_value = myRU.DRIVER_PEAK_INIT_VALUE
    myRU.pa_driver_bias_calc_write_dac( branch, 1, main_init_value)
    myRU.pa_driver_bias_calc_write_dac(branch, 2, peak_init_value)
    myRU.pa_bias_calc_en_dac()
    myRU.pa_bias_calc_pa_on(branch)
    (y, x ) = myRU.pa_driver_bias_calc_tune(branch, main_init_value, myRU.DRIVER_BIAS_TARGET)
    return y, x

def pa_final_bias_calc(myRU, branch):
    myRU.reset_pa_driver()
    myRU.set_pa_branch(branch)
    myRU.pre_set_bias()
    myRU.set_lowest_pa_bias()
    main_init_value = myRU.FINAL_MAIN_INIT_VALUE
    myRU.pa_final_bias_calc_write_dac(branch, 1, main_init_value)
    myRU.pa_bias_calc_en_dac()
    myRU.pa_bias_calc_pa_on(branch)
    target = myRU.FINAL_BIAS_TARGET
    m = myRU.pa_final_bias_calc_tune(branch, 1, main_init_value, target)
    myRU.pa_bias_calc_pa_off()
    myRU.set_lowest_pa_bias()
    peak_init_value = myRU.FINAL_PEAK_INIT_VALUE
    myRU.pa_final_bias_calc_write_dac(branch, 2, peak_init_value)
    myRU.pa_bias_calc_en_dac()
    myRU.pa_bias_calc_pa_on(branch)
    z = myRU.pa_final_bias_calc_tune(branch, 2, peak_init_value, target)
    myRU.pa_bias_calc_pa_off()
    z = int(z, 16)
    z -= 900
    z = hex(z)
    return m, z




if __name__ == '__main__':

    dt = datetime.now()
    filename = dt.strftime("../../../Result/ORU1126 calibration and test log_%Y%m%d_%H%M%S.txt")
    # set up logging to file - see previous section for more details
    logger = log.setup_custom_logger('root', filename)
    logger.debug('main message')


    myps = PS.PS('TCPIP0::172.16.1.252::inst0::INSTR')
    mySA = SA.SA('TCPIP0::172.16.1.66::inst0::INSTR')

    chp1 = mySA.set_chp(center=3700, sweep_time=0.05, sweep_count=10, rbw=100, int_bw=98.3, rlev=20,
                         offs=41.7)
    myRU = RU.RU(com_id=3, baud_rate=115200, t=1)
    #active = True
    try:

        # myRU.set_pa_bias('A')
        # myRU.set_pa_bias('B')
        # myRU.set_pa_bias('C')
        # myRU.set_pa_bias('D')

        myRU.read_pa_bias( branch_set = ['A', 'B','C','D'])



        # #set carrier and pa on
        # #if myRU.set_data_on(bandwidth=100):
        # if myRU.set_data_on(bandwidth=20):
        #     if myRU.set_carrier(type = 'tx', freq = 3700, bandwidth = 100):
        #         myRU.set_pa_on(branch='A')
        #         myRU.set_txlow_on(branch='A')
        record = ()
        for branch in ['A']:
            torpm = myRU.get_tor_pm(branch)
            logger.debug(f'branch {branch} tor power  = {torpm} dBm')
            adcpm = myRU.get_ADC_pm(branch)
            logger.debug(f'branch {branch} adc power  = {adcpm} dBm')
            dpdpm = myRU.get_DPD_pm(branch)
            logger.debug(f'branch {branch} dpd power  = {dpdpm} dBm')

            # pa bias calib
            [y, x] = pa_driver_bias_calib(myRU, branch)
            [m, z] = pa_final_bias_calc(myRU, branch)
            logger.critical(f'The calc DAC value in main of driver of branch {branch} is {y}')
            logger.critical(f'The calc DAC value in peak of driver of branch  {branch} is {x}')
            logger.critical(f'The calc DAC value in main of final of branch  {branch} is  {m}')
            logger.critical(f'The calc DAC value in peak of final of branch  {branch} is  {z}')
            record = record + (y,)
            record = record + (x,)
            record = record + (m,)
            record = record + (z,)
        #tor_dsa_lin(myRU)

        # for j in range(int(len(record) / 4)):
        #     branch = chr(j + 65)
        #   logger.debug(f'The calc DAC value in main of driver of branch {branch} is { record[j * 4]}')
        #   logger.debug(f'The calc DAC value in peak of driver of branch { branch } is {record[j * 4 + 1]}')
        #   logger.debug(f'The calc DAC value in main of final of branch { branch } is {record[j * 4 + 2]}')
        #   logger.debug(f'The calc DAC value in peak of final of branch {branch } is {record[j * 4 + 3] }')

        while True:
            #myRU.init_check()
            logger.info(f'total consumption is {round(myps.get_consumption())} W')
            chp = mySA.get_chp()
            logger.info(f' carrier power is {chp} dBm')
            temp = myRU.read_temp_pa('A')
            logger.info(f'branch A PA temperature is {round(temp)}°')
            time.sleep(0.3)
            # if myRU.get_dpd_status():
            #     print('dpd is running')
            # else:
            #     print('dod has stopped')



    except KeyboardInterrupt:
        #logger_info.removeHandler(console)
        #del logger_info, console
        pass