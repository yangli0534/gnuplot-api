# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""
from pathlib import Path

def get_folder_path():
    #filename = os.getcwd()
    #os.path.abspath(filename)
    path = Path().absolute()
    return path
