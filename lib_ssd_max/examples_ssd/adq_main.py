import matplotlib.pyplot as plt

with open("adq1.txt",'r') as file:
    d1,d2=[],[]
    for line in file:

        line=line.replace(" , "," ").split()
        print(line)
        d1.append(line[0])
        d2.append(line[1])
        d1 = [int(a) for a in d1]
        d2 = [int(a) for a in d2]

plt.plot(d1)
plt.plot(d2)
plt.show()
