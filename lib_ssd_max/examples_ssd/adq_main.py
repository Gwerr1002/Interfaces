import matplotlib.pyplot as plt
import numpy as np

with open("adq2.txt",'r') as file:
    d1,d2=[],[]
    for line in file:

        line=line.replace(" , "," ").split()
        #print(line)
        d1.append(line[0])
        #d2.append(line[1])
        d1 = [int(a) for a in d1]
        d2 = [int(a) for a in d2]

d1_1 = -53*(np.array(d1)-17000)/2000+20
d1_1_1 = -53*(np.array(d1)-17000)/2000+40
d2_2 = 53*(np.array(d2)-17000)/2000+40

def graf(*args):
    plt.figure()
    for arg in args:
        plt.plot(arg)
    plt.show()
info = ""
for i in d1_1.astype(int)[::20]:
    info+=f"{i},"
print(info)
#graf(d1_1.astype(int))
#graf(d1_1)
#graf(d1)
i = 10
t = np.linspace(0,len(d1_1)/27,len(d1_1))
plt.figure()
plt.plot(t,d1_1)
plt.show()
