# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 10:26:58 2020

@author: simon
"""


import time

time_ms = lambda: int(round(time.time() * 1000))
tim = time_ms()

def tic():
    global tim
    tim = time_ms()
    
def toc():
    global tim
    elapsed = time_ms() - tim
    print('Elapsed time: ' + str(elapsed) + ' ms')
    tim = time_ms()







