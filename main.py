# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
import sys
sys.path.append('./RecordFile')
from GetRecordFileFolderPath import *

#Test Record File Module
path = GetRecordFileFolderPath()
print(path)