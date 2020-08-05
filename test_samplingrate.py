# -*- coding: utf-8 -*-
"""
@author:   simon burkhardt
@copyright (c) 2020 eta systems GmbH. All rights reserved.
@date      2020-08-05
@brief     Example to trace and plot a simple resistor curve with 100 data points

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""


#%%

import time
from sys import stderr
import serial

from curve_tracer import curvetracer
import le_tictoc as tt

import numpy as np
import matplotlib.pyplot as plt

#%%

# PARAMETERS
com = 'COM3'
baudrate = '115200'

VOLTS_MIN = -5.0
VOLTS_MAX =  5.0
CURR_MIN = -0.05
CURR_MAX =  0.05

N_POINTS  = 100
N_OVERSAMPLE = 1
VOLTS_SWEEP = VOLTS_MAX - VOLTS_MIN
T_SETTLE = 0.0015
T_DELAY = 0.000

val = {}
val['source'] = {}
val['source']['voltage'] = np.zeros(N_POINTS)
val['source']['current'] = np.zeros(N_POINTS)

#%%
tracer = curvetracer(com, baudrate, log_level=1)
tracer.write('*RST')
time.sleep(1.5)
tracer.close()

tracer = curvetracer(com, baudrate, log_level=0)
tracer.write(':SOUR:CURR:LIM ' + str(CURR_MAX))     # OCP
time.sleep(T_SETTLE)
tracer.write(':SOUR:VOLT:LIM ' + str(22.0))         # OVP
time.sleep(T_SETTLE)
tracer.write(':SOUR:VOLT:LEV ' + str(0.0))          # init 0V
time.sleep(T_SETTLE)
tracer.write(':CURR:RANG ' + str(0.005))            # 5mA Range

#%%
tt.tic()
for k in range(0, N_POINTS):
    vset = round(VOLTS_MIN + (VOLTS_SWEEP / N_POINTS * k), 3)  # round to mV
    tracer.write(':SOUR:VOLT ' + str(vset))
    time.sleep(T_SETTLE)
    vread = 0.0
    iread = 0.0
    
    for i in range(N_OVERSAMPLE):
        vread += float(tracer.request(':MEAS:VOLT?'))
        #time.sleep(T_DELAY)
        iread += float(tracer.request(':MEAS:CURR?'))
        #time.sleep(T_DELAY)
    vread /= float(N_OVERSAMPLE)
    iread /= float(N_OVERSAMPLE) / 1000.0 # mA
    val['source']['voltage'][k] = vread
    val['source']['current'][k] = iread
    
tracer.write(':SOUR:VOLT:LEV ' + str(0.0))
tracer.close()
tt.toc()

#%%
# https://www.pythoninformer.com/python-libraries/matplotlib/line-plots/
# use r'$3.4 \Omega$' for Latex Math mode
plt.figure(figsize=(5,5))
#plt.plot(val['source']['voltage'][5:], val['source']['current'][5:], linewidth=2, marker='X')
plt.plot(val['source']['voltage'][5:], val['source']['current'][5:], linewidth=4)
plt.xlabel(r'$V_f$ [V]')
plt.ylabel(r'$I_f$ [mA]')
plt.title(r'current-voltage curve of a 1N4007 Diode')
plt.grid()

plt.savefig('1N4007_curve.pdf')

#%% close COM Port if exeption occurrs
tracer.close()


#%% Print for Excel

for k in range(len(val['source']['voltage'])):
    print(str(val['source']['voltage'][k]) + '\t' + str(val['source']['current'][k]))



