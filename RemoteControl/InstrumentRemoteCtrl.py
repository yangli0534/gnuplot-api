# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append('../RecordFile')
from GetRecordFileFolderPath import *

def instru_remote_ctrl(RecordName, ActionName, par, cmd, read, ctrlmode, ip, gpib):
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
    record_folder_path = get_folder_path()
