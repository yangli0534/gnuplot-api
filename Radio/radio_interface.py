# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-19-20

"""
import sys
sys.path.append(r'D:\code\visa_tutorials\Station')
sys.path.append(r'D:\code\visa_tutorials\Lib')

import Com
import PS
import time
import re
from threading import Thread


class RU:
    def __init__(self, com_id, baud_rate, t):
        self._mycom = Com.Com(3, 115200, 0.5)
        connect_status = 0
        while connect_status == 0:
            time.sleep(1)
            answer = self._mycom.send_read_cmd('')
            # answer = mycom.receive_data()
            # answer = answer.rstrip()
            #print(answer)
            # print([ord(c) for c in answer])
            # print([ord(c) for c in 'root@ORU4419:~#'])
            terminator = 'root@ORU1226:~#'
            search_obj = re.search(terminator, answer, re.M | re.I)
            if search_obj:
                connect_status = 1
                print('RU connected successful')
            else:
                print('Connecting...')

    #def write(self):

    def __branch_def(self, branch_id):
        branch_id = str(branch_id)
        branch_def = {'0':'A','1':'B','2':'C','3':'D','A':'A','B':'B','C':'C','D':'D','a':'A','b':'B','c':'C','d':'D'}
        return branch_def[branch_id]

    def read_temp_PA(self, branch):
        temp = self._mycom.send_read_cmd(f' spi paCtrl temp {self.__branch_def(branch)}')
        PA_temp = float(re.findall(r"Reading PA temperature :(.+?)\n", temp)[0].strip())
        return PA_temp



    def __del__(self):
        print('RU has been disconnected')

if __name__ == '__main__':
    myRU = RU(com_id = 3 , baud_rate = 115200 , t = 1)
    #active = True
    try:
        while True:
            temp = myRU.read_temp_PA('A')
            print(f'branch A PA temperature is {temp} ')
            temp = myRU.read_temp_PA('B')
            print(f'branch B PA temperature is {temp} ')
            temp = myRU.read_temp_PA('C')
            print(f'branch C PA temperature is {temp} ')
            temp = myRU.read_temp_PA('D')
            print(f'branch D PA temperature is {temp} ')

    except KeyboardInterrupt:
        pass
