#!/bin/bash
#SBATCH --job-name=srm020_2010
#SBATCH --partition=compute
#SBATCH --ntasks=768
#SBATCH --ntasks-per-node=128
#SBATCH --account=gg0877
#SBATCH --time=8:00:00
#SBATCH --wait-all-node=1
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=veronika.mohr@hereon.de
#SBATCH --output=error_run.o
#SBATCH --error=error_run.e

###Load  module files
#module load netcdf_c/4.3.2-gcc48
#module load intel/18.0.4
#module load intelmpi/5.1.3.223
#module load intel
#module load ncview
#module load intelmpi
#module load netcdf_c/4.3.2-gcc48

module load intel-oneapi-compilers
module load ncview
module load openmpi
module load intel-oneapi-mpi
module load netcdf-c
module load netcdf-cxx
module load netcdf-fortran
module load python3

ulimit -c 0
ulimit -s 1500000
srun --propagate=STACK,CORE --cpu_bind=cores \
  --distribution=block:cyclic --export=ALL ./pschism

###Define paths
outpath=$1
rundir=$PWD


sed -i "s/ihot = 2/ihot = 0/g" param.nml

rnday="`grep 'rnday =' param.nml`"
IFS=' ' read -ra ADDR <<< "$rnday"  #Internal Field Seperator
newday="74"

sed -i "s/rnday = ${ADDR[2]}/rnday = $newday/g" param.nml

###Define paths
outpath=$1
rundir=$PWD

###Create link to output folder and copy setup files
mkdir -p $outpath || true
ln -sf $outpath $rundir/outputs
rm -rf $outpath/* || true
mkdir -p $outpath/plots || true

#srun --cpu-freq=HighM1 /pf/g/g260149/schism/src/pschism_BORA_Intel_VL
srun --cpu-freq=HighM1 /home/g/g260204/schism_shoots_wind/build/bin/pschism_ICM_SED_TVD-SB
