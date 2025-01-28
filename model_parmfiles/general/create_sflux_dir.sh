#!/bin/bash

datadir=/work/gg0877/KST/cD3/schism-sflux_cD3_011_ERAi/
years=(2010)
months=(01 02 03 04 05 06 07 08 09 10 11 12)
#months=(01)

rm -rf ./sflux

mkdir -p sflux

i=0

for year in ${years[@]}; do
  for month in ${months[@]}; do
    i=$((i+1))
    num=`printf %04d $i`
    ln -sf ${datadir}/cD3.air.${year}_${month}.nc sflux/sflux_air_1.${num}.nc
    ln -sf ${datadir}/cD3.rad.${year}_${month}.nc sflux/sflux_rad_1.${num}.nc
    ln -sf ${datadir}/cD3.prec.${year}_${month}.nc sflux/sflux_prc_1.${num}.nc
  done
done

    i=$((i+1))
    num=`printf %04d $i`
    ln -sf ${datadir}/cD3.air.$((year+1))_01.nc sflux/sflux_air_1.${num}.nc
    ln -sf ${datadir}/cD3.rad.$((year+1))_01.nc sflux/sflux_rad_1.${num}.nc
    ln -sf ${datadir}/cD3.prec.$((year+1))_01.nc sflux/sflux_prc_1.${num}.nc


# write namelist file
cat > sflux/sflux_inputs.txt << EOL
&sflux_inputs
!start_year = ${years[0]}, ! start year 
!start_month = ${months[0]}, ! start month 
!start_day = 01, ! start day 
!start_hour = 0.0, ! start hour 
!utc_start = 0.0, ! offset from UTC in hours, with positive numbers for western hemishpere 
/
EOL




