#!/bin/bash
#SBATCH --job-name=copym
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --mail-type=NONE
#SBATCH --account=gg0877
#SBATCH --output=copy_mirror.o
#SBATCH --error=copy_mirror.e

ver=$1
new="outputs/mirror_${ver}.out"

cp outputs/mirror.out $new

