import read_TS as ts
import pandas as pd
import numpy as np
from plotly import express as px
import matplotlib.pyplot as plt

def plot_3d(data, filename, electrode_type = [3, 4, 5, 6, 7, 8]):
    plot_atoms = data.loc[data['Type'].isin(electrode_type)]
    fig = px.scatter_3d(plot_atoms, x='X', y='Y', z='Z', color='Q')
    print(filename)
    fig.show()
    #fig.write_image('{}_Q.png'.format(filename))
    
def sum_charge(data, water_id, cat_id, an_id):
    water_atoms = data.loc[data['Type'].isin(water_id)]
    cat_atoms = data.loc[data['Type'].isin(cat_id)]
    an_atoms = data.loc[data['Type'].isin(an_id)]
    water_q = water_atoms['Q'].sum()
    cat_q = cat_atoms['Q'].sum()
    an_q = an_atoms['Q'].sum()
    return water_q, cat_q, an_q



def calc_charge(data, cell):
    # define plot
    Z = cell[2]
    resolution = 500
    dz = Z/resolution
    height = np.linspace(0.0, Z, resolution)

    # iterate over timestep and calcuate total charge in each dz layer
    charge = np.zeros(resolution)
    for index, row in data.iterrows():
        q = row['Q']
        h = row['Z']
        layer_index = int(h/dz)
        charge[layer_index] += q
    
    return height, charge

def find_solvent_region(timestep, cat_id, anode_id):
    cat_atoms = timestep[timestep['Type'] == cat_id]
    z_max = cat_atoms['Z'].min()

    anode_atoms = timestep[timestep['Type'] == anode_id]
    z_min = anode_atoms['Z'].max()
    return z_max, z_min
#######################################
### 3d plot
# path = '/Users/steve/doe-project/recomb/pt_production/{}/chg.1800000.lmp'
# folders = ['pt_coupled_0v', 'pt_coupled_20v', 'pt_seperate_1v', 'pt_seperate_5v', 'pt_seperate_20v']
# for job in folders:
#     time, data, cell = ts.read_TS(path.format(job), True)
#     plot_3d(data, job)

### Plot z-charge evolution
path = '/Users/steve/doe-project/recomb/pt_production/{}/chg.{}.lmp'
folders = ['pt_coupled_0v', 'pt_coupled_1v', 'pt_coupled_5v', 'pt_coupled_20v', 'pt_seperate_1v', 'pt_seperate_5v', 'pt_seperate_20v']
inputs = np.arange(0,1800000, 10000)

water = [1, 2]
cathode = [4,6,7]
anode = [3,5,8]

for job in folders:
    x = []
    w = []
    c = []
    a = []
    for step in inputs:
        time, data, cell = ts.read_TS(path.format(job, str(step)), True)
        sim_time = time * 0.00025 # timestep to ps
        x.append(sim_time)
        wa,ca,an = sum_charge(data, water, cathode, anode)
        w.append(wa)
        c.append(ca)
        a.append(an)
    fig, axs = plt.subplots()    
    axs.plot(x, w, label='water')
    axs.plot(x, c, label='cathode')
    axs.plot(x, a, label='anode')
    axs.legend()
    axs.set_xlabel('Simulation Time [ps]')
    axs.set_ylabel('Charge')
    axs.set_title('Charge Accumulation')
    plt.savefig('{}_qSum.png'.format(job))

# folders = ['pt_coupled_0v', 'pt_coupled_1v', 'pt_coupled_5v', 'pt_coupled_20v', 'pt_seperate_1v', 'pt_seperate_5v', 'pt_seperate_20v']
# inputs = ['0', '10000', '500000', '1000000', '1500000', '1800000' ]
# for job in folders:
#     fig, axs = plt.subplots(len(inputs), 1, figsize=(10,6))
#     plt_i = 0
#     for step in inputs:
#         time, data, cell = ts.read_TS(path.format(job, step), True)
#         sim_time = time * 0.00025 # timestep to ps
#         #print(data)
#         cat_max, cat_min = find_solvent_region(data, 4, 7)
#         an_max, an_min = find_solvent_region(data, 8, 5)
#         axs[plt_i].axvline(x = cat_max, color = 'r')
#         axs[plt_i].axvline(x = cat_min, color = 'r')
#         axs[plt_i].axvline(x = an_max, color = 'k')
#         axs[plt_i].axvline(x = an_min, color = 'k')
#         x, y = calc_charge(data, cell)
#         axs[plt_i].plot(x, y, label =time)
#         axs[plt_i].set_title('Charge at '+ str(sim_time) + ' [ps]')
#         axs[plt_i].set_xlim(0, x.max())
#         axs[plt_i].set_ylim(-30, 30)
#         plt_i +=1
#     axs[len(inputs)-1].set_xlabel('z height [angstrom]')
#     plt.subplots_adjust(top = 0.9, bottom=0.1, hspace=1.5, wspace=0.4)
#     #plt.show()
#     plt.savefig('{}_qEvo.png'.format(job))