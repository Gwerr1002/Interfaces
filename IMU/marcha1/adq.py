# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 12:05:55 2022

@author:gerard
"""

from numpy import array, load, save, linspace
from time import time,sleep
from matplotlib.pyplot import figure, subplots, ylim, xlim, show

"Frecuencia de muestreo 31Hz"

''' Filtro para gx y gy caminar normal, desfase 0.58 segundos'''
IIR1 = [([0.049241670369405736, 0.09848334073881147, 0.049241670369405736], [4.231503273101177, -7.901516659261189, 3.866980067637634]),
([0.020193328227308436, 0.04038665645461687, 0.020193328227308436], [4.460211761442208, -7.959613343545383, 3.580174895012408])
]
''' Filtro para gx y gy correr'''
IIR2 = [([0.0832184229242957, 0.1664368458485914, 0.0832184229242957], [4.320158506475599, -7.833563154151409, 3.8462783393729927]),
([0.03412672470415125, 0.0682534494083025, 0.03412672470415125], [4.606150687883521, -7.931746550591697, 3.4621027615247817])
]
'''Filtro para ay desfase 0.1735'''
IIR2_6 = [([0.2322906428895593, 0.4645812857791186, 0.2322906428895593], [4.892741896576417, -7.5354187142208815, 3.571839389202702]),
([0.3302256268434288, 0.3302256268434288], [2.3302256268434287, -1.6697743731565713])
]
''' Filtro para ay desfase 0.1 segundos'''
IIR5 = [([1.2310417592351435, 2.462083518470287, 1.2310417592351435], [6.142349772894001, -5.537916481529713, 4.319733745576286]),
([0.5048332056827107, 1.0096664113654215, 0.5048332056827107], [6.70492537175721, -6.990333588634579, 2.304741039608211])
]

IIR8 = [([5.463843325435465, 10.92768665087093, 5.463843325435465], [11.605447720526197, 2.92768665087093, 7.322238930344733]),
([2.5590091112257354, 5.118018222451471, 2.5590091112257354], [11.72929948709161, -2.8819817775485292, 1.3887187353598613])
]

class Adq_save():
    def __init__(self):
        self.dev1 = {'ax':[], 'ay':[], 'az':[], 'gx':[], 'gy':[], 'gz':[]}
        self.dev2 = {'ax':[], 'ay':[], 'az':[], 'gx':[], 'gy':[], 'gz':[]}
        self.fs = 31
    
    def s_device1(self):
        self.dev1['fs'] = 31
        save("adq_dev1.npy", self.dev1)
    
    def s_device2(self):
        self.dev2['fs'] = 31
        save("adq_dev2.npy", self.dev2)
    
    def decode(self, data, dev):
        data = data.decode()
        data = data.split(',')[:-1]
        data = [i.split() for i in data]
        for arreglo in data:
            for num,key in zip(arreglo,self.dev1.keys()):
                if dev == "08:3A:F2:B7:6C:22":
                    self.dev1[key].append(float(num))
                elif dev == "C8:F0:9E:9E:72:DA":
                    self.dev2[key].append(float(num))
                else:
                    print(dev)
                    
class graf():
    def __init__(self):
        self.fig, self.ax = subplots(2,1, figsize=(13, 6), layout='constrained')
        self.h1, = self.ax[0].plot([],[])
        self.ax[0].set_title("Pierna izquierda (1 gy)")
        self.ax[0].set_xlim(0,10)
        self.ax[0].set_ylim(-2,2) #para los giros va de -300 a 300 para acel de -2 a 2
        self.h2, = self.ax[1].plot([],[])
        self.ax[1].set_title("Pierna derecha (2 gy)")
        self.ax[1].set_xlim(0,10)
        self.ax[1].set_ylim(-2,2)
        #
        self.N = 310 #5 segundos
        self.fs = 31
        self.desfase = 0
    
    def set_desfase(self,desfase):
        print("Desfase")
        self.desfase = desfase
        
    def update_graf(self,d1,d2):
        
        if len(d1) > self.N:
            tf1 = len(d1)/self.fs
            d1 = d1[-self.N:]
            t1 = linspace(tf1-5,tf1,len(d1))
            self.ax[0].set_xlim(tf1-5,tf1)
        else:
            t1 = linspace(0,len(d1)/self.fs,len(d1))
        
        if len(d2) > self.N:
            tf2 = len(d2)/self.fs+self.desfase
            d2 = d2[-self.N:]
            t2 = linspace(tf2-5,tf2,len(d2))
            self.ax[1].set_xlim(tf1-5,tf1)
        else:
            t2 = linspace(self.desfase,len(d2)/self.fs+self.desfase,len(d2))
        self.h1.set_data(t1,d1)
        self.h2.set_data(t2,d2)
        

#14
"08:3A:F2:B7:6C:22: bytearray(b'0.1044922 1.002441 0.06005859 4.198473 0.9923664 -0.1374046,0.1018066 0.984375 0.05981445 4.816794 0.870229 -0.389313,0.1018066 0.9978027 0.06640625 5.862596 0.3206107 -0.2290076,')"
"https://www.lawebdelprogramador.com/foros/Python/1548513-Derivadas-numericas.html"
"https://pythondiario.com/2018/08/graficos-en-tercera-dimension-3d-con.html"