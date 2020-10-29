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

import Station

mybench = Station.Station()
print(mybench.get_tx_IL(3700))