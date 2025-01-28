#!/bin/bash
#SBATCH --job-name=m_srm020_2010
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --account=gg0877
#SBATCH --time=03:00:00
#SBATCH --wait-all-node=1
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=veronika.mohr@hereon.de
#SBATCH --output=error_merge.o
#SBATCH --error=error_merge.e

###Load  module files
module load netcdf_c/4.3.2-gcc48
module load intel/18.0.4
module load intelmpi/5.1.3.223

from=$2
to=$3
outpath=$1
cd $outpath
/home/g/g260204/schism_noicm/build/bin/combine_output11 -b $from -e $to > combine.txt

