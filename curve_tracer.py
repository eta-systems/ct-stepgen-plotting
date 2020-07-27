# -*- coding: utf-8 -*-
"""
@author: simon

Copyright (c) 2020 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

from time import sleep
from sys import stderr
import serial

class curvetracer:
    def __init__(self, com='COM1', baudrate=19200, timeout=1, log_level=0):
        self.com = com
        self.baudrate = baudrate
        self.timeout = timeout
        self.log_level = int(log_level)  # 0=off, 1=log
        self.instr = serial.Serial(self.com, self.baudrate, timeout=self.timeout)
        self.instr.timeout = self.timeout
        
        self.instr.write(b'\r\n')  # just send an empty line
        
#        message = 'ETA-SYSTEMS,STEP-GENERATOR,0,2020-08'
        message = self.request('*IDN?')
        if('ETA-SYSTEMS' in str(message)):
            print(str(message))
        else:
            self.instr.close()
            print(str(message))
            raise RuntimeError('Curve Tracer not connected')
    
    def write(self, message):
        if(self.log_level>0):
            print('[w] ' + str(message))
        self.instr.write(bytes(message + '\r\n', 'utf-8'))
    
    def read(self, address):
        if(self.log_level>0):
            print('[r] ', end = ' ') # end -> no \n
        val = self.instr.read_until()
        if(self.log_level>0):
            print(val, end='')
        return val.decode('utf-8')  # convert bytestring to utf-8
    
    def request(self, message):
        if(self.log_level>0):
            print('[q] ' + str(message), end='')
        self.instr.write(bytes(message + str('\r\n'), 'utf-8')) 
        val = self.instr.read_until()
        print(val.decode('utf-8'), end='')
        return val.decode('utf-8')  # convert bytestring to utf-8
        
    def close(self):
        self.instr.close()
