#!/bin/bash
export LAMMPS_EXEC=/home/steve/lammps-23Jun2022/build/lmp_yes
export OMP_NUM_THREADS=1

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

mpiexec -n 1 -wdir $SCRIPTPATH/ $LAMMPS_EXEC -in job.lmp