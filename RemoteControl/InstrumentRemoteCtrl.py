# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""

def InstrumentRemoteCtrl(RecordName, ActionName, par, cmd, read, ctrlmode, ip, gpib):
    """
    
    :param RecordName: 
    :param ActionName: if ActionName~= '*' then other input parameter is optional,'par' can be '-','*' or nothing
                       else cmd is mandatory,other is optional,'par' can be '-','*' or nothing
    :param par: 
    :param cmd: 
    :param read: 
    :param ctrlmode: 
    :param ip: 
    :param gpib: 
    :return: 
    """