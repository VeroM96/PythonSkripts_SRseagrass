#!/bin/bash
#SBATCH --job-name=mhot
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --mail-type=NONE
#SBATCH --account=gg0877
#SBATCH --output=merge_hotstart.o
#SBATCH --error=merge_hotstart.e

###Load  module files
module load netcdf_c/4.3.2-gcc48
module load intel/18.0.4
module load intelmpi/5.1.3.223
export I_MPI_PMI_LIBRARY=/use/lib64/libmpi.so

#define important directories
this_dir=$PWD
merge_bin_path=/home/g/g260204/schism-5.8/build/bin/combine_hotstart7
mergepath=/scratch/g/g260204/SR5yr/srm020_2010
cd $mergepath

#find biggest timestep
biggest_t=0
for f in hotstart_*_*.nc; do
  file=$f
  IFS='_' read -ra ADDR <<< "$file"  #Internal Field Seperator
  dtnc=${ADDR[2]}
  IFS='.' read -ra ADDR <<< "$dtnc"  #Internal Field Seperator
  dt=${ADDR[0]}
  if [ $biggest_t -lt $dt ]
    then biggest_t=$dt
  fi
done

#merge hotstart with biggest timestep and copy it here
$merge_bin_path -i $biggest_t
rm $this_dir\/hotstart.nc
ln -s $this_dir\/outputs\/hotstart_it\=$biggest_t\.nc $this_dir\/hotstart.nc
cd $this_dir

