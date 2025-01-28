This depository contains the paramter files for running the schism model (https://doi.org/10.5281/zenodo.14192592), as well as the python scripts and jupyter notebooks used for analyzing the results.

### CONTENT:
1. Parameter input files
   
   **model_paramfiles**
     - **general:**     all files, that do not change between the different runs
     - **no_sg:**       input files that are specific to the no seagrass scenario runs
     - **stat_sg_int:** input files that are specific to the stat sg [int] scenario runs
     - **stat_sg_ref:** input files that are specific to the stat sg [ref] scenario runs
     - **var_sg_int:** imput files that are specific to the var sg [int] scenario runs
     - **var_sg_ref:**  input files that are specific to the var sg [ref] scenario runs
   
   In order to run the model, the SCHISM model has to be build and all necessary input files have to be gathered in a single folder. All input data except for the sflux files is availiable in this repository. The sflux files can be generated according to the SCHISM conventions using the coastDat-3 dataset (Helmholtz-Zentrum Geesthacht, Zentrum für Material- und Küstenforschung GmbH (HZG) (2017). coastDat-3_COSMO-CLM_ERAi. World Data Center for Climate (WDCC) at DKRZ. http://cera-www.dkrz.de/WDCC/ui/Compact.jsp?acronym=coastDat-3_COSMO-CLM_ERAi)
   
2. Python scripts and Jupyter Notebooks for analyzing and plotting the results

   **SchismUtils**
     - contains utility files for reading the schism output files schout_*.n that are called in the plotting functions
   
   **SyltRomo** 
     - plotting files for simulated mean meadow canopy height and growth density and comparison to observerd data (Figure 2, Figure 6)
     - preparation files for eroded volume plots
   
   **jupyter_notebook/SR5yr**
     - plotting files for depth change across the flats (Figure 4)
     - validation of simulated wl and temp (Figure 3a)
     - mean canopy height, water temperature and solar radiation (Figure 5)
     - mean canopy height, shoot density inside single meadow (Figure 7)
     - relative change to erosion and velocity (Figure 8, Figure 10)
     - areas with relative velocity/depth change vs. meadow area (Figure 9/11)
     - sediment volume change in different parts in intertidal/ sutidal (Figure 12)
     - storm impact (Figure 13, Figure 14)
   
   **sim_obs/stations**
     - water level and water temperature validation plots (Figure 3b,c)
