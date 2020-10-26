# -*- coding: utf-8 -*-
"""
@author: Jimmy
"""
import serial
import re
import time
import sys



class Com:
    def __init__(self, com_id, baud_rate, t):
        port = 'COM' + str(com_id)
        try:
            self.com = serial.Serial(port, baud_rate, timeout=t)
            print("COM port create and open successfully")
            #return True
        except:
            print(f'COM{com_id} is not available so fail to open!!!')
            sys.exit('stop running')
            #return False
        # if self.com.isOpen():
        #     print("COM port create and open successfully")
        # else:
        #     print("COM create failed")
        self.iv = self.is_virtual()

    def __read_line_cus(self, terminator):
        eol = b'\r'
        leneol = len(eol)
        ter_eol = len(terminator)
        line = bytearray()
        while True:
            c = self.com.read(1)
            if c:
                line += c
                if line[-leneol:] == eol or (line[-ter_eol:] == terminator):
                    break
            else:
                break
        return bytes(line)

    def receive_data(self):

        output = ''
        flag = 1
        while flag:
            data = self.__read_line_cus(b'root@ORU1226:~#')
            try:
                if re.search('root@ORU1226:~#', str(data), re.M | re.I) is not None:
                    flag = 0
                    output = output + data.decode('utf-8')
                    #print(data.decode('utf-8'), end='\n')
                else:
                    output = output + data.decode('utf-8')
                    #print(data.decode('utf-8'), end='')
            except Exception as err:
                print('Error %s in reading', err)

        return output

    def send_read_cmd(self, cmd):
        cmd = self.carriage_return(cmd)
        self.com.write(cmd.encode('utf-8'))
        #print(cmd)
        return self.receive_data()

    def send_cmd(self, cmd):
        cmd = self.carriage_return(cmd)
        #print('cmd')
        self.com.write(cmd.encode('utf-8'))
        self.receive_data()

    def read_raw_reg(self, cmd):
        cmd = self.carriage_return(cmd)
        self.com.write(cmd.encode('utf-8'))
        data = self.receive_data()
        data = data.split('\r\n')
        reg_data = data[1]
        reg_data = reg_data.split(' ')
        return reg_data[-1]

    def close(self):
        self.com.close()
        # print("COM_close finished")

    def open(self):
        self.com.open()
        # print("COM_open finished")

    def is_virtual(self):
        com_id = self.com.port
        com_id = re.findall(r'\d+', com_id)
        com_id = int(com_id[0])
        if com_id < 10:
            return 0
        else:
            return 1

    def carriage_return(self, cmd):
        iv = self.iv
        if iv == 1:
            cmd = cmd + '\r'
        else:
            cmd = cmd + '\n'
        return cmd

    def send_multi_cmd(self, multi_cmd):
        if len(multi_cmd[1]) == 1:
            self.send_read_cmd(multi_cmd)
        else:
            for i in range(len(multi_cmd)):
                self.send_read_cmd(multi_cmd[i-1])

    def fpga_write(self, add, value):
        cmd = 'fpga w ' + add + ' ' + value
        self.send_cmd(cmd)

    def spi_write(self, device, add, value):
        cmd = 'spi ' + device + ' w ' + add + ' ' + value
        self.send_cmd(cmd)

    def spi_read(self, device, add):
        cmd = 'spi ' + device + ' r ' + add
        data = self.read_raw_reg(cmd)
        return data

    def read_db(self, cmd):
        out = self.send_read_cmd(cmd)
        return out

    def __del__(self):
        print('COM has been disconnected')
        self.close()


if __name__ == '__main__':
    a = Com(3, 115200, 1)
    for i in range(1):
        start = time.perf_counter()
        a.send_read_cmd('spi paCtrl temp A')
        stop = time.perf_counter()
        cost_time = stop - start
        print(f'Total time is {cost_time} s')
        time.sleep(1)
    a.close()
