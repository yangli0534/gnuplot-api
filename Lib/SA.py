# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:22:56 2020

@author: Integration: Jimmy and Leon
"""
import pyvisa
import time
import datetime

class SA:
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # instr = rm.open_resource('GPIB0::18::INSTR')
        self._instr = rm.open_resource(address)
        self._instr.timeout = 10000
        self._instr.chunk_size = 102400
        self.name = self._instr.query('*IDN?')[:-1]
        self.set_init()
        print(f'{self.name} has been connected successfully' )


    def write_value(self, cmd):
        self._instr.write(cmd)

    def read_value(self, cmd):
        self.write_value(cmd)
        return self._instr.read_ascii_values()

    def set_cal(self):
        self.write_value(f':CAL')

    def set_cls(self):
        self.write_value(f'*CLS')

    def set_rst(self):
        self.write_value(f'*RST')

    def get_stb(self):
        return self.read_value(f'*STB?')

    def set_init(self):
        self.set_rst()

        #self.set_cal()
        #self.take_one_sweep()
        self.set_cls()
        self.set_unit()

    def set_close(self):
        self._instr.close()

    #set default unit to dBm
    def set_unit(self):
        cmd = 'UNIT:POW dBm'
        self.write_value(cmd)

    def set_span(self, target):
        cmd = f'FREQ:SPAN {target} MHz'
        self.write_value(cmd)

    def get_span(self):
        cmd = f'FREQ:SPAN?'
        return self.read_value(cmd)

    def set_start(self, target):
        cmd = f'FREQ:STAR {target} MHz'
        self.write_value(cmd)

    def get_start(self):
        cmd = f'FREQ:STAR?'
        return self.read_value(cmd)

    def set_stop(self, target):
        cmd = f'FREQ:STOP {target} MHz'
        self.write_value(cmd)

    def get_stop(self):
        cmd = f'FREQ:STOP?'
        return self.read_value(cmd)

    def set_center(self, target):
        cmd = f'FREQ:RF:CENT {target} MHz'
        self.write_value(cmd)

    def get_center(self):
        cmd = f'FREQ:RF:CENT?'
        return self.read_value(cmd)

    # set the rbw with unit kHz
    def set_rbw(self, target):
        cmd = f'BAND {target} kHz'
        self.write_value(cmd)

    def get_rbw(self):
        cmd = f'BAND?'
        return self.read_value(cmd)

    def set_vbw(self, target):
        cmd = f'BAND:VID {target} kHz'
        self.write_value(cmd)

    def get_vbw(self):
        cmd = f'BAND:VID?'
        return self.read_value(cmd)

    def set_sweep_time(self, target):
        cmd = f'SWE:TIME {target} s'
        self.write_value(cmd)

    def get_sweep_time(self):
        cmd = f'SWE:TIME?'
        return self.read_value(cmd)

    def set_sweep_point(self, target):
        cmd = f'SWE:POIN {target} s'
        self.write_value(cmd)

    def get_sweep_point(self):
        cmd = f'SWE:POIN?'
        return self.read_value(cmd)

    def set_y_offset(self, target):
        cmd = f'DISP:WIND:TRAC:Y:RLEV:OFFS {target}'
        self.write_value(cmd)

    def get_y_offset(self):
        cmd = f'DISP:WIND:TRAC:Y:RLEV:OFFS?'
        return self.read_value(cmd)

    def set_ref_level(self, target):
        cmd = f'DISP:WIND:TRAC:Y:RLEV {target}'
        self.write_value(cmd)

    def get_ref_level(self):
        cmd = f'DISP:WIND:TRAC:Y:RLEV?'
        return self.read_value(cmd)

    def set_att(self, target):
        cmd = f'POW:ATT {target} dB'
        self.write_value(cmd)

    def set_pow_gain(self):
        cmd = f'POW:GAIN OFF'
        self.write_value(cmd)

    def get_att(self):
        cmd = f'POW:ATT?'
        return self.read_value(cmd)

    def set_trigger(self, target):
        if target == 'free' or target == 'FREE':
            key = 'IMM'
        elif target == 'ext1' or target == 'EXT1':
            key = 'EXT1'
        else:
            pass
        cmd = f"TRIG:PULS:SOUR {key}"
        self.write_value(cmd)

    def set_gate_delay(self, target):
        cmd = f'SWE:EGAT:DEL {target} ms'
        self.write_value(cmd)

    def set_gate_len(self, target):
        cmd = f'SWE:EGAT:LENG {target} ms'
        self.write_value(cmd)

    # target = 'on' or 'off'
    def set_gate_stat(self, target):
        cmd = f'SWE:EGAT {target}'
        self.write_value(cmd)

    def set_fdd(self):
        self.set_trigger('IMM')
        self.set_gate_stat('OFF')

    def set_tdd(self, delay, length):
        self.set_trigger('EXT1')
        self.set_gate_delay(delay)
        self.set_gate_len(length)
        self.set_gate_stat('ON')

    def set_mode(self, mode):
        # 'SA': sweep analyzer
        # 'BASIC': IQ analyzer
        # 'PNOISE': phase noise
        # 'LTE': LTE module
        cmd = f'INST {mode}'
        self.write_value(cmd)


    def set_meas(self, meas):
        self.set_mode('SA')
        # 'SAN': Swept SA measurement
        # 'CHP': Channel power measurement
        # 'OBW': Occupied bandwidth measurement
        # 'ACP': Adjacent channel measurement
        # 'PST': Ccdf measurement
        # 'BPOW': Burst power measurement
        # 'SPUR': Spurious emissions measurement
        # 'SEM': Spectrum emission mask measurement
        # 'TOI': TOI measurement
        # 'HARM': Harmonics measurement
        # 'LIST': List sweep measurement
        cmd = f'CONF:{meas}'
        self.write_value(cmd)

    def set_cont(self, target):
        # target = 1, continuos meas/sweep enable
        # target = 0, continuos meas/sweep disable
        cmd = f'INIT:CONT {target}'
        self.write_value(cmd)

    def set_chp_span(self, target):
        cmd = f'CHP:FREQ:SPAN {target} MHz'
        self.write_value(cmd)

    def set_chp_sweep_time(self, target):
        cmd = f'CHP:SWE:TIME {target} s'
        self.write_value(cmd)

    def set_chp_rbw(self, target):
        cmd = f'CHP:BAND {target} kHz'
        self.write_value(cmd)

    def set_chp_trace_mode(self, target):
        cmd = f'CHP:AVER {target}'
        self.write_value(cmd)

    def set_chp_aver_count(self, target):
        cmd = f'CHP:AVER:COUN {target}'
        self.write_value(cmd)

    # target unit is MHz
    def set_chp_int_bw(self, target):
        cmd = f'CHP:BAND:INT {target} MHz'
        self.write_value(cmd)

    def set_chp_scale(self, target):
        cmd = f'DISP:CHP:VIEW:WIND:TRAC:Y:PDIV {target}'
        self.write_value(cmd)
    def set_chp_scale_auto(self):
        cmd = f'DISP:CHP:VIEW:WIND:TRAC:Y:COUP ON'
        self.write_value(cmd)

    # target unit dBm
    # set reference level
    def set_acp_rlev(self, target):
        cmd = f':DISP:ACP:VIEW:WIND:TRAC:Y:RLEV {target} '
        self.write_value(cmd)

    # target  unit db
    # set amplitude offset
    # def set_acp_rlev_offs(self, target):
    #     cmd = f'DISP:WIND:TRAC:Y:RLEV:OFFS {target}'
    #     self.write_value(cmd)

    #
    def set_acp_band_rbw(self, target):
        cmd = f':ACP:BAND {target} KHz'
        self.write_value(cmd)

    def set_acp_band_vbw(self, target):
        cmd = f':ACP:BAND:VID {target} KHz '
        self.write_value(cmd)

    def set_acp_aver(self, target):
        #
        if target == 0:
            cmd = f':ACP:AVER:STAT 0'
        else:
            cmd = f':ACP:AVER:COUN {target}'
        self.write_value(cmd)

    def set_acp_carr_num(self, target):
        #target is carrier number,
        cmd = f':ACP:CARR:COUN {target} '
        self.write_value(cmd)

    def set_acp_carr_freq(self, target):
        #target is carrier center frequency,
        cmd = f':ACP:CARR:RCFR {target} MHz'
        self.write_value(cmd)

    def set_acp_carr_list_widt(self, target):
        #target is integration bandwidth,
        cmd = f':ACP:CARR:LIST:WIDT {target} MHz'
        self.write_value(cmd)

    def set_acp_carr_list_band(self, target):
        #target is carrier bandwidth,
        cmd = f':ACP:CARR:LIST:BAND {target} MHz'
        self.write_value(cmd)

    def set_acp_offs_list_stat(self):
        #
        cmd = f':ACP:OFFS:LIST:STAT 1, 1, 0, 0, 0, 0'
        self.write_value(cmd)

    def set_acp_offs_list_freq(self, target1, target2):
        #target is aclr offset frequency
        cmd = f':ACP:OFFS:LIST:FREQ {target1} MHz, {target2} MHz'
        self.write_value(cmd)

    def set_acp_offs_list_band(self, target1, target2):
        #target is aclr integration frequency
        cmd = f':ACP:OFFS:LIST:BAND {target1} MHz, {target2} MHz'
        self.write_value(cmd)

    def set_acp_offs_list_limit(self):
        #
        cmd = f':ACP:OFFS:LIST:RCAR -45, -60, 0, 0, 0, 0'
        self.write_value(cmd)
        cmd = f':ACP:OFFS:LIST:TEST REL, REL, REL, REL, REL, REL'
        self.write_value(cmd)
    def set_acp_calc_stat(self):
        cmd = f':CALC:ACP:LIM:STAT ON'
        self.write_value(cmd)

    def set_acp_meth(self):
        #
        cmd = f':ACP:METH IBW'
        self.write_value(cmd)

    def set_acp_psd_unit(self):
        cmd = f'UNIT:ACP:POW:PSD DBMHZ'
        self.write_value(cmd)

    def set_acp_lim_stat(self):
        cmd = f':CALC:ACP:LIM:STAT ON'
        self.write_value(cmd)

    def set_acp_span(self, target):
        cmd = f':ACP:FREQ:SPAN {target} MHz'
        self.write_value(cmd)


    def set_acp_sweep_time(self, target):
        #target unit is ms
        cmd = f':ACP:SWE:TIME {target}ms'
        self.write_value(cmd)

    def set_acp_det(self):
        cmd = f':ACP:DET AVER'
        self.write_value(cmd)

    # sa parameter define
    # target unit dBm
    # set reference level
    def set_rlev(self, target):
        cmd = f':DISP:WIND:TRAC:Y:RLEV {target} '
        self.write_value(cmd)

        # target  unit db
        # set amplitude offset

    def set_rlev_offs(self, target):
        cmd = f'DISP:WIND:TRAC:Y:RLEV:OFFS {target}'
        self.write_value(cmd)

        #

    def set_rbw(self, target):
        cmd = f':BAND {target} KHz'
        self.write_value(cmd)

    def set_vbw(self, target):
        cmd = f':BAND:VID {target} KHz '
        self.write_value(cmd)

    def set_aver(self, target):
        #
        if target == 0:
            cmd = f':AVER:STAT 0'
        else:
            cmd = f':AVER:COUN {target}'
        self.write_value(cmd)




    def set_san_meth(self):
        #
        cmd = f':SA:METH IBW'
        self.write_value(cmd)

    # def set_sa_span(self, target):
    #     cmd = f':SA:FREQ:SPAN {target} MHz'
    #     self.write_value(cmd)

    # def set_sa_sweep_time(self, target):
    #     # target unit is ms
    #     cmd = f':sa:SWE:TIME {target}ms'
    #     self.write_value(cmd)

    def set_san_det(self):
        cmd = f':sa:DET AVER'
        self.write_value(cmd)

    def set_data_form(self, target):
        # 'ASC': ASCii
        # 'REAL,32': real
        cmd = f':FORM:DATA {target}'
        self.write_value(cmd)
        if format == 'REAL,32':
            cmd = f':FORM:BORD SWAP'
            self.write_value(cmd)

    def take_one_sweep(self):
        self.write_value('INIT;*WAI')

    def get_chp(self):
        cmd = 'FETCh:CHPower:CHPower?'
        return self.read_value(cmd)

    def set_cd(self, cd):
        cmd = f'MMEM:CDIR {cd}'
        self.write_value(cmd)

    def set_acp_title(self, title):
        #cmd = f':DISP:ANN:TITL:DATA "{title}"'
        #self.write_value(cmd)
        cmd = f':DISP:ACP:ANN:TITL:DATA "{title}"'
        self.write_value(cmd)
        #cmd = f':DISP:WIND1:TITL ON'
        #self.write_value(cmd)

    def set_chp_title(self, title):
        #cmd = f':DISP:ANN:TITL:DATA "{title}"'
        #self.write_value(cmd)
        cmd = f':DISP:CHP:ANN:TITL:DATA "{title}"'
        self.write_value(cmd)
        #cmd = f':DISP:WIND1:TITL ON'
        #self.write_value(cmd)


    def set_title(self, title):
        cmd = f':DISP:ANN:TITL:DATA "{title}"'
        self.write_value(cmd)

    def get_trace(self):
         self.take_one_sweep()
         cmd = f'TRAC? TRACE1'
         #self.write_value(cmd)
         return self.read_value(cmd)

    def get_scr(self, filename):
        cmd = ':MMEM:CDIR "D:\\User_My_Documents\\Administrator\\My Documents\\SA\\screen"'
        self.write_value(cmd)

        cmd = f'MMEM:STOR:SCR "{filename}"'
        self.write_value(cmd)

        cmd = f'MMEM:DATA? "{filename}"'
        capture = self._instr.query_binary_values(message = cmd, container = list, datatype ='c')
        with open(filename, 'wb') as fp:
            for byte in capture:
                fp.write(byte)
        # Delete the file from memory
        fp.close()
        cmd = f'MMEM:DEL "{filename}"'
        self.write_value(cmd)

        print(f'{filename} has been saved on PC')

    def test_chp(self, center, sweep_time, sweep_count, rbw, int_bw, rlev, offs, scale = 5):
        self.set_init()
        self.set_meas('CHP')
        self.set_center(center)
        #self.set_chp_span(span)
        self.set_rlev(rlev)
        self.set_rlev_offs(offs)
        #self.set_chp_scale(scale)
        self.set_chp_scale_auto()
        self.set_chp_sweep_time(sweep_time)
        self.set_chp_rbw(rbw)
        self.set_chp_int_bw(int_bw)
        self.set_data_form('ASC')
        self.set_cont(1)
        if sweep_count == 0:
            self.set_chp_trace_mode(0)
        else:
            self.set_chp_trace_mode(1)
            self.set_chp_aver_count(sweep_count)
        self.take_one_sweep()
        # need to add wait time if average mode
        time.sleep(sweep_time*sweep_count)
        self.set_chp_title('O-RU ACP Measurement')
        return self.get_chp()


    def test_acp(self, center, span, sweep_time, sweep_count, rbw, vbw, rlev, offs,cbw,obw):
        self.set_init()
        #self.set_acp_init()
        self.set_meas('ACP')
        self.set_att(16)
        self.set_pow_gain()
        self.set_cont(1)
        self.set_center(center)
        self.set_acp_span(span)
        self.set_acp_rlev(rlev)
        self.set_rlev_offs(offs)
        self.set_acp_aver(sweep_count)
        self.set_acp_sweep_time(sweep_time)
        self.set_acp_band_rbw(rbw)
        self.set_acp_band_vbw(vbw)
        self.set_acp_carr_num(1)
        self.set_acp_carr_freq(center)
        self.set_acp_carr_list_band(obw)
        self.set_acp_carr_list_widt(obw)
        self.set_acp_offs_list_stat()
        self.set_acp_offs_list_freq(cbw, cbw*2)
        self.set_acp_offs_list_band(obw, obw)
        self.set_acp_offs_list_limit()
        self.set_acp_calc_stat()
        self.set_acp_title('O-RU ACLR Measurement')

    def test_san(self, center, span, sweep_time, sweep_count, rbw, vbw, rlev, offs):
        self.set_init()
        #self.set_acp_init()
        self.set_meas('SAN')
        self.set_att(16)
        self.set_pow_gain()
        self.set_cont(1)
        self.set_center(center)
        self.set_span(span)
        self.set_rlev(rlev)
        self.set_rlev_offs(offs)
        self.set_aver(sweep_count)
        #self.set_sa_sweep_time(sweep_time)
        self.set_rbw(rbw)
        self.set_vbw(vbw)

        self.set_title('O-RU SA Measurement')

    def test(self):
        self.set_title('O-RU ACLR measurement')

    def __del__(self):
        self.set_close()
        print('SA has been disconnected')


if __name__ == '__main__':
    #mysa = SA('GPIB0::25::INSTR')
    mysa = SA('TCPIP0::172.16.1.66::inst0::INSTR')
    chp1 = mysa.test_chp(center=3700, sweep_time=0.05, sweep_count=10, rbw=100, int_bw=98.3, rlev = 20, offs = 41.7)
    #print(chp1)


    # print(type(chp1))
    # chp2 = mysa.test_chp(3800, 10, 1, 0, 100, 5)
    # print(chp2)
    # print(type(chp2))
    #mysa.test_acp(center=3000, span=10, sweep_time=50, sweep_count=10, rbw=0.5, vbw=1, rlev=15, offs=0.6, cbw=2, obw=1.8)
    #mysa.test_san(center=3000, span=500, sweep_time=50, sweep_count=10, rbw=10, vbw=30, rlev=0, offs=0.7)
    # for i in range(1):
    #     dt = datetime.datetime.now()
    #     #     #chp1 = mysa.test_chp(3700, 100, 1, 0, 100, 5)
    #     mysa.test_acp(center=3000, span=300, sweep_time=50, sweep_count=10, rbw=100, vbw=300, rlev=15, offs=0.6, cbw=500, obw=45)
    #     #chp1 = mysa.test_chp(3700, 10, 1, 0, 100, 5)
    #     #print(chp1)
    #     mysa.take_one_sweep()
    #     filename = dt.strftime("MSO5_%Y%m%d_%H%M%S.png")
    #     mysa.get_scr(filename)
    #mysa.test()
    #trace = mysa.get_trace()
    #print(len(trace))
    mysa.set_close()
