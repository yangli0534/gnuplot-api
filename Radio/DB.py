"""
@author: Leon
@time: 2020-10-29

"""
import sys

sys.path.append(r'..\Station')
sys.path.append(r'..\Lib')

import Com
import PS
import time
import re
import math
from threading import Thread
# from Lib import PS
import logging
import numpy as np


class DB(object):

    def __init__(self):
        self.TX_40W_ANALOG_DSA_INIT_A_KEY = "/rhb/tx_db/tx:0/40W/drudsa/initValue"
        self.TX_40W_ANALOG_DSA_INIT_B_KEY = "/rhb/tx_db/tx:1/40W/drudsa/initValue"
        self.TX_40W_ANALOG_DSA_INIT_C_KEY = "/rhb/tx_db/tx:2/40W/drudsa/initValue"
        self.TX_40W_ANALOG_DSA_INIT_D_KEY = "/rhb/tx_db/tx:3/40W/drudsa/initValue"
        self.TX_ALG_DSA_INIT_KEY = {'A': self.TX_40W_ANALOG_DSA_INIT_A_KEY, 'B': self.TX_40W_ANALOG_DSA_INIT_B_KEY,
                                    'C': self.TX_40W_ANALOG_DSA_INIT_C_KEY, 'D': self.TX_40W_ANALOG_DSA_INIT_D_KEY}

        self.TX_40W_DIGITAL_DSA_INIT_A_KEY = "/rhb/tx_db/tx:0/40W/drudig/initValue"
        self.TX_40W_DIGITAL_DSA_INIT_B_KEY = "/rhb/tx_db/tx:1/40W/drudig/initValue"
        self.TX_40W_DIGITAL_DSA_INIT_C_KEY = "/rhb/tx_db/tx:2/40W/drudig/initValue"
        self.TX_40W_DIGITAL_DSA_INIT_D_KEY = "/rhb/tx_db/tx:3/40W/drudig/initValue"
        self.TX_DIG_DSA_INIT_KEY = {'A': self.TX_40W_DIGITAL_DSA_INIT_A_KEY, 'B': self.TX_40W_DIGITAL_DSA_INIT_B_KEY,
                                    'C': self.TX_40W_DIGITAL_DSA_INIT_C_KEY, 'D':self.TX_40W_DIGITAL_DSA_INIT_D_KEY}

        self.TOR_40W_ANALOG_DSA_INIT_AB_KEY = "/rhb/fb_db/fb:0/40W/drudsa/initValue"
        self.TOR_40W_ANALOG_DSA_INIT_CD_KEY = "/rhb/fb_db/fb:1/40W/drudsa/initValue"
        # self.TOR_40W_ANALOG_DSA_INIT_C_KEY="/rhb/fb_db/fb:1/40W/drudsa/initValue"
        # self.TOR_40W_ANALOG_DSA_INIT_D_KEY="/rhb/fb_db/fb:3/40W/drudsa/initValue"
        self.TOR_ALG_DSA_INIT_KEY = {'A': self.TOR_40W_ANALOG_DSA_INIT_AB_KEY, 'B': self.TOR_40W_ANALOG_DSA_INIT_AB_KEY,
                                     'C': self.TOR_40W_ANALOG_DSA_INIT_CD_KEY, 'D': self.TOR_40W_ANALOG_DSA_INIT_CD_KEY}

        self.TOR_40W_DIGITAL_DSA_INIT_AB_KEY = "/rhb/fb_db/fb:0/40W/drudig/initValue"
        self.TOR_40W_DIGITAL_DSA_INIT_CD_KEY = "/rhb/fb_db/fb:1/40W/drudig/initValue"
        self.TOR_DIG_DSA_INIT_KEY = {'A': self.TOR_40W_DIGITAL_DSA_INIT_AB_KEY,
                                     'B': self.TOR_40W_DIGITAL_DSA_INIT_AB_KEY,
                                     'C': self.TOR_40W_DIGITAL_DSA_INIT_CD_KEY,
                                     'D': self.TOR_40W_DIGITAL_DSA_INIT_CD_KEY}

        self.RX_40W_ANALOG_DSA_INIT_A_KEY = "/rhb/rx_db/rx:0/drudsa/initValue"
        self.RX_40W_ANALOG_DSA_INIT_B_KEY = "/rhb/rx_db/rx:1/drudsa/initValue"
        self.RX_40W_ANALOG_DSA_INIT_C_KEY = "/rhb/rx_db/rx:2/drudsa/initValue"
        self.RX_40W_ANALOG_DSA_INIT_D_KEY = "/rhb/rx_db/rx:3/drudsa/initValue"
        self.RX_ALG_DSA_INIT_KEY = {'A': self.RX_40W_ANALOG_DSA_INIT_A_KEY, 'B': self.RX_40W_ANALOG_DSA_INIT_B_KEY,
                                    'C': self.RX_40W_ANALOG_DSA_INIT_C_KEY, 'D': self.RX_40W_ANALOG_DSA_INIT_D_KEY}

        self.RX_40W_DIGITAL_DSA_INIT_A_KEY = "/rhb/rx_db/rx:0/drudig/initValue"
        self.RX_40W_DIGITAL_DSA_INIT_B_KEY = "/rhb/rx_db/rx:1/drudig/initValue"
        self.RX_40W_DIGITAL_DSA_INIT_C_KEY = "/rhb/rx_db/rx:2/drudig/initValue"
        self.RX_40W_DIGITAL_DSA_INIT_D_KEY = "/rhb/rx_db/rx:3/drudig/initValue"
        self.RX_DDC_VCA_INIT_KEY = {'A': self.RX_40W_DIGITAL_DSA_INIT_A_KEY, 'B': self.RX_40W_DIGITAL_DSA_INIT_B_KEY,
                                    'C': self.RX_40W_DIGITAL_DSA_INIT_C_KEY, 'D': self.RX_40W_DIGITAL_DSA_INIT_D_KEY}

        self.DRIVER_40W_PABIAS_INIT_MAIN_A_KEY = "/rhb/sau_db/40W/IDpa0.0/initValue"
        self.DRIVER_40W_PABIAS_INIT_MAIN_B_KEY = "/rhb/sau_db/40W/IDpa1.0/initValue"
        self.DRIVER_40W_PABIAS_INIT_MAIN_C_KEY = "/rhb/sau_db/40W/IDpa2.0/initValue"
        self.DRIVER_40W_PABIAS_INIT_MAIN_D_KEY = "/rhb/sau_db/40W/IDpa3.0/initValue"
        self.DRIVER_BIAS_MAIN_INIT_KEY = {'A': self.DRIVER_40W_PABIAS_INIT_MAIN_A_KEY,
                                          'B': self.DRIVER_40W_PABIAS_INIT_MAIN_B_KEY,
                                          'C': self.DRIVER_40W_PABIAS_INIT_MAIN_C_KEY,
                                          'D': self.DRIVER_40W_PABIAS_INIT_MAIN_D_KEY}

        self.DRIVER_40W_PABIAS_INIT_PEAK_A_KEY = "/rhb/sau_db/40W/IDpa0.1/initValue"
        self.DRIVER_40W_PABIAS_INIT_PEAK_B_KEY = "/rhb/sau_db/40W/IDpa1.1/initValue"
        self.DRIVER_40W_PABIAS_INIT_PEAK_C_KEY = "/rhb/sau_db/40W/IDpa2.1/initValue"
        self.DRIVER_40W_PABIAS_INIT_PEAK_D_KEY = "/rhb/sau_db/40W/IDpa3.1/initValue"
        self.DRIVER_BIAS_PEAK_INIT_KEY = {'A': self.DRIVER_40W_PABIAS_INIT_PEAK_A_KEY,
                                          'B': self.DRIVER_40W_PABIAS_INIT_PEAK_B_KEY,
                                          'C': self.DRIVER_40W_PABIAS_INIT_PEAK_C_KEY,
                                          'D': self.DRIVER_40W_PABIAS_INIT_PEAK_D_KEY}

        self.DRIVER_40W_PABIAS_MAIN_OFFSET_A_KEY = "/rhb/sau_db/40W/IDpa0.0/offset"
        self.DRIVER_40W_PABIAS_MAIN_OFFSET_B_KEY = "/rhb/sau_db/40W/IDpa1.0/offset"
        self.DRIVER_40W_PABIAS_MAIN_OFFSET_C_KEY = "/rhb/sau_db/40W/IDpa2.0/offset"
        self.DRIVER_40W_PABIAS_MAIN_OFFSET_D_KEY = "/rhb/sau_db/40W/IDpa3.0/offset"
        self.DRIVER_BIAS_MAIN_OFFSET_KEY = {'A': self.DRIVER_40W_PABIAS_MAIN_OFFSET_A_KEY,
                                            'B': self.DRIVER_40W_PABIAS_MAIN_OFFSET_B_KEY,
                                            'C': self.DRIVER_40W_PABIAS_MAIN_OFFSET_C_KEY,
                                            'D': self.DRIVER_40W_PABIAS_MAIN_OFFSET_D_KEY}

        self.DRIVER_40W_PABIAS_PEAK_OFFSET_A_KEY = "/rhb/sau_db/40W/IDpa0.1/offset"
        self.DRIVER_40W_PABIAS_PEAK_OFFSET_B_KEY = "/rhb/sau_db/40W/IDpa1.1/offset"
        self.DRIVER_40W_PABIAS_PEAK_OFFSET_C_KEY = "/rhb/sau_db/40W/IDpa2.1/offset"
        self.DRIVER_40W_PABIAS_PEAK_OFFSET_D_KEY = "/rhb/sau_db/40W/IDpa3.1/offset"
        self.DRIVER_BIAS_PEAK_OFFSET_KEY = {'A': self.DRIVER_40W_PABIAS_PEAK_OFFSET_A_KEY,
                                            'B': self.DRIVER_40W_PABIAS_PEAK_OFFSET_B_KEY,
                                            'C': self.DRIVER_40W_PABIAS_PEAK_OFFSET_C_KEY,
                                            'D': self.DRIVER_40W_PABIAS_PEAK_OFFSET_D_KEY}

        self.DRIVER_40W_PABIAS_BACKOFFDAC_A_KEY = "/rhb/sau_db/40W/IDpa0.1/backoffDAC"
        self.DRIVER_40W_PABIAS_BACKOFFDAC_B_KEY = "/rhb/sau_db/40W/IDpa1.1/backoffDAC"
        self.DRIVER_40W_PABIAS_BACKOFFDAC_C_KEY = "/rhb/sau_db/40W/IDpa2.1/backoffDAC"
        self.DRIVER_40W_PABIAS_BACKOFFDAC_D_KEY = "/rhb/sau_db/40W/IDpa3.1/backoffDAC"

        self.DRIVER_40W_DPAVDD_INIT_A_KEY = "/rhb/sau_db/40W/dpaVdd:0/initValue"
        self.DRIVER_40W_DPAVDD_INIT_B_KEY = "/rhb/sau_db/40W/dpaVdd:1/initValue"
        self.DRIVER_40W_DPAVDD_INIT_C_KEY = "/rhb/sau_db/40W/dpaVdd:2/initValue"
        self.DRIVER_40W_DPAVDD_INIT_D_KEY = "/rhb/sau_db/40W/dpaVdd:3/initValue"

        self.DRIVER_40W_PABIAS_MAIN_TEMP_A_KEY = "/rhb/sau_db/IDpa0.0/tempTab"
        self.DRIVER_40W_PABIAS_MAIN_TEMP_B_KEY = "/rhb/sau_db/IDpa1.0/tempTab"
        self.DRIVER_40W_PABIAS_MAIN_TEMP_C_KEY = "/rhb/sau_db/IDpa2.0/tempTab"
        self.DRIVER_40W_PABIAS_MAIN_TEMP_D_KEY = "/rhb/sau_db/IDpa3.0/tempTab"
        self.DRIVER_BIAS_MAIN_TEMP_TAB_KEY = {'A': self.DRIVER_40W_PABIAS_MAIN_TEMP_A_KEY,
                                              'B': self.DRIVER_40W_PABIAS_MAIN_TEMP_B_KEY,
                                              'C': self.DRIVER_40W_PABIAS_MAIN_TEMP_C_KEY,
                                              'D': self.DRIVER_40W_PABIAS_MAIN_TEMP_D_KEY}

        self.DRIVER_40W_PABIAS_PEAK_TEMP_A_KEY = "/rhb/sau_db/IDpa0.1/tempTab"
        self.DRIVER_40W_PABIAS_PEAK_TEMP_B_KEY = "/rhb/sau_db/IDpa1.1/tempTab"
        self.DRIVER_40W_PABIAS_PEAK_TEMP_C_KEY = "/rhb/sau_db/IDpa2.1/tempTab"
        self.DRIVER_40W_PABIAS_PEAK_TEMP_D_KEY = "/rhb/sau_db/IDpa3.1/tempTab"
        self.DRIVER_BIAS_PEAK_TEMP_TAB_KEY = {'A': self.DRIVER_40W_PABIAS_PEAK_TEMP_A_KEY,
                                              'B': self.DRIVER_40W_PABIAS_PEAK_TEMP_B_KEY,
                                              'C': self.DRIVER_40W_PABIAS_PEAK_TEMP_C_KEY,
                                              'D': self.DRIVER_40W_PABIAS_PEAK_TEMP_D_KEY}

        self.DRIVER_40W_DPAVDD_OFFSET_A_KEY = "/rhb/sau_db/40W/dpaVdd:0/offset"
        self.DRIVER_40W_DPAVDD_OFFSET_B_KEY = "/rhb/sau_db/40W/dpaVdd:1/offset"
        self.DRIVER_40W_DPAVDD_OFFSET_C_KEY = "/rhb/sau_db/40W/dpaVdd:2/offset"
        self.DRIVER_40W_DPAVDD_OFFSET_D_KEY = "/rhb/sau_db/40W/dpaVdd:3/offset"

        self.DRIVER_40W_DPAVDD_TEMP_A_KEY = "/rhb/sau_db/dpaVdd:0/tempTab"
        self.DRIVER_40W_DPAVDD_TEMP_B_KEY = "/rhb/sau_db/dpaVdd:1/tempTab"
        self.DRIVER_40W_DPAVDD_TEMP_C_KEY = "/rhb/sau_db/dpaVdd:2/tempTab"
        self.DRIVER_40W_DPAVDD_TEMP_D_KEY = "/rhb/sau_db/dpaVdd:3/tempTab"

        self.FINALLY_DRIVER_40W_PAVDD_INIT_A_KEY = "/rhb/pau_db/40W/mpaVdd:0/initValue"
        self.FINALLY_DRIVER_40W_PAVDD_INIT_B_KEY = "/rhb/pau_db/40W/mpaVdd:1/initValue"
        self.FINALLY_DRIVER_40W_PAVDD_INIT_C_KEY = "/rhb/pau_db/40W/mpaVdd:2/initValue"
        self.FINALLY_DRIVER_40W_PAVDD_INIT_D_KEY = "/rhb/pau_db/40W/mpaVdd:3/initValue"

        self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_A_KEY = "/rhb/pau_db/40W/IMpa0.0/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_B_KEY = "/rhb/pau_db/40W/IMpa1.0/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_C_KEY = "/rhb/pau_db/40W/IMpa2.0/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_D_KEY = "/rhb/pau_db/40W/IMpa3.0/initValue"
        self.FINAL_BIAS_MAIN_INIT_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_A_KEY,
                                         'B': self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_B_KEY,
                                         'C': self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_C_KEY,
                                         'D': self.FINALLY_DRIVER_40W_PABIAS_INIT_MAIN_D_KEY}

        self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_A_KEY = "/rhb/pau_db/40W/IMpa0.1/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_B_KEY = "/rhb/pau_db/40W/IMpa1.1/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_C_KEY = "/rhb/pau_db/40W/IMpa2.1/initValue"
        self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_D_KEY = "/rhb/pau_db/40W/IMpa3.1/initValue"
        self.FINAL_BIAS_PEAK_INIT_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_A_KEY,
                                         'B': self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_B_KEY,
                                         'C': self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_C_KEY,
                                         'D': self.FINALLY_DRIVER_40W_PABIAS_INIT_PEAK_D_KEY}

        self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_A_KEY = "/rhb/pau_db/40W/IMpa0.0/offset"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_B_KEY = "/rhb/pau_db/40W/IMpa1.0/offset"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_C_KEY = "/rhb/pau_db/40W/IMpa2.0/offset"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_D_KEY = "/rhb/pau_db/40W/IMpa3.0/offset"
        self.FINAL_BIAS_MAIN_OFFSET_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_A_KEY,
                                           'B': self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_B_KEY,
                                           'C': self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_C_KEY,
                                           'D': self.FINALLY_DRIVER_40W_PABIAS_MAIN_OFFSET_D_KEY}

        self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_A_KEY = "/rhb/pau_db/40W/IMpa0.1/offset"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_B_KEY = "/rhb/pau_db/40W/IMpa1.1/offset"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_C_KEY = "/rhb/pau_db/40W/IMpa2.1/offset"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_D_KEY = "/rhb/pau_db/40W/IMpa3.1/offset"
        self.FINAL_BIAS_PEAK_OFFSET_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_A_KEY,
                                           'B': self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_B_KEY,
                                           'C': self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_C_KEY,
                                           'D': self.FINALLY_DRIVER_40W_PABIAS_PEAK_OFFSET_D_KEY}

        self.FINALLY_DRIVER_40W_PABIAS_BACKOFFDAC_A_KEY = "/rhb/pau_db/40W/IMpa0.1/backoffDAC"
        self.FINALLY_DRIVER_40W_PABIAS_BACKOFFDAC_B_KEY = "/rhb/pau_db/40W/IMpa1.1/backoffDAC"
        self.FINALLY_DRIVER_40W_PABIAS_BACKOFFDAC_C_KEY = "/rhb/pau_db/40W/IMpa2.1/backoffDAC"
        self.FINALLY_DRIVER_40W_PABIAS_BACKOFFDAC_D_KEY = "/rhb/pau_db/40W/IMpa3.1/backoffDAC"

        self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_A_KEY = "/rhb/pau_db/IMpa0.0/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_B_KEY = "/rhb/pau_db/IMpa1.0/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_C_KEY = "/rhb/pau_db/IMpa2.0/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_D_KEY = "/rhb/pau_db/IMpa3.0/tempTab"
        self.FINAL_BIAS_MAIN_TEMP_TAB_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_A_KEY,
                                             'B': self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_B_KEY,
                                             'C': self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_C_KEY,
                                             'D': self.FINALLY_DRIVER_40W_PABIAS_MAIN_TEMP_D_KEY}

        self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_A_KEY = "/rhb/pau_db/IMpa0.1/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_B_KEY = "/rhb/pau_db/IMpa1.1/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_C_KEY = "/rhb/pau_db/IMpa2.1/tempTab"
        self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_D_KEY = "/rhb/pau_db/IMpa3.1/tempTab"
        self.FINAL_BIAS_PEAK_TEMP_TAB_KEY = {'A': self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_A_KEY,
                                             'B': self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_B_KEY,
                                             'C': self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_C_KEY,
                                             'D': self.FINALLY_DRIVER_40W_PABIAS_PEAK_TEMP_D_KEY}

        self.FINALLY_DRIVER_40W_PAVDD_OFFSET_A_KEY = "/rhb/pau_db/40W/mpaVdd:0/offset"
        self.FINALLY_DRIVER_40W_PAVDD_OFFSET_B_KEY = "/rhb/pau_db/40W/mpaVdd:1/offset"
        self.FINALLY_DRIVER_40W_PAVDD_OFFSET_C_KEY = "/rhb/pau_db/40W/mpaVdd:2/offset"
        self.FINALLY_DRIVER_40W_PAVDD_OFFSET_D_KEY = "/rhb/pau_db/40W/mpaVdd:3/offset"

        self.FINALLY_DRIVER_40W_PAVDD_TEMP_A_KEY = "/rhb/pau_db/mpaVdd:0/tempTab"
        self.FINALLY_DRIVER_40W_PAVDD_TEMP_B_KEY = "/rhb/pau_db/mpaVdd:1/tempTab"
        self.FINALLY_DRIVER_40W_PAVDD_TEMP_C_KEY = "/rhb/pau_db/mpaVdd:2/tempTab"
        self.FINALLY_DRIVER_40W_PAVDD_TEMP_D_KEY = "/rhb/pau_db/mpaVdd:3/tempTab"

        self.TX_40W_PWR_LOW_LIMIT_KEY = "/rhb/tx_db/tx:x/digpwr/lowLimit"
        self.TX_40W_PWR_HIGH_LIMIT_KEY = "/rhb/tx_db/tx:x/digpwr/highLimit"

        self.TOR_40W_PWR_LOW_LIMIT_KEY = "/rhb/fb_db/fb:x/digpwr/lowLimit"
        self.TOR_40W_PWR_HIGH_LIMIT_KEY = "/rhb/fb_db/fb:x/digpwr/highLimit"

        self.TOR_40W_PWR_FREQ_A_KEY = "/rhb/fb_db/fb:0/freTab"
        self.TOR_40W_PWR_FREQ_B_KEY = "/rhb/fb_db/fb:1/freTab"
        self.TOR_40W_PWR_FREQ_C_KEY = "/rhb/fb_db/fb:2/freTab"
        self.TOR_40W_PWR_FREQ_D_KEY = "/rhb/fb_db/fb:3/freTab"
        self.TOR_FREQ_TAB_KEY = {'A': self.TOR_40W_PWR_FREQ_A_KEY, 'B': self.TOR_40W_PWR_FREQ_B_KEY,
                                 'C': self.TOR_40W_PWR_FREQ_C_KEY, 'D': self.TOR_40W_PWR_FREQ_D_KEY}

        self.TOR_40W_PWR_TEMP_A_KEY = "/rhb/fb_db/fb:0/tempTab"
        self.TOR_40W_PWR_TEMP_B_KEY = "/rhb/fb_db/fb:1/tempTab"
        self.TOR_40W_PWR_TEMP_C_KEY = "/rhb/fb_db/fb:2/tempTab"
        self.TOR_40W_PWR_TEMP_D_KEY = "/rhb/fb_db/fb:3/tempTab"
        self.TOR_TEMP_TAB_KEY = {'A': self.TOR_40W_PWR_TEMP_A_KEY, 'B': self.TOR_40W_PWR_TEMP_B_KEY,
                                 'C': self.TOR_40W_PWR_TEMP_C_KEY, 'D': self.TOR_40W_PWR_TEMP_D_KEY}

        self.TOR_40W_PWR_TEMPREF_A_KEY = "/rhb/fb_db/fb:0/freqTab/tempRef"
        self.TOR_40W_PWR_TEMPREF_B_KEY = "/rhb/fb_db/fb:0/freqTab/tempRef"
        self.TOR_40W_PWR_TEMPREF_C_KEY = "/rhb/fb_db/fb:1/freqTab/tempRef"
        self.TOR_40W_PWR_TEMPREF_D_KEY = "/rhb/fb_db/fb:1/freqTab/tempRef"
        self.TOR_TEMP_REF_KEY = {'A': self.TOR_40W_PWR_TEMPREF_A_KEY, 'B': self.TOR_40W_PWR_TEMPREF_B_KEY,
                                 'C': self.TOR_40W_PWR_TEMPREF_C_KEY, 'D': self.TOR_40W_PWR_TEMPREF_D_KEY}

        self.TX_40W_DIF_PWR_LOW_LIMIT_KEY = "/rhb/tx_db/tx:x/pwrdif/lowEdge"
        self.TX_40W_DIF_PWR_HIGH_LIMIT_KEY = "/rhb/tx_db/tx:x/pwrdif/highEdge"

        self.TX_40W_DIF_PWR_THRESHOLD_KEY = "/rhb/tx_db/tx:x/pwrdif/threshold"

        self.TX_40W_DRUDSA_PWR_STEP_KEY = "/rhb/tx_db/tx:x/drudsa/step"
        self.TX_40W_DRUDSA_PWR_LOW_LIMIT_KEY = "/rhb/tx_db/tx:x/drudsa/lowLimit"
        self.TX_40W_DRUDSA_PWR_HIGH_LIMIT_KEY = "/rhb/tx_db/tx:x/drudsa/highLimit"

        self.TX_40W_DRUDIG_PWR_STEP_KEY = "/rhb/tx_db/tx:x/drudig/step"
        self.TX_40W_DRUDIG_PWR_LOW_LIMIT_KEY = "/rhb/tx_db/tx:x/drudig/lowLimit"
        self.TX_40W_DRUDIG_PWR_HIGH_LIMIT_KEY = "/rhb/tx_db/tx:x/drudig/highLimit"

        self.RX_40W_LINKGAIN_KEY = "/rhb/rx_db/linkGain"
        self.RX_40W_GAIN_TEMP_A_KEY = "/rhb/rx_db/rx:0/tempTab"
        self.RX_40W_GAIN_TEMP_B_KEY = "/rhb/rx_db/rx:1/tempTab"
        self.RX_40W_GAIN_TEMP_C_KEY = "/rhb/rx_db/rx:2/tempTab"
        self.RX_40W_GAIN_TEMP_D_KEY = "/rhb/rx_db/rx:3/tempTab"
        self.RX_TEMP_TAB_KEY = {'A': self.RX_40W_GAIN_TEMP_A_KEY, 'B': self.RX_40W_GAIN_TEMP_B_KEY,
                                'C': self.RX_40W_GAIN_TEMP_C_KEY, 'D': self.RX_40W_GAIN_TEMP_D_KEY}

        self.RX_40W_GAIN_FREQ_A_KEY = "/rhb/rx_db/rx:0/freTab"
        self.RX_40W_GAIN_FREQ_B_KEY = "/rhb/rx_db/rx:1/freTab"
        self.RX_40W_GAIN_FREQ_C_KEY = "/rhb/rx_db/rx:2/freTab"
        self.RX_40W_GAIN_FREQ_D_KEY = "/rhb/rx_db/rx:3/freTab"
        self.RX_FREQ_TAB_KEY = {'A': self.RX_40W_GAIN_FREQ_A_KEY, 'B': self.RX_40W_GAIN_FREQ_B_KEY,
                                'C': self.RX_40W_GAIN_FREQ_C_KEY, 'D': self.RX_40W_GAIN_FREQ_D_KEY}

        self.RX_40W_DELTA_DSA_LOW_EDGE_KEY = "/rhb/rx_db/rx:x/pwrdif/lowEdge"
        self.RX_40W_DELTA_DSA_HIGH_EDGE_KEY = "/rhb/rx_db/rx:x/pwrdif/highEdge"

        self.RX_40W_DELTA_DSA_THRESHOLD_KEY = "/rhb/rx_db/rx:x/pwrdif/threshold"
        self.RX_40W_DRUDSA_THRESHOLD_KEY = "/rhb/rx_db/rx:x/drudsa/increaseThreshold"
        self.RX_40W_DRUDSA_STEP_KEY = "/rhb/rx_db/rx:x/drudsa/step"

        self.RX_40W_PWR_TEMPREF_A_KEY = "/rhb/rx_db/rx:0/freTab/tempRef"
        self.RX_40W_PWR_TEMPREF_B_KEY = "/rhb/rx_db/rx:1/freTab/tempRef"
        self.RX_40W_PWR_TEMPREF_C_KEY = "/rhb/rx_db/rx:2/freTab/tempRef"
        self.RX_40W_PWR_TEMPREF_D_KEY = "/rhb/rx_db/rx:3/freTab/tempRef"
        self.RX_TEMP_REF_KEY = {'A': self.RX_40W_PWR_TEMPREF_A_KEY, 'B': self.RX_40W_PWR_TEMPREF_B_KEY,
                                'C': self.RX_40W_PWR_TEMPREF_C_KEY, 'D': self.RX_40W_PWR_TEMPREF_D_KEY}

        self.RX_40W_PWR_FREQ_REF_A_KEY = "/rhb/rx_db/rx:0/freTabRef"
        self.RX_40W_PWR_FREQ_REF_B_KEY = "/rhb/rx_db/rx:1/freTabRef"
        self.RX_40W_PWR_FREQ_REF_C_KEY = "/rhb/rx_db/rx:2/freTabRef"
        self.RX_40W_PWR_FREQ_REF_D_KEY = "/rhb/rx_db/rx:3/freTabRef"
        self.RX_REF_GAIN_KEY = {'A': self.RX_40W_PWR_FREQ_REF_A_KEY, 'B': self.RX_40W_PWR_FREQ_REF_B_KEY,
                                'C': self.RX_40W_PWR_FREQ_REF_C_KEY, 'D': self.RX_40W_PWR_FREQ_REF_D_KEY, }
