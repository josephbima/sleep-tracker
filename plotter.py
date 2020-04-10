import matplotlib.pyplot as plt
import csv

t = []
x = []
y = []
z = []

with open('/Users/johanthomassajan/Downloads/sleep-tracker-328/Sleeping Log + Data/Johan/sleep-johan-1-data.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        t.append(row[0])
        x.append((row[1]))
        y.append(row[2])
        z.append(row[3])
        print(row)
        

plt.plot(t,x, label='X axis')
plt.plot(t,y, label='Y axis')
plt.plot(t,z, label='Z axis')

plt.xlabel('Time')
plt.ylabel('Axis')
plt.title('Axis/Time Graph')
plt.legend()
plt.show()