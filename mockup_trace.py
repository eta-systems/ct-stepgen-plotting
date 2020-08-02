# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:56:36 2020

@author: simon
"""

import numpy as np
import matplotlib.pyplot as plt


VOLTS_MIN = -1.4
VOLTS_MAX = 5.0
N_POINTS = 100
IS = 0.001
nVt = 0.3

val = {}
val['source'] = {}
val['source']['voltage'] = np.linspace(VOLTS_MIN, VOLTS_MAX, N_POINTS)
val['source']['current'] = np.zeros(N_POINTS)

for k in range(N_POINTS):
    VD = val['source']['voltage'][k]
    I = IS * float(np.exp((VD-4) / nVt))
    I =  I - IS* float(np.exp((-VD-0.3)/(nVt*0.7)))
    I = I + np.random.rand()*0.0005
    val['source']['current'][k] = I


# use r'$3.4 \Omega$' for Latex Math mode
plt.figure(figsize=(8,8))
plt.plot(val['source']['voltage'][10:], val['source']['current'][10:])
plt.xlabel(r'voltage [V]')
plt.ylabel(r'current [A]')
plt.title(r'current-voltage curve of a $4.7$V Zener Diode')
plt.grid()

