#!/bin/bash
#SBATCH -J N20_B_nomol
#SBATCH -A mp149
#SBATCH -C cpu
#SBATCH -q regular
#SBATCH -N 2
#SBATCH --ntasks-per-node 64
#SBATCH -c 2
#SBATCH -t 08:00:00
#SBATCH -o slurm-%j.out
#SBATCH -e slurm-%j.err
#SBATCH --mail-user=jmn951@naver.com
#SBATCH --mail-type=BEGIN,END,FAIL

cd /pscratch/sd/y/ywchoi/nangman/12-perturbation-range/N20_B_nomol

module load PrgEnv-gnu

export OMP_NUM_THREADS=2
export OMP_PLACES=threads
export OMP_PROC_BIND=spread
export LD_LIBRARY_PATH=/global/homes/y/ywchoi/local/lib:$LD_LIBRARY_PATH

SIESTA=/global/homes/y/ywchoi/siesta/_build/Src/siesta

ldd $SIESTA 2>&1 | grep -iE "elpa|sci"

srun -n 128 -c 2 --cpu_bind=cores $SIESTA < input.fdf > siesta.stdout 2>&1
