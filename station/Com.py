# -*- coding: utf-8 -*-
"""
@author: Jimmy
"""
import serial
import re
import time



class Com:
    def __init__(self, com_id, baud_rate, t):
        port = 'COM' + str(com_id)
        self.com = serial.Serial(port, baud_rate, timeout=t)
        if self.com.isOpen():
            print("COM port create and open successfully")
        else:
            print("COM create failed")
        self.iv = self.is_virtual()

    def receive_data(self):
        output = ''
        while True:
            data = self.com.readline()
            try:
                if data != b'':
                    output = output + data.decode('utf-8')
                    #print(data.decode('utf-8'), end='')
                else:
                    break
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
        self.com.write(cmd.encode('utf-8'))

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
    a = Com(1, 115200, 0.5)
    for i in range(10):
        a.send_cmd('fpga r 0x1807')
        time.sleep(1)
    a.close()
