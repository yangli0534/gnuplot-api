# -*- coding: utf-8 -*-

"""
@author: Leon
@time: 2020-09-20

"""

#SA_cmd_set = {'action':{'Reset', 'SetRefLevel', 'SetRefAtt', 'SetRBW', 'SetVBW', 'SetTrace1Mode', 'SetDetector',
#                        'SetSweepTime', 'SetSpan', 'SetCenterFrequency', 'EnableMarker1', 'SetMarker1Freq',
#                        'SetDataFormat', 'SetDest', 'SetFileFormat', 'SetFileNameAndPath', 'SetFileItem',
#                        'SetFileComment', 'StoreFile', 'SetNextStoreFileName', 'SetTrigSourceFreeRun', 'SetTrigSourceEXT',
#                        'SetTrigSourceEXT1', 'SetContinousOff', 'SetContinousOn', 'SetAverCount', 'SetAverOff',
#                        'SetAverOn', 'SetAcpSpace', 'SetRefLevOffset', 'SetMode', 'SetAcpMeas', 'SetAcpStandard',
#                        'SetAcpTxChCnt', 'SetAcpAdjChCnt', 'SetAcpRefCh', 'SetAcpMode', 'SetAcpTx1Bw', 'SetAcpAchBw',
#                        'SetAcpAlt1Bw', 'SetAcpAchSpace', 'SetAcpAlt1Space', 'SetAcpAchLimit', 'SetAcpAlt1Limit',
#                        'SetAcpLimitCheck', 'SetAcpAchLimCheck', 'SetAcpAlt1LimCheck', 'WaitForFinish', 'GetAcpAchRes',
#                        'GetAcpAlt1Res', 'GetAcpResults', 'GetRBW', 'GetMarker1Value', 'GetFreqStart', 'GetFreqStop',
#                        'GetSweepPointNum', 'GetTrace1', 'GetTrace2', 'GetTrace3', 'GetTrace4', 'GetTrace5', 'GetTrace6',
#                        'GetFileFromSA'},
#              'command':{'*RST', 'DISP:TRAC:Y:RLEV',  'INP:ATT', 'BAND', 'BAND:VID', 'DISP:TRAC1:MODE', 'DET', 'SWE:TIME',
#                         'FREQ:SPAN', 'FREQ:CENT', 'CALC:MARK1', 'CALC:MARK1:X', 'FORMAT', 'HCOP:DEST', 'HCOP:DEV:LANG',
#                         'MMEM:NAME', 'HCOP:ITEM:ALL', 'HCOP:ITEM:WIND:TEXT', 'HCOP:IMM', 'HCOP:NEXT', 'TRIGGER:SOURCE',
#                         'TRIGGER:SOURCE', 'TRIGGER:SOURCE', 'INIT:CONT', 'INIT:CONT', 'AVER:COUN', 'AVER', 'AVER',
#                         'POW:ACH:SPAC', 'DISP:TRAC:Y:RLEV:OFFS', 'INST', 'CALC:MARK:FUNC:POW:SEL',
#                         'CALC:MARK:FUNC:POW:PRES', 'POW:ACH:TXCH:COUN', 'POW:ACH:ACP', 'POW:ACH:REF:TXCH:MAN',
#                         'POW:ACH:MODE', 'POW:ACH:BWID:CHAN1', 'POW:ACH:BWID:ACH', 'POW:ACH:BWID:ALT1', 'POW:ACH:SPAC',
#                         'POW:ACH:SPAC:ALT1', 'CALC:LIM:ACP:ACH', 'CALC:LIM:ACP:ALT1', 'CALC:LIM:ACP',
#                         'CALC:LIM:ACP:ACH:STAT', 'CALC:LIM:ACP:ALT1:STAT', 'INIT;*WAI', 'CALC:LIM:ACP:ACH:RES?',
#                         'CALC:LIM:ACP:ALT1:RES?', 'CALC:MARK:FUNC:POW:RES?', 'BAND?', 'CALC:MARK1:Y?', 'FREQ:START?',
#                         'FREQ:STOP?', 'SENS:SWE:POIN?', 'TRAC?', 'TRAC?', 'TRAC?', 'TRAC?', 'TRAC?', 'TRAC?', 'MMEM:DATA?'},
#              'cmd_par':{'-', '-10dBm', '0dB', '0.03MHz', '0.3MHz', 'WRIT', 'RMS', '1s', '120MHz', '1940MHz', 'ON',
#                         '2MHz', 'REAL,32', '', 'MMEM', '', 'PNG', '', 'C:\Screenshot.png', '', '-', '', 'test', '',
#                         '-', '-', 'IMM', 'EXT', 'EXT1', 'Off', 'ON', '0', 'OFF', 'On', '5MHz', '60dB', 'LTE', 'ACP',
#                         'NONE', '1', '2', '1', 'REL', '5MHz', '5MHz', '5MHz', '5MHz', '10MHz', '-45DB,-45DB',
#                         '-45DB,-45DB', 'ON', 'ON', 'ON', '-', '-', '-', 'ACP', '-', '-', '-', '-', '-', 'TRACE1',
#                         'TRACE2' 'TRACE3', 'TRACE4', 'TRACE5', 'TRACE6', '', 'C:\Screenshot.png', ''},
#              'rd_wr_flag':{'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
#                                 '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
#                                 '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1',
#                                 '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0'}
#
#}
#

SA_CMD_SET = {
    "Reset":{                "Cmd": "*RST",                     "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetRefLevel":{          "Cmd": "DISP:TRAC:Y:RLEV",         "CmdPar": "-10dBm",                "RdWrFlag": "0"},
    "SetRefAtt":{            "Cmd": "INP:ATT",                  "CmdPar": "0dB",                   "RdWrFlag": "0"},
    "SetRBW":{               "Cmd": "BAND",                     "CmdPar": "0.03MHz",               "RdWrFlag": "0"},
    "SetVBW":{               "Cmd": "BAND:VID",                 "CmdPar": "0.3MHz",                "RdWrFlag": "0"},
    "SetTrace1Mode":{        "Cmd": "DISP:TRAC1:MODE",          "CmdPar": "WRIT",                  "RdWrFlag": "0"},
    "SetDetector":{          "Cmd": "DET",                      "CmdPar": "RMS",                   "RdWrFlag": "0"},
    "SetSweepTime":{         "Cmd": "SWE:TIME",                 "CmdPar": "1s",                    "RdWrFlag": "0"},
    "SetSpan":{              "Cmd": "FREQ:SPAN",                "CmdPar": "120MHz",                "RdWrFlag": "0"},
    "SetCenterFrequency":{   "Cmd": "FREQ:CENT",                "CmdPar": "1940MHz",               "RdWrFlag": "0"},
    "EnableMarker1":{        "Cmd": "CALC:MARK1",               "CmdPar": "ON",                    "RdWrFlag": "0"},
    "SetMarker1Freq":{       "Cmd": "CALC:MARK1:X",             "CmdPar": "2MHz",                  "RdWrFlag": "0"},
    "SetDataFormat":{        "Cmd": "FORMAT",                   "CmdPar": "REAL,32",               "RdWrFlag": "0"},
    "SetDest":{              "Cmd": "HCOP:DEST",                "CmdPar": "'MMEM'",                "RdWrFlag": "0"},
    "SetFileFormat":{        "Cmd": "HCOP:DEV:LANG",            "CmdPar": "PNG",                   "RdWrFlag": "0"},
    "SetFileNameAndPath":{   "Cmd": "MMEM:NAME",                "CmdPar": "'C:\Screenshot.png'",   "RdWrFlag": "0"},
    "SetFileItem":{          "Cmd": "HCOP:ITEM:ALL",            "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetFileComment":{       "Cmd": "HCOP:ITEM:WIND:TEXT",      "CmdPar": "'test'",                "RdWrFlag": "0"},
    "StoreFile":{            "Cmd": "HCOP:IMM",                 "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetNextStoreFileName":{ "Cmd": "HCOP:NEXT",                "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetTrigSourceFreeRun":{ "Cmd": "TRIGGER:SOURCE",           "CmdPar": "IMM",                   "RdWrFlag": "0"},
    "SetTrigSourceEXT":{     "Cmd": "TRIGGER:SOURCE",           "CmdPar": "EXT",                   "RdWrFlag": "0"},
    "SetTrigSourceEXT1":{    "Cmd": "TRIGGER:SOURCE",           "CmdPar": "EXT1",                  "RdWrFlag": "0"},
    "SetContinousOff":{      "Cmd": "INIT:CONT",                "CmdPar": "Off",                   "RdWrFlag": "0"},
    "SetContinousOn":{       "Cmd": "INIT:CONT",                "CmdPar": "ON",                    "RdWrFlag": "0"},
    "SetAverCount":{         "Cmd": "AVER:COUN",                "CmdPar": "0",                     "RdWrFlag": "0"},
    "SetAverOff":{           "Cmd": "AVER",                     "CmdPar": "OFF",                   "RdWrFlag": "0"},
    "SetAverOn":{            "Cmd": "AVER",                     "CmdPar": "On",                    "RdWrFlag": "0"},
    "SetAcpSpace":{          "Cmd": "POW:ACH:SPAC",             "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetRefLevOffset":{      "Cmd": "DISP:TRAC:Y:RLEV:OFFS",    "CmdPar": "60dB",                  "RdWrFlag": "0"},
    "SetMode":{              "Cmd": "INST",                     "CmdPar": "LTE",                   "RdWrFlag": "0"},
    "SetAcpMeas":{           "Cmd": "CALC:MARK:FUNC:POW:SEL",   "CmdPar": "ACP",                   "RdWrFlag": "0"},
    "SetAcpStandard":{       "Cmd": "CALC:MARK:FUNC:POW:PRES",  "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "SetAcpTxChCnt":{        "Cmd": "POW:ACH:TXCH:COUN",        "CmdPar": "1",                     "RdWrFlag": "0"},
    "SetAcpAdjChCnt":{       "Cmd": "POW:ACH:ACP",              "CmdPar": "2",                     "RdWrFlag": "0"},
    "SetAcpRefCh":{          "Cmd": "POW:ACH:REF:TXCH:MAN",     "CmdPar": "1",                     "RdWrFlag": "0"},
    "SetAcpMode":{           "Cmd": "POW:ACH:MODE",             "CmdPar": "REL",                   "RdWrFlag": "0"},
    "SetAcpTx1Bw":{          "Cmd": "POW:ACH:BWID:CHAN1",       "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpAchBw":{          "Cmd": "POW:ACH:BWID:ACH",         "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpAlt1Bw":{         "Cmd": "POW:ACH:BWID:ALT1",        "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpAchSpace":{       "Cmd": "POW:ACH:SPAC",             "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpAlt1Space":{      "Cmd": "POW:ACH:SPAC:ALT1",        "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "SetAcpAchLimit":{       "Cmd": "CALC:LIM:ACP:ACH",         "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "SetAcpAlt1Limit":{      "Cmd": "CALC:LIM:ACP:ALT1",        "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "SetAcpLimitCheck":{     "Cmd": "CALC:LIM:ACP",             "CmdPar": "ON",                    "RdWrFlag": "0"},
    "SetAcpAchLimCheck":{    "Cmd": "CALC:LIM:ACP:ACH:STAT",    "CmdPar": "ON",                    "RdWrFlag": "0"},
    "SetAcpAlt1LimCheck":{   "Cmd": "CALC:LIM:ACP:ALT1:STAT",   "CmdPar": "ON",                    "RdWrFlag": "0"},
    "WaitForFinish":{        "Cmd": "INIT;*WAI",                "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetAcpAchRes":{         "Cmd": "CALC:LIM:ACP:ACH:RES?",    "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetAcpAlt1Res":{        "Cmd": "CALC:LIM:ACP:ALT1:RES?",   "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetAcpResults":{        "Cmd": "CALC:MARK:FUNC:POW:RES?",  "CmdPar": "ACP",                   "RdWrFlag": "1"},
    "GetRBW":{               "Cmd": "BAND?",                    "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetMarker1Value":{      "Cmd": "CALC:MARK1:Y?",            "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetFreqStart":{         "Cmd": "FREQ:START?",              "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetFreqStop":{          "Cmd": "FREQ:STOP?",               "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetSweepPointNum":{     "Cmd": "SENS:SWE:POIN?",           "CmdPar": "-",                     "RdWrFlag": "1"},
    "GetTrace1":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE1",                "RdWrFlag": "0"},
    "GetTrace2":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE2",                "RdWrFlag": "0"},
    "GetTrace3":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE3",                "RdWrFlag": "0"},
    "GetTrace4":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE4",                "RdWrFlag": "0"},
    "GetTrace5":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE5",                "RdWrFlag": "0"},
    "GetTrace6":{            "Cmd": "TRAC?",                    "CmdPar": "TRACE6",                "RdWrFlag": "0"},
    "GetFileFromSA":{        "Cmd": "MMEM:DATA?",               "CmdPar": "'C:\Screenshot.png'",   "RdWrFlag": "0"}

}

SA_CMD_SET_GET_ACP = {
    "S01":{                    "Cmd": "INIT;*WAI",                "CmdPar": "-",                     "RdWrFlag": "1"},
    "S02":{                    "Cmd": "CALC:LIM:ACP:ACH:RES?",    "CmdPar": "-",                     "RdWrFlag": "1"},
    "S03":{                    "Cmd": "CALC:LIM:ACP:ALT1:RES?",   "CmdPar": "-",                     "RdWrFlag": "1"},
    "S04":{                    "Cmd": "CALC:MARK:FUNC:POW:RES?",  "CmdPar": "ACP",                   "RdWrFlag": "1"}

}

SA_CMD_SET_INIT_CONFIG = {
    "Reset":{                "Cmd": "*RST",                     "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetRefLevel":{          "Cmd": "DISP:TRAC:Y:RLEV",         "CmdPar": "-10dBm",                "RdWrFlag": "0"},
    "SetRefAtt":{            "Cmd": "INP:ATT",                  "CmdPar": "0dB",                   "RdWrFlag": "0"},
    "SetRBW":{               "Cmd": "BAND",                     "CmdPar": "0.03MHz",               "RdWrFlag": "0"},
    "SetVBW":{               "Cmd": "BAND:VID",                 "CmdPar": "0.3MHz",                "RdWrFlag": "0"},
    "SetTraceMode":{         "Cmd": "DISP:TRAC1:MODE",          "CmdPar": "WRIT",                  "RdWrFlag": "0"},
    "SetDetector":{          "Cmd": "DET",                      "CmdPar": "RMS",                   "RdWrFlag": "0"},
    "SetSweepTime":{         "Cmd": "SWE:TIME",                 "CmdPar": "1s",                    "RdWrFlag": "0"},
    "SetSpan":{              "Cmd": "FREQ:SPAN",                "CmdPar": "120MHz",                "RdWrFlag": "0"},
    "SetCenterFrequency":{   "Cmd": "FREQ:CENT",                "CmdPar": "1932.5MHz",             "RdWrFlag": "0"}
}

SA_CMD_SET_PRINT_SCREEN = {
    "SetDest":{              "Cmd": "HCOP:DEST",                "CmdPar": "'MMEM'",                "RdWrFlag": "0"},
    "SetFileFormat":{        "Cmd": "HCOP:DEV:LANG",            "CmdPar": "PNG",                   "RdWrFlag": "0"},
    "SetFileNameAndPath":{   "Cmd": "MMEM:NAME",                "CmdPar": "'C:\Screenshot.png'",   "RdWrFlag": "0"},
    "SetFileItem":{          "Cmd": "HCOP:ITEM:ALL",            "CmdPar": "-",                     "RdWrFlag": "0"},
    "SetFileComment":{       "Cmd": "HCOP:ITEM:WIND:TEXT",      "CmdPar": "'comments'",            "RdWrFlag": "0"},
    "StoreFile":{            "Cmd": "HCOP:IMM",                 "CmdPar": "-",                     "RdWrFlag": "0"}
}

SA_CMD_SET_ACP = {
    "S1":{                   "Cmd": "CALC:MARK:FUNC:POW:SEL",        "CmdPar": "ACP",                   "RdWrFlag": "0"},
    "S2":{                   "Cmd": "CALC:MARK:FUNC:POW:PRES",       "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "S3":{                   "Cmd": "POW:ACH:TXCH:COUN",             "CmdPar": "1",                     "RdWrFlag": "0"},
    "S4":{                   "Cmd": "POW:ACH:NAME:CHAN1",            "CmdPar": "'TxChannel'",           "RdWrFlag": "0"},
    "S5":{                   "Cmd": "POW:ACH:NAME:CHAN2",            "CmdPar": "'TxChanne2'",           "RdWrFlag": "0"},
    "S6":{                   "Cmd": "POW:ACH:NAME:CHAN3",            "CmdPar": "'TxChanne3'",           "RdWrFlag": "0"},
    "S7":{                   "Cmd": "POW:ACH:ACP",                   "CmdPar": "2",                     "RdWrFlag": "0"},
    "S8":{                   "Cmd": "POW:ACH:NAME:ACH",              "CmdPar": "'ACH'",                 "RdWrFlag": "0"},
    "S9":{                   "Cmd": "POW:ACH:NAME:ALT1",             "CmdPar": "'ALT1'",                "RdWrFlag": "0"},
    "S10":{                  "Cmd": "POW:ACH:NAME:ALT2",             "CmdPar": "'ALT2'",                "RdWrFlag": "0"},
    "S11":{                  "Cmd": "POW:ACH:BWID:CHAN1",            "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S12":{                  "Cmd": "POW:ACH:BWID:CHAN2",            "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S13":{                  "Cmd": "POW:ACH:BWID:CHAN3",            "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S14":{                  "Cmd": "POW:ACH:BWID:ACH",              "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S15":{                  "Cmd": "POW:ACH:BWID:ALT1",             "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S16":{                  "Cmd": "POW:ACH:BWID:ALT2",             "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S17":{                  "Cmd": "POW:ACH:SPAC:CHAN1",            "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S18":{                  "Cmd": "POW:ACH:SPAC:CHAN2",            "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S19":{                  "Cmd": "POW:ACH:SPAC",                  "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S20":{                  "Cmd": "POW:ACH:SPAC:ALT1",             "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S21":{                  "Cmd": "POW:ACH:SPAC:ALT2",             "CmdPar": "15MHz",                 "RdWrFlag": "0"},
    "S22":{                  "Cmd": "POW:ACH:MODE",                  "CmdPar": "REL",                   "RdWrFlag": "0"},
    "S23":{                  "Cmd": "POW:ACH:REF:TXCH:MAN",          "CmdPar": "1",                     "RdWrFlag": "0"},
    "S24":{                  "Cmd": "CALC:MARK:FUNC:POW:STAN:SAVE",  "CmdPar": "'my_aclr_standard'",    "RdWrFlag": "0"},
    "S25":{                  "Cmd": "POW:ACH:FILT:ALPH:CHAN1",       "CmdPar": "0.35",                  "RdWrFlag": "0"},
    "S26":{                  "Cmd": "POW:ACH:FILT:CHAN1",            "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S27":{                  "Cmd": "POW:ACH:FILT:ALPH:ACH",         "CmdPar": "0.35",                  "RdWrFlag": "0"},
    "S28":{                  "Cmd": "POW:ACH:FILT:ACH",              "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S29":{                  "Cmd": "POW:ACH:FILT:ALPH:ALT1",        "CmdPar": "0.35",                  "RdWrFlag": "0"},
    "S30":{                  "Cmd": "POW:ACH:FILT:ALT1",             "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S31":{                  "Cmd": "CALC:LIM:ACP:ACH",              "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S32":{                  "Cmd": "CALC:LIM:ACP:ALT1",             "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S33":{                  "Cmd": "CALC:LIM:ACP:ALT2",             "CmdPar": "55DB,55DB",             "RdWrFlag": "0"},
    "S34":{                  "Cmd": "CALC:LIM:ACP:ACH:ABS",          "CmdPar": "-25DBM,-25DBM",         "RdWrFlag": "0"},
    "S35":{                  "Cmd": "CALC:LIM:ACP:ALT1:ABS",         "CmdPar": "-30DBM,-30DBM",         "RdWrFlag": "0"},
    "S36":{                  "Cmd": "CALC:LIM:ACP:ALT2:ABS",         "CmdPar": "-35DBM,-35DBM",         "RdWrFlag": "0"},
    "S37":{                  "Cmd": "CALC:LIM:ACP",                  "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S38":{                  "Cmd": "CALC:LIM:ACP:ACH:STAT",         "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S39":{                  "Cmd": "CALC:LIM:ACP:ALT1:STAT",        "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S40":{                  "Cmd": "CALC:LIM:ACP:ALT2:STAT",        "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S41":{                  "Cmd": "CALC:LIM:ACP:ACH:ABS:STAT",     "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S42":{                  "Cmd": "CALC:LIM:ACP:ALT1:ABS:STAT",    "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S43":{                  "Cmd": "CALC:LIM:ACP:ALT2:ABS:STAT",    "CmdPar": "ON",                    "RdWrFlag": "0"}
}

SA_CMD_SET_ACP_5M = {
    "S1":{                   "Cmd": "CALC:MARK:FUNC:POW:SEL",        "CmdPar": "ACP",                   "RdWrFlag": "0"},
    "S2":{                   "Cmd": "CALC:MARK:FUNC:POW:PRES",       "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "S3":{                   "Cmd": "POW:ACH:TXCH:COUN",             "CmdPar": "1",                     "RdWrFlag": "0"},
    "S4":{                   "Cmd": "POW:ACH:ACP",                   "CmdPar": "2",                     "RdWrFlag": "0"},
    "S5":{                   "Cmd": "POW:ACH:REF:TXCH:MAN",          "CmdPar": "1",                     "RdWrFlag": "0"},
    "S6":{                   "Cmd": "POW:ACH:MODE",                  "CmdPar": "REL",                   "RdWrFlag": "0"},
    "S7":{                   "Cmd": "POW:ACH:BWID:CHAN1",            "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S8":{                   "Cmd": "POW:ACH:BWID:ACH",              "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S9":{                   "Cmd": "POW:ACH:BWID:ALT1",             "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S10":{                  "Cmd": "POW:ACH:SPAC",                  "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "S11":{                  "Cmd": "POW:ACH:SPAC:ALT1",             "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S12":{                  "Cmd": "CALC:LIM:ACP:ACH",              "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S13":{                  "Cmd": "CALC:LIM:ACP:ALT1",             "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S14":{                  "Cmd": "CALC:LIM:ACP",                  "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S15":{                  "Cmd": "CALC:LIM:ACP:ACH:STAT",         "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S16":{                  "Cmd": "CALC:LIM:ACP:ALT1:STAT",        "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S17":{                  "Cmd": "FREQ:CENT",                     "CmdPar": "1932.5MHz",             "RdWrFlag": "0"}
}

SA_CMD_SET_ACP_10M = {
    "S1":{                   "Cmd": "CALC:MARK:FUNC:POW:SEL",        "CmdPar": "ACP",                   "RdWrFlag": "0"},
    "S2":{                   "Cmd": "CALC:MARK:FUNC:POW:PRES",       "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "S3":{                   "Cmd": "POW:ACH:TXCH:COUN",             "CmdPar": "1",                     "RdWrFlag": "0"},
    "S4":{                   "Cmd": "POW:ACH:ACP",                   "CmdPar": "2",                     "RdWrFlag": "0"},
    "S5":{                   "Cmd": "POW:ACH:REF:TXCH:MAN",          "CmdPar": "1",                     "RdWrFlag": "0"},
    "S6":{                   "Cmd": "POW:ACH:MODE",                  "CmdPar": "REL",                   "RdWrFlag": "0"},
    "S7":{                   "Cmd": "POW:ACH:BWID:CHAN1",            "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S8":{                   "Cmd": "POW:ACH:BWID:ACH",              "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S9":{                   "Cmd": "POW:ACH:BWID:ALT1",             "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S10":{                  "Cmd": "POW:ACH:SPAC",                  "CmdPar": "10MHz",                 "RdWrFlag": "0"},
    "S11":{                  "Cmd": "POW:ACH:SPAC:ALT1",             "CmdPar": "20MHz",                 "RdWrFlag": "0"},
    "S12":{                  "Cmd": "CALC:LIM:ACP:ACH",              "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S13":{                  "Cmd": "CALC:LIM:ACP:ALT1",             "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S14":{                  "Cmd": "CALC:LIM:ACP",                  "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S15":{                  "Cmd": "CALC:LIM:ACP:ACH:STAT",         "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S16":{                  "Cmd": "CALC:LIM:ACP:ALT1:STAT",        "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S17":{                  "Cmd": "FREQ:CENT",                     "CmdPar": "1932.5MHz",             "RdWrFlag": "0"}
}

SA_CMD_SET_ACP_20M = {
    "S1":{                   "Cmd": "CALC:MARK:FUNC:POW:SEL",        "CmdPar": "ACP",                   "RdWrFlag": "0"},
    "S2":{                   "Cmd": "CALC:MARK:FUNC:POW:PRES",       "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "S3":{                   "Cmd": "POW:ACH:TXCH:COUN",             "CmdPar": "1",                     "RdWrFlag": "0"},
    "S4":{                   "Cmd": "POW:ACH:ACP",                   "CmdPar": "2",                     "RdWrFlag": "0"},
    "S5":{                   "Cmd": "POW:ACH:REF:TXCH:MAN",          "CmdPar": "1",                     "RdWrFlag": "0"},
    "S6":{                   "Cmd": "POW:ACH:MODE",                  "CmdPar": "REL",                   "RdWrFlag": "0"},
    "S7":{                   "Cmd": "POW:ACH:BWID:CHAN1",            "CmdPar": "20MHz",                 "RdWrFlag": "0"},
    "S8":{                   "Cmd": "POW:ACH:BWID:ACH",              "CmdPar": "20MHz",                 "RdWrFlag": "0"},
    "S9":{                   "Cmd": "POW:ACH:BWID:ALT1",             "CmdPar": "20MHz",                 "RdWrFlag": "0"},
    "S10":{                  "Cmd": "POW:ACH:SPAC",                  "CmdPar": "20MHz",                 "RdWrFlag": "0"},
    "S11":{                  "Cmd": "POW:ACH:SPAC:ALT1",             "CmdPar": "40MHz",                 "RdWrFlag": "0"},
    "S12":{                  "Cmd": "CALC:LIM:ACP:ACH",              "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S13":{                  "Cmd": "CALC:LIM:ACP:ALT1",             "CmdPar": "-45DB,-45DB",           "RdWrFlag": "0"},
    "S14":{                  "Cmd": "CALC:LIM:ACP",                  "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S15":{                  "Cmd": "CALC:LIM:ACP:ACH:STAT",         "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S16":{                  "Cmd": "CALC:LIM:ACP:ALT1:STAT",        "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S17":{                  "Cmd": "FREQ:CENT",                     "CmdPar": "1932.5MHz",             "RdWrFlag": "0"}
}

SA_CMD_SET_ACP_VEE = {
    "SetAcpMeas":{           "Cmd": "CALC:MARK:FUNC:POW:PRES",       "CmdPar": "NONE",                  "RdWrFlag": "0"},
    "SetAcpSpace":{          "Cmd": "POW:ACH:SPAC",                  "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpBwid":{           "Cmd": "POW:ACH:BWID",                  "CmdPar": "5MHz",                  "RdWrFlag": "0"},
    "SetAcpBwidAch":{        "Cmd": "POW:ACH:BWID:ACH",              "CmdPar": "5MHZ",                  "RdWrFlag": "0"},
    "SetAcpMode":{           "Cmd": "POW:ACH:MODE",                  "CmdPar": "REL",                   "RdWrFlag": "0"},
    "SetAcpAch":{            "Cmd": "POW:ACH:ACP",                   "CmdPar": "2",                     "RdWrFlag": "0"},
    "SetSpan":{              "Cmd": "FREQ:SPAN",                     "CmdPar": "70MHz",                 "RdWrFlag": "0"}
}

SA_CMD_SET_LTE_EVM_FDD_5M_TM3P1 = {
    "S1":{                   "Cmd": "*RST",                          "CmdPar": "-",                     "RdWrFlag": "0"},
    "S2":{                   "Cmd": "INST",                          "CmdPar": "LTE",                   "RdWrFlag": "0"},
    "S3":{                   "Cmd": "FREQ:CENT",                     "CmdPar": "1932.5MHz",             "RdWrFlag": "0"},
    "S4":{                   "Cmd": "CONF:LDIR",                     "CmdPar": "DL",                    "RdWrFlag": "0"},
    "S5":{                   "Cmd": "CONF:DUPL",                     "CmdPar": "FDD",                   "RdWrFlag": "0"},
    "S6":{                   "Cmd": "MMEM:LOAD:TMOD:DL",             "CmdPar": "'E-TM3_1__5MHz'",       "RdWrFlag": "0"},
    "S7":{                   "Cmd": "CONF:DL:BW",                    "CmdPar": "BW5_00",                "RdWrFlag": "0"},
    "S8":{                   "Cmd": "CONF:DL:CYCP",                  "CmdPar": "NORM",                  "RdWrFlag": "0"},
    "S9":{                   "Cmd": "CONF:DL:PLC:CID",               "CmdPar": "AUTO",                  "RdWrFlag": "0"},
    "S10":{                  "Cmd": "CONF:DL:PLCI:PLID?",            "CmdPar": "1",                     "RdWrFlag": "0"},
    "S11":{                  "Cmd": "DL:DEM:MCF",                    "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S12":{                  "Cmd": "DL:DEM:MCF?",                   "CmdPar": "1",                     "RdWrFlag": "0"},
    "S13":{                  "Cmd": "FETC:SUMM:EVM:DSQP?",           "CmdPar": "1",                     "RdWrFlag": "0"},
    "S14":{                  "Cmd": "FETC:SUMM:EVM:DSST?",           "CmdPar": "1",                     "RdWrFlag": "0"},
    "S15":{                  "Cmd": "FETC:SUMM:EVM:DSSF?",           "CmdPar": "1",                     "RdWrFlag": "0"},
    "S16":{                  "Cmd": "DL:DEM:AUTO",                   "CmdPar": "ON",                    "RdWrFlag": "0"},
    "S17":{                  "Cmd": "DL:FORM:PSCD",                  "CmdPar": "PHYDET",                "RdWrFlag": "0"},
    "S18":{                  "Cmd": "SUBFrame:SELect",               "CmdPar": "ALL",                   "RdWrFlag": "0"}
}
for item in SaCmdSet.keys():
     #str = ""
     str = SaCmdSet[item].values()
     print(str)
