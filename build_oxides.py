from ase.io import vasp, lammpsdata
from ase import Atom, Atoms, build

#slab = build.fcc111('Ni', size=(14,16,6), orthogonal=True)
slab = vasp.read_vasp(file='o_2x2.vasp')

for atom in slab:
    if atom.symbol == 'O':
        atom.y = atom.y - 1.6

slab.center(vacuum=30.0, axis=2)
lammpsdata.write_lammps_data(file='./p2x2_vac.input', atoms=slab, units='metal', atom_style='charge')
vasp.write_vasp(file='p2x2_vacuum.vasp', atoms=slab, vasp5=True)
# multiplier = [[6,0,0], [0,7,0], [0,0,1]]
# super = build.make_supercell(slab, multiplier)

# slab.center(vacuum=10, axis=2)
# super.center(vacuum=10, axis=2)



# vasp.write_vasp(file='./test.vasp', atoms=slab, vasp5=True)
# vasp.write_vasp(file='./super.vasp', atoms=super, vasp5=True)