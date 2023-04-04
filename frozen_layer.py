from ase import Atom, Atoms
from ase.io.lammpsdata import write_lammps_data, read_lammps_data
from ase.io.lammpsrun import read_lammps_dump_text
import read_TS as ts

# ---------- read in the template structure, 2 slab electrodes(type 3) seperated by water (type 1,2)
in_ats = read_lammps_data('ni_eq_OUT.lmp', style='charge', units='metal')
#in_ats = read_lammps_dump_text('cu_NVT_out.lmp')
#time, data, uc = ts.read_TS('pt_eq_OUT.lmp', return_cell=True)

# in_ats = Atoms(cell=uc)
# for index, row in data.iterrows():
#     atom = Atom(row['Type'], (row['X'], row['Y'], row['Z']))
#     in_ats.append(atom)

# ---------- find the z level of each layer in the electrodes
unique_Zs = []

for atom in in_ats:
    if atom.number in [1,2,3,6] and round(atom.z,0) not in unique_Zs:
        unique_Zs.append(round(atom.z,0))

unique_Zs.sort()
print(unique_Zs)

# ---------- Change the id number of each layer to proper group
for atom in in_ats:
    if atom.number == 3 and round(atom.z,0) == unique_Zs[-1:]: # cathode (top)
        atom.number = 7
    if atom.number == 6 and round(atom.z,0) in unique_Zs[:2]: # anode (bottom)
        atom.number = 8
write_lammps_data('ni_clean.input', atoms=in_ats, units='metal', atom_style='charge')