import numpy as np
import matplotlib.pyplot as plt

data1=np.load("adq1.npy", allow_pickle=True).item()
data2=np.load("adq2.npy", allow_pickle=True).item()
data3=np.load("adq3.npy", allow_pickle=True).item()
data4=np.load("adq4.npy", allow_pickle=True).item()
caida1=np.load("caida1.npy", allow_pickle=True).item()
caida2=np.load("caida2.npy", allow_pickle=True).item()

d = {key : data1[key]+data2[key]+data3[key] + data4[key] for key in list(data1.keys())[:-1]}

q1 = {key : np.quantile(d[key],.25) for key in d}
q2 = {key : np.quantile(d[key],.5) for key in d}
q3 = {key : np.quantile(d[key],.75) for key in d}
RIC = {key : q3[key]-q1[key] for key in d}

inf = {key : q1[key] -1.5*RIC[key] for key in d}
sup = {key : q3[key] + 1.5*RIC[key] for key in d}
print("inferioir:",inf)
print("mediana:",q2)
print("superior:",sup)

D = [d[key] for key in d]

#plt.boxplot(D)
plt.figure()
plt.boxplot(caida2['az'][434:466])