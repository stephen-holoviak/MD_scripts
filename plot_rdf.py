import read_TS 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from tqdm import tqdm

# Calculate the distance between atom a(list with [x,y,z]) and atom b in a periodic cell with dimensions cell=[x,y,z]
def pbc_distance(a, b, cell):
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

# find the z-position of the bottom and top of the solvent region for a dataframe with the timestep data from a lammps dump
# define cathode as the top slab and anode as the bottom slab
def find_solvent_region(timestep, cat_id, anode_id):
    cat_atoms = timestep[timestep['Type'] == cat_id]
    z_max = cat_atoms['Z'].min()

    anode_atoms = timestep[timestep['Type'] == anode_id]
    z_min = anode_atoms['Z'].max()
    return z_max, z_min

# find the volume of a sphere, less any part that would be outside the solvent region
def volume(z, r, z_bot, z_top):
    """ volume of a sphere of radius r located at height z """
    volume = 4.0 / 3.0 * math.pi * r**3
     
    """ cut off a spherical cap if the sphere extends below z_bot """
    if z - r < z_bot:
        h = z_bot - (z - r)
        volume -= math.pi * h**2 * (r - h / 3.0)
 
    """ cut off a spherical cap if the sphere extends above z_top """
    if z + r > z_top:
        h = z + r - z_top
        volume -= math.pi * h**2 * (r - h / 3.0)
     
    return volume

# given a dataframe with LAMMPS dump data, plot the rdf of the atoms with ids given in id
def calc_rdf(timestep, cell, z_bot, z_top, o_type = 5):
    # calculate some physical parameters needed for the rdf
    A = cell[0]
    B = cell[1]
    num_water = len(timestep[timestep['Type'] == o_type])
    water_volume = A * B * (z_top - z_bot)
    
    # set up the rdf calculation
    r_cutoff = min(cell) / 2.0  # only look 1/2 the smallest lattice parameter away to avoid double counting
    resolution = 1000
    dr = r_cutoff/resolution
    radii = np.linspace(0.0, r_cutoff, resolution)
    volumes = np.zeros(resolution)
    g_of_r = np.zeros(resolution)

    # iterate over all the oxygen atoms and calculate the number of atoms in a shell of radius r with thickness dr
    o_atoms = timestep[timestep['Type'] == o_type].reset_index()

    for index in tqdm(range(num_water)):   ###!!!NOTE: will need to change the range of the calculation if doing something other than O-O RDF
        row = o_atoms.iloc[index]
        o1_pos = [float(row['X']), float(row['Y']), float(row['Z'])]
        o1_ID = row['ID']
        o2_atoms = o_atoms[o_atoms['ID'] > o1_ID] 
        # Calculate volume of spherical shells (with cuts if appropriate)
        for j in range(resolution):
            r1 = j * dr
            r2 = r1 + dr
            v1 = volume(o1_pos[2], r1, z_bot, z_top)
            v2 = volume(o1_pos[2], r2, z_bot, z_top)
            volumes[j] += v2 - v1
        
        # Loop over the pairs of O atoms
        for index, row in o2_atoms.iterrows():
            o2_pos = [float(row['X']), float(row['Y']), float(row['Z'])]
            dist = pbc_distance(o1_pos, o2_pos, cell)
            bucket = int(dist/dr)
            if 0 < bucket < resolution:
                g_of_r[bucket] += 2.0

    # Normalize the RDF
    for index, value in enumerate(g_of_r):
        v_h2o = water_volume / num_water
        g_of_r[index] = value * v_h2o / volumes[index]

    return g_of_r, radii

def plot_rdf (radii, g, file='out.png', write=True):
    fig, ax = plt.subplots()

    ax.set_xlabel('r (Å)')
    ax.set_ylabel('g$_{OO}$(r)')
    ax.set_title('Water O-O RDF')
    ax.plot(radii, g)

    if write:
        plt.savefig(file, dpi=300, format='png')

    plt.show()

############################################

file = '/Users/steve/doe-project/recomb/pt_production/pt_coupled_5v/chg.2000000.lmp'
print('Reading File: ', file)
ts, data, cell = read_TS.read_TS(file, return_cell=True)
print('cell dimmensions: ', cell)

cat = 4
anode = 5
oxygen = 1

zmax, zmin = find_solvent_region(data, cat, anode)
print('solvent z max = ', zmax, ' z min = ', zmin)


num_water = len(data[data['Type'] == oxygen])
o_atoms = data[data['Type'] == oxygen].reset_index()

g_r, r= calc_rdf(data, cell, zmin, zmax, o_type=oxygen)
plot_rdf(r, g_r, file='new.png')