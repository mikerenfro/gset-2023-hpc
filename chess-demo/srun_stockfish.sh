#!/bin/bash
#. /opt/ohpc/pub/spack/v0.20.0/share/spack/setup-env.sh
#spack load openmpi
#srun --nodes=$1 --cpus-per-task=$2 ./stockfish
salloc --nodes=$1 --ntasks-per-node=$2 mpirun -np $(($1 * $2)) ./stockfish