# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append('../RecordFile')
sys.path.append('../Station')
from get_record_file_folder_path import *
from instrument_addr_config import *
def instr_remote_ctrl(record_name, action_name, par, cmd, read, ctrl_mode, ip, gpib):
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

    # action_name == '*' means other parameter will be used as input
    if( ('action_name' in locals().keys()) and not (action_name = '*')):