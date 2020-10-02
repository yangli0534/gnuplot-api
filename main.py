# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append('./RecordFile')
sys.path.append('./Station')

from GetRecordFileFolderPath import *
from InstrumentAddrConfig import *

#Test Record File Module
path = get_folder_path()
print(path)

for key in inst_addr_conf:
        print(inst_addr_conf[key])