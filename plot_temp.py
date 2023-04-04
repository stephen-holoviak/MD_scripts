import matplotlib.pyplot as plt

f = open('/Users/steve/doe-project/recomb/pt_production/pt_coupled_5v/lmp.log', 'r')

data = [['Time Step'], ['totE [eV]'], ['KE [eV]'], ['Temp [K]'], ['PE [eV]']]
num_data_lines = 5
data_line = 0
step = 0
totE = -1.0
ke = -1.0
pe = -1.0
temp = -1.0

for line in f.readlines():
    if 'Step' in line:
        #print(line)
        step = int(line.split()[2])
        data_line = 0

    elif step > 1 and data_line == 0 : #and step < 121000
        data[0].append(step)
        totE = float(line.split()[2])
        data[1].append(totE)

        ke = float(line.split()[5])
        data[2].append(ke)

        temp = float(line.split()[8])
        data[3].append(temp)
        data_line += 1

    elif step > 1 and data_line == 1: # and step < 121000
        pe = float(line.split()[2])
        data[4].append(pe)
        data_line += 1

fig, ax1 = plt.subplots()
l1, = ax1.plot(data[0][1:], data[1][1:], 'b', label = 'total E')
l2, = ax1.plot(data[0][1:], data[4][1:], 'g', label = 'PE')
ax2 = ax1.twinx()
ax2.set_ylim(200,450)
l3, = ax2.plot(data[0][1:], data[2][1:], 'r', label = 'KE')
plt.legend(handles=[l1,l2,l3])
plt.xlabel('Time Step [fs]')
plt.ylabel('Energy [eV]')
plt.show()

fig, ax1 = plt.subplots()
ax1.plot(data[0][1:], data[3][1:])
plt.xlabel('Time Step [fs]')
plt.ylabel('Temperature [K]')
ax1.set_ylim(260, 325)
plt.show()

eq = data[1]
print(len(eq))