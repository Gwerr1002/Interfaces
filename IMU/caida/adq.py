# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:05:55 2022

@author:gerard
"""

from numpy import load, save

"Frecuencia de muestreo 31Hz"


class Adq_save():
    def __init__(self):
        self.dev = {'ax':[], 'ay':[], 'az':[], 'gx':[], 'gy':[], 'gz':[]}
        self.fs = 31
    
    def s_device(self):
        self.dev['fs'] = 24
        save("adq_dev1.npy", self.dev)
    
    def decode(self, data):
        data = data.decode()
        data = data.split(',')[:-1]
        data = [i.split() for i in data]
        for arreglo in data:
            for num,key in zip(arreglo,self.dev.keys()):
                self.dev[key].append(float(num))
                    
