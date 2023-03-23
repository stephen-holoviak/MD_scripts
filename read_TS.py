# Reads lammps dump file and puts the data in a Pandas dataframe

import pandas as pd

def read_TS(file, return_cell = False):
    # read in the data file for a given timestep and convert to a dataframe
    input = open(file, 'r')
    raw_data = input.readlines()
    input.close()

    timestep = int(raw_data[1])
    ts_data = {'ID':[], 'Type':[], 'X':[], 'Y':[], 'Z':[], 'Q':[]}

    for line in raw_data[9:]:
                ld = line.split()
                #print(ld)
                ts_data['ID'].append(int(ld[0]))
                ts_data['Type'].append(int(ld[1]))
                ts_data['X'].append(float(ld[2]))
                ts_data['Y'].append(float(ld[3]))
                ts_data['Z'].append(float(ld[4]))
                ts_data['Q'].append(float(ld[5]))

    run_data = pd.DataFrame.from_dict(ts_data)
    run_data = run_data.sort_values(by=['ID'])

    if return_cell:
        cell_x = float(raw_data[5].split()[0]) + float(raw_data[5].split()[1]) # casts from string in scientific notation to float and sums lammps xmin & xmax
        cell_y = float(raw_data[6].split()[0]) + float(raw_data[6].split()[1])
        cell_z = float(raw_data[7].split()[0]) + float(raw_data[7].split()[1])
        cell = [cell_x, cell_y, cell_z]
        return timestep, run_data, cell
    else:
        return timestep, run_data
