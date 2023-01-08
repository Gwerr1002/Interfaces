# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 01:19:48 2023

@author: luci
"""
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt

data1 = load("adq_dev1.npy",allow_pickle=True)
data2 = load("adq_dev2.npy",allow_pickle=True)
d1 = data1.item()
t1 = np.linspace(0,len(d1['ay'])/31,len(d1['ay']))
d2=data2.item()
t2 = np.linspace(0,len(d2['ay'])*0.04,len(d2['ay']))+8.35

fig,ax=plt.subplots(6,2)

for i,key in zip(range(6),d2.keys()):
    PSD = sp.welch(d2[key],31)
    ax[i][0].plot(t2,d2[key])
    ax[i][1].plot(PSD[0],PSD[1])
    
for i,key in zip(range(6),d2.keys()):
    d = d2[key]
    for f in IIR8:
        d = sp.lfilter(f[0],f[1],d)
    PSD = sp.welch(d,31)
    ax[i][0].plot(t2,d)
    ax[i][1].plot(PSD[0],PSD[1])