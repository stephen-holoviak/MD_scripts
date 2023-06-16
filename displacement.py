# Plot the displacement of the cathode and anode working atoms:
import math, os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def read_TS(file): # read in the data file for a given timestep and store it as a list of dictionaries, each dict represents an atom
    input = open(file, 'r')
    raw_data = input.readlines()
    input.close()

    timestep = int(raw_data[1])
   
    run_data = []
    for line in raw_data[9:]:
                ld = line.split()
                ts_data = dict.fromkeys(['ID', 'Type', 'X', 'Y', 'Z', 'Q'])
                #print(ld)
                ts_data['ID'] = int(ld[0])
                ts_data['Type'] = int(ld[1])
                ts_data['X'] = float(ld[2])
                ts_data['Y'] = float(ld[3])
                ts_data['Z'] = float(ld[4])
                ts_data['Q'] = float(ld[5])
                run_data.append(ts_data)
    run_data = sorted(run_data, key=lambda x: x['ID']) # sort by atom ID tag

    cell_x = float(raw_data[5].split()[0]) + float(raw_data[5].split()[1]) # casts from string in scientific notation to float and sums lammps xmin & xmax
    cell_y = float(raw_data[6].split()[0]) + float(raw_data[6].split()[1])
    cell_z = float(raw_data[7].split()[0]) + float(raw_data[7].split()[1])
    cell = [cell_x, cell_y, cell_z]
    return timestep, run_data, cell

def pbc_distance(a, b, cell):# Calculate the distance between atom a(list with [x,y,z]) and atom b in a periodic cell with dimensions cell=[x,y,z]
    A = cell[0]
    B = cell[1]
    C = cell[2]

    dx = abs(a[0] - b[0])
    x = min(dx, abs(A - dx))
     
    dy = abs(a[1] - b[1])
    y = min(dy, abs(B - dy))
     
    dz = abs(a[2] - b[2])
    z = min(dz, abs(C - dz))
 
    return math.sqrt(x**2 + y**2 + z**2)

def msd(type, path, t1, t0): # return the root mean squared deviation of atoms of type given two timesteps
    time1, data1, cell1 = read_TS(f'{path}/chg.{t1}.lmp')
    data1 = [atom for atom in data1 if atom['Type'] == type] # only save atoms of the desired type for t1

    time0, data0, cell0 = read_TS(f'{path}/chg.{t0}.lmp') 
    data0 = [atom for atom in data0 if atom['Type'] == type]
    
    # iterate over every atom in data0 by index so we can access the same atom in data1
    msd = 0
    for i in range(0, len(data0)):
        #print(f"{data0[i]}, {data1[i]}")
        r1 = [data1[i]['X'], data1[i]['Y'], data1[i]['Z']]
        r0 = [data0[i]['X'], data0[i]['Y'], data0[i]['Z']]
        dist = pbc_distance(r1, r0, cell1)
        msd += dist**2
    msd = math.sqrt(msd / len(data0))
    
    return msd

def plot_msd(time, cat_disp, an_disp, title):
    plt.scatter(time, cat_disp, c='r')
    plt.scatter(time, an_disp, c='k')
    plt.xlabel('Time')
    plt.ylabel('Root Mean Squared Deviation')
    plt.title(f'{title}')
    
    # calculate trendline
    z_cat = np.polyfit(time, cat_disp, 1)
    p_cat = np.poly1d(z_cat)
    plt.plot(time,p_cat(time),linestyle='--', color='r')

    z_an = np.polyfit(time, an_disp, 1)
    p_an = np.poly1d(z_an)
    plt.plot(time,p_an(time),linestyle='--', color='k')

    #plt.show()
    plt.savefig(f'{title}_RMSD.png')
    plt.clf()

    

###################
def test():
    path = '/Users/steve/doe-project/recomb/pt_production/'
    job = 'pt_coupled_20v'
    anode_id = 5
    cathode_id = 4
    timesteps = range(50000,1800000, 10000)
    cat_disp = []
    an_disp = []
    for t in tqdm(range(1, len(timesteps))):
        m1 = msd(cathode_id, path+job, timesteps[t], timesteps[0])
        cat_disp.append(m1)
        m2 = msd(anode_id, path+job, timesteps[t], timesteps[0])
        an_disp.append(m2)
    plot_msd(timesteps[1:], cat_disp, an_disp, title=job)

def main():
    identifier = 'cu'
    rootdir = f'/Users/steve/doe-project/recomb/{identifier}_production'
    jobs = []
    cathode_id = 4
    anode_id = 5

    # search rootdir for subdirectories and save them to a list
    for job in os.scandir(rootdir):
        if job.is_dir():
            name = str(job.path).split('/')[-1]
            if identifier in name:
                jobs.append(name)

    print(f'Job folders in {rootdir} are: \n{jobs}')
    for job in tqdm(jobs):
        timesteps = []
        cat_disp = []
        an_disp = []
        for file in os.listdir(f'{rootdir}/{job}'):
            if file.startswith('chg'):
                ts = int(file.split('.')[1])
                timesteps.append(ts)

        timesteps.sort()
        print(f'Plotting {job}\n')
        for t in tqdm(range(1, len(timesteps))):
            # m1 = msd(cathode_id, f'{rootdir}/{job}', timesteps[t], timesteps[t-1])
            m1 = msd(cathode_id, f'{rootdir}/{job}', timesteps[t], timesteps[0])
            cat_disp.append(m1)
            m2 = msd(anode_id, f'{rootdir}/{job}', timesteps[t], timesteps[0])
            # m2 = msd(anode_id, f'{rootdir}/{job}', timesteps[t], timesteps[t-1])
            an_disp.append(m2)

        plot_msd(timesteps[1:], cat_disp, an_disp, title=job)
        


if __name__ == '__main__':
    main()
    # test()