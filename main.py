# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
from station import Com


if __name__ == '__main__':
    com_obj = ruCom.Com(6, 115200, 0.5)
    handle = TX_On.TxHandle(com_obj)
    handle.send_iq_data()
