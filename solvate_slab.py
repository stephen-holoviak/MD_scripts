# Take an orthogonal slab, mirror it to build a electrode system, then add in the water box built with packmol

from ase import Atom, Atoms
import ase.io.vasp as vasp
import ase.io.lammpsdata as lammps
import numpy as np

# Simulation parameters:
electrolyte_thickness = 76.0
vacuum = 15.0


# Read in the single electrode 
#slab = vasp.read_vasp(file='p2x2_vac.vasp')
slab = lammps.read_lammps_data(file='alpha-pt-o2_vac.input', Z_of_type=[1, 7, 78], units='metal', style='charge')
slab.center(15.0, axis=2)

# extract slab geometry
pos = np.copy(slab.get_positions())
xmax, ymax, zmax = pos.max(axis=0)
xmin, ymin, zmin = pos.min(axis=0)
slab_thickness = zmax - zmin
print('Slab thickness = '+str(slab_thickness) +', zmax = ' + str(zmax))

# Extend the cell for electrolyte, and the other electrode (computed above)
x,y,z = slab.get_cell()
z = [0,0,vacuum + slab_thickness + electrolyte_thickness + slab_thickness + vacuum]
cell = [x,y,z]
slab.set_cell(cell)
print('Cell Dimmensions: \n  a= ' + str(x)+'\n  b= ' + str(y) + '\n  c= ' + str(z))

# Mirror the electrode about the xy-plane halfway up the z-axis
mirror_plane = z[2]/2
for atom in slab:
    slab.append(Atom(atom.symbol, position = [atom.x, atom.y, mirror_plane + (mirror_plane - atom.z)]))
###############################

#lammps.write_lammps_data('test.input', atoms = slab, units = 'metal', atom_style = 'charge')
#vasp.write_vasp(file = 'test.vasp', atoms=slab, vasp5=True)

# add in the water
water = lammps.read_lammps_data(file='water.input', Z_of_type= [1,1,8], units='metal', style='charge')

for atom in water:
    slab.append(Atom(atom.symbol, position = [atom.x + 1.5, atom.y + 1.5, atom.z + zmax + 2.5]))

lammps.write_lammps_data('alpha-pt-o2.input', atoms = slab, units = 'metal', atom_style = 'charge')
