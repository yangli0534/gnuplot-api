# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append('./RecordFile')
sys.path.append('./Station')

from GetRecordFileFolderPath import *
from Station import *

#Test Record File Module
path = get_folder_path()
print(path)

for i in instru_remote_ctrl:
    for j in i:
        print(j)