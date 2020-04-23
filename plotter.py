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

with open(sys.argv[1], 'w', newline='') as file:
    writer = csv.writer(file)
    for a in range(len(t)):
        writer.writerow([t[a],x[a],y[a],z[a],i[a]])

print("Complete")



# plt.plot(t,x, label='X axis')
# plt.plot(t,y, label='Y axis')
# plt.plot(t,z, label='Z axis')

# plt.xlabel('Time')
# plt.ylabel('Axis')
# plt.title('Axis/Time Graph')
# plt.legend()
# plt.show()
# plt.savefig('x.png')

