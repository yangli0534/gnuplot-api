# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:22:56 2020

@author: Integration
"""
import pyvisa
import time


class sa:
    def __init__(self, address):
        rm = pyvisa.ResourceManager()
        # instr = rm.open_resource('GPIB0::18::INSTR')
        self.instr = rm.open_resource(address)

    def write_value(self, cmd):
        self.instr.write(cmd)

    def read_value(self, cmd):
        self.write_value(cmd)
        return self.instr.read_ascii_values()

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
        cmd = f'CONF:{mode}'
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

    def test_chp(self, center, span, sweep_time, sweep_count, rbw, int_bw):
        self.set_mode('CHP')
        self.set_center(center)
        self.set_chp_span(span)
        self.set_chp_sweep_time(sweep_time)
        self.set_chp_rbw(rbw)
        self.set_chp_int_bw(int_bw)
        self.set_data_form('ASC')
        if sweep_count == 0:
            self.set_chp_trace_mode(0)
        else:
            self.set_chp_trace_mode(1)
            self.set_chp_aver_count(sweep_count)
        self.take_one_sweep()
        # need to add wait time if average mode
        time.sleep(sweep_time*sweep_count)
        return self.get_chp()


if __name__ == '__main__':
    mysa = sa('GPIB0::25::INSTR')
    chp1 = mysa.test_chp(3700, 10, 1, 0, 100, 5)
    print(chp1)
    print(type(chp1))
    chp2 = mysa.test_chp(3800, 10, 1, 5, 100, 5)
    print(chp2)
    print(type(chp2))
