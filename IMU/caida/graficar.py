# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 01:01:43 2023

@author: gerard
"""

import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt

#%%
data = np.load("caida1.npy",allow_pickle=True)
d = data.item()
t = np.linspace(0,len(d['ay'])/24,len(d['ay']))

fig,ax=plt.subplots(6,1)

for i,key in zip(range(6),d.keys()):
    ax[i].plot(t,d[key],label=key)
    
plt.legend()