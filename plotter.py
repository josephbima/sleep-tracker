import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv
import sys

t = []
x = []
y = []
z = []
i = []


# with open(sys.argv[1],'r') as csvfile:
with open(sys.argv[1],'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        t.append(row[0])
        x.append(float(row[1]))
        y.append(float(row[2]))
        z.append(float(row[3]))
        i.append(row[4])
        # print(row)


print(t[0])
print(x[0])
print(y[0])
print(z[0])
print(i[0])

# with open('brand-new-merged-activity.csv','w') as file:
#     print("Creating new file")
#     writer = csv.writer(file)
#     for el in range(len(t)):
#         writing = [t[el],x[el],y[el],z[el],i[el]]
#         print('Writing', writing)
#         writer.writerow(writing)


plt.plot(t,x, label='X axis')
plt.plot(t,y, label='Y axis')
plt.plot(t,z, label='Z axis')

plt.xlabel('Time')
plt.ylabel('Axis')
plt.title('Axis/Time Graph')
plt.legend()
plt.show()
plt.savefig('x.png')

