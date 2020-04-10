import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('sleep-joseph-data.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[0]))
        y.append(row[1])


plt.plot(x,y, label='Loaded from file!')
plt.xlabel('Time')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()