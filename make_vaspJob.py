#sbs5563_c_g_bc_default

pbs_str = '''#!/bin/sh
#PBS -l feature=rhel7
#PBS -N {}
#PBS -o scheduler.log
#PBS -e scheduler.err
#PBS -l walltime={}:00:00
#PBS -l nodes={}:ppn=20

#PBS -A sbs5563_f_g_bc_default

cd $PBS_O_WORKDIR
export UCX_TLS=all

module purge
module use /gpfs/group/RISE/sw7/modules
module load intel mkl impi
module load vasp/vasp-5.4.1a

mpirun vasp_gam'''
##########################################

incar_str = '''ENCUT = {}
EDIFF = 1E-4
EDIFFG = -25E-3

IBRION = 2
NSW = 250
NELM = 400
NELMIN = 8
ALGO = Fast
PREC = Accurate
LREAl = Auto
NCORE = 4

ISPIN = 1
ISMEAR = 0
SIGMA = {}

ISIF = 2
ISYM = 2'''
###########################################

k_str = '''Automatic mesh
0
Gamma
{}  {}  {}
0. 0. 0.'''


def write_PBS(job_path, job_name='test', hours='48', nodes='4'):
    with open('{}/runPBS'.format(job_path), 'w') as writer:
        writer.write(pbs_str.format(job_name, hours, nodes))

def write_INCAR(job_path, encut='400', sigma='0.05'):
    with open('{}/INCAR'.format(job_path), 'w') as writer:
        writer.write(incar_str.format(encut, sigma))

def write_KPOINTS(job_path, kx, ky, kz):
    with open('{}/KPOINTS'.format(job_path), 'w') as writer:
        writer.write(k_str.format(kx, ky, kz))
