import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, math
import read_timeStep as steve

folder = 'coupled_1.0/'
dir = '/Users/steve/doe-project/reductive_reconstruction/oxide_tests/structures/pt/' + folder

time = []
b_Q =[]
t_Q = []
s_Q=[]

# read the data from the output files
for x in os.walk(dir):
    for f in x[2]:
        ts = -1
        fullRun = pd.DataFrame()
        if f.startswith('chg.'):
            ts, fullRun = steve.read_TS(dir + f)
            #print(fullRun.head())
            b_total, b_avg, b_min, b_max, b_num = steve.seperate_layer(data=fullRun, types =[1,2,3,6], zmin =0.0, zmax=28.0)
            t_total, t_avg, t_min, t_max, t_num = steve.seperate_layer(data=fullRun, types =[1,2,3,6], zmin =99.0, zmax=120.0)
            s_total, s_avg, s_min, s_max, s_num = steve.seperate_layer(data=fullRun, types =[4,5], zmin =0.0, zmax=120.0)
            # print('For timestep: ' + str(ts))
            # print('The total charge of this layer is: ' + str(total))
            # print('The average charge of this layer is: ' + str(avg))
            # print('There are ' + str(num) + ' atoms in the layer')
            # print('The minimum charge is ' + str(min) + ' , and the max charge is ' + str(max))
            time.append(ts)
            b_Q.append(b_avg)
            t_Q.append(t_avg)
            s_Q.append(s_avg)


# plot the data
b_mean = np.mean(b_Q)
b_std = np.std(b_Q)
print('b mean: ' + str(b_mean))
print('b std: ' + str(b_std))
plt.scatter(time, b_Q)
plt.title('Annode Charge Evolution')
plt.xlabel('Timestep')
plt.ylabel('Avgerage atomic charge in layer [e]')
plt.show()

t_mean = np.mean(t_Q)
t_std = np.std(t_Q)
print('t mean: ' + str(t_mean))
print('t std: ' + str(t_std))
plt.scatter(time, t_Q)
plt.title('Cathode Charge Evolution')
plt.xlabel('Timestep')
plt.ylabel('Total charge in layer [e]')
plt.show()

s_mean = np.mean(s_Q)
s_std = np.std(s_Q)
print('s mean: ' + str(s_mean))
print('s std: ' + str(s_std))
plt.scatter(time, s_Q)
plt.title('Solvent Charge Evolution')
plt.xlabel('Timestep')
plt.ylabel('Total charge in layer [e]')
plt.show()