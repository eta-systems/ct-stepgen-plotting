# -*- coding: utf-8 -*-
"""
@author:   simon burkhardt
@copyright (c) 2020 eta systems GmbH. All rights reserved.
@date      2020-07-27
@brief     Example to trace and plot a simple resistor curve with 100 data points

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

import time
from sys import stderr
import serial

from curve_tracer import curvetracer

import numpy as np
import matplotlib.pyplot as plt

#%%

# PARAMETERS
com = 'COM3'
baudrate = '115200'

VOLTS_MIN = 0.0
VOLTS_MAX = 5.0
CURR_MIN = -0.01
CURR_MAX = 0.006

N_POINTS  = 100
VOLTS_SWEEP = VOLTS_MAX - VOLTS_MIN
T_SETTLE = 0.050

val = {}
val['source'] = {}
val['source']['voltage'] = np.zeros(N_POINTS)
val['source']['current'] = np.zeros(N_POINTS)

#%%
tracer = curvetracer(com, baudrate, log_level=1)
tracer.write(':SOUR:CURR:LIM ' + str(CURR_MAX))
tracer.write(':SOUR:VOLT:LEV ' + str(VOLTS_MIN))
tracer.write(':CURR:RANG ' + str(0.005))

#%%
for k in range(0, N_POINTS):
    vset = round(VOLTS_MIN + (VOLTS_SWEEP / N_POINTS * k), 3)
    tracer.write(':SOUR:VOLT ' + str(vset))
    time.sleep(T_SETTLE)
    vread = float(tracer.request(':MEAS:VOLT?'))
    time.sleep(T_SETTLE)
    iread = float(tracer.request(':MEAS:CURR?'))
    val['source']['voltage'][k] = vread
    val['source']['current'][k] = iread
    
tracer.write(':SOUR:VOLT:LEV ' + str(VOLTS_MIN))
tracer.close()

#%%
# use r'$3.4 \Omega$' for Latex Math mode
plt.figure(figsize=(8,5))
plt.plot(val['source']['voltage'], val['source']['current'])
plt.xlabel(r'voltage [V]')
plt.ylabel(r'current [A]')
plt.title(r'current-voltage curve of a 1$k\Omega$ resistor')
plt.grid()

#%% close COM Port if exeption occurrs
tracer.close()



