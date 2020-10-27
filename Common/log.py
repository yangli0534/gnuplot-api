# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-10-27

"""


import sys
sys.path.append(r'..\Station')
sys.path.append(r'..\Lib')
sys.path.append(r'..\Radio')

import logging

def setup_custom_logger(name, filename):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    #handler.setFormatter(formatter)
    # logging.basicConfig(level=logging.DEBUG,
    #                     filename=filename,
    #                     filemode='w',
    #                     format='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
    #                     )
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
