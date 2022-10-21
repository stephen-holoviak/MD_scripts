import pandas as pd
import os, math

def read_TS(file = '/Users/steve/doe-project/reductive_reconstruction/oxide_tests/structures/pt/coupled_1.0/chg.0.lmp'):
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
                ts_data['X'].append(float(ld[2])*33.262)
                ts_data['Y'].append(float(ld[3])*33.607)
                ts_data['Z'].append(float(ld[4])*128.632)
                ts_data['Q'].append(float(ld[5]))

    run_data = pd.DataFrame.from_dict(ts_data)
    run_data = run_data.sort_values(by=['ID'])

    return timestep, run_data

def seperate_layer(data: pd.DataFrame, types: list, zmin: float, zmax: float):
    # data = pd.Dataframe, types = list of atom ids to include, zmin/zmax = range of values for the layer
    layer = data[(data['Type'].isin(types)) & (data['Z'] > zmin) & (data['Z'] < zmax)]
    numAtoms = len(layer.ID)
    totalQ = layer['Q'].sum()
    avgQ = totalQ / numAtoms
    minQ = layer['Q'].min()
    maxQ = layer['Q'].max()
    return totalQ, avgQ, maxQ, minQ, numAtoms

