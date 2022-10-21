from asyncore import write
from ase import Atom, Atoms
from ase.io.lammpsdata import write_lammps_data, read_lammps_data

# ---------- read in the template structure, 2 slab electrodes(type 3) seperated by water (type 1,2)
in_ats = read_lammps_data('alpha-pt-o2.input', style='charge', units='metal')

# ---------- find the z level of each layer in the electrodes
# unique_Zs = []

# for atom in in_ats:
#     if atom.number == 4 and round(atom.z,0) not in unique_Zs:
#         unique_Zs.append(round(atom.z,0))

# unique_Zs.sort()
# print(unique_Zs)

# # ---------- Change the id number of each layer to proper group
# for atom in in_ats:
#     if atom.number == 3:
#         if round(atom.z,2) == unique_Zs[0] or round(atom.z,2) == unique_Zs[1]  or round(atom.z,2) == unique_Zs[2]:
#             atom.number = 3 # bottom thermo Pt
#         if round(atom.z,2) == unique_Zs[3] or round(atom.z,2) == unique_Zs[4]  or round(atom.z,2) == unique_Zs[5]:# or round(atom.z,2) == unique_Zs[6]:
#             atom.number = 4 # bottom working Pt
#         if round(atom.z,2) == unique_Zs[6] or round(atom.z,2) == unique_Zs[7] or round(atom.z,2) == unique_Zs[8]: #or round(atom.z,2) == unique_Zs[10]:
#             atom.number = 5 # top working Pt
#         if round(atom.z,2) == unique_Zs[9] or round(atom.z,2) == unique_Zs[10] or round(atom.z,2) == unique_Zs[11]:
#             atom.number = 6 # top thermo Pt
#     if atom.number == 2 and atom.z > 103.0: # seperate the top oxide & water
#         atom.number = 7
#     if atom.number == 2 and atom.z < 29.0: # seperate the bottom oxide & water
#         atom.number = 8

for atom in in_ats:
    if atom.number == 4:
        if round(atom.z,1) < 20.5:
            atom.number = 5 # bottom thermo layer
        if round(atom.z, 1) > 117.0:
            atom.number = 6 # top thermo
for atom in in_ats:
    if atom.number == 4 and round(atom.z,1) > 100.0:
        atom.number = 7 # should have removed thermo layers from consideration, then seperate top work layer from bottom work layer
    if atom.number == 2 and atom.z > 100.0:
        atom.number = 8

write_lammps_data('out.lmp', atoms=in_ats, units='metal', atom_style='charge')