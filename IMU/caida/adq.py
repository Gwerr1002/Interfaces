# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:05:55 2022

@author:gerard
"""

from numpy import load, save, quantile

"Frecuencia de muestreo 31Hz"


class Adq_save():
    def __init__(self):
        self.dev = {'ax':[], 'ay':[], 'az':[], 'gx':[], 'gy':[], 'gz':[]}
        self.fs = 31
        
        self.par_inf = {'ax': -1.0475, 'ay': -0.377, 'az': -0.3005, 'gx': -43.6530, 'gy': -22.846, 'gz': -21.776}
        self.par_sup = {'ax': -0.8115, 'ay': 0.279, 'az': 0.3675, 'gx': 59.523, 'gy': 24.602, 'gz': 22.7155}
        self.count_n = 0
    
    def s_device(self):
        self.dev['fs'] = self.fs
        save("adq_dev1.npy", self.dev)
    
    def decode(self, data):
        data = data.decode()
        data = data.split(',')[:-1]
        self.count_n += len(data)
        data = [i.split() for i in data]
        #
        for arreglo in data:
            for num,key in zip(arreglo,self.dev.keys()):
                self.dev[key].append(float(num))
        #
        if self.count_n == self.fs:
            self.count_n = 0
            self.caida()
                
    def caida(self):
        window = {key : self.dev[key][:-self.fs] for key in self.dev}
        q2 = {key : quantile(window[key],.5) for key in window}
        
    
#bytearray(b'0.1044922 1.002441 0.06005859 4.198473 0.9923664 -0.1374046,0.1018066 0.984375 0.05981445 4.816794 0.870229 -0.389313,0.1018066 0.9978027 0.06640625 5.862596 0.3206107 -0.2290076,')
