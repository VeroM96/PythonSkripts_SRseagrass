# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:55:02 2022

@author: Vero
"""

import os.path
#from plot_elev_obs import plot_elev
#from plot_temp_obs import plot_temp
#from plot_hyps import plot_hyp
#from plot_morph import plot_morph
#from plot_hyps_dev import plot_hyps_dev
#from old_hcan.plot_hsav import plot_hsav
from plot_hcan_all_obs import plot_hcan
from plot_N_all_obs import plot_n
#from plot_hcan_N_obs import plot_hcan_n

##main for defining paths and evironment vars
rnames= [["srm024_2010"],["srm024_2011"],["srm024_2012"],["srm024_2013"],["srm024_2014"],['srm024_2015']]
last = "11"
mspeed = 1;
pointst = [44444] #Temperature, grid SyltRomo100
points = [27906, 39222, 44444, 48718] #grid SyltRomo 100
facessg = [25248,51400,28015,41419,54751,62107,87992,87456] #(all -1) grid SyltRomo 100 
#points = [13563, 12914, 8840, 12671] #grid SyltRomo 50
#points = [1749, 2752, 1305, 1379] #grid SyltRomo 200


schout_path = "/work/gg0877/g260204/sim_data/SR5yr/"
for rname in rnames:
    plot_path = "/work/gg0877/g260204/sim_data/SR5yr/plots/plots/" + rname[0] +'/' 


    if not os.path.exists(schout_path + rname[0]):
        print('input folder does not exist')
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

#    plot_elev(schout_path,rname,plot_path, points) #plot water elevation.
#    plot_temp(schout_path,rname,plot_path, pointst) #plot water temperature
    plot_hcan(schout_path,rname,plot_path,facessg) #plot developent of canopy height
    plot_n(schout_path,rname,plot_path,facessg) #plot developent of meadow density
#plot_hcan_n(schout_path,rname,plot_path,facessg) #plot canopy height vs meadow density
#plot_hyp(schout_path,rname,plot_path, last,mspeed) #plot hypsometry at last time step
#plot_morph(schout_path,rname,plot_path,last,mspeed) #plot morphology at last time step
#plot_hyps_dev(schout_path,rname,plot_path,mspeed) #plot development of mean depth 
#plot_hsav(schout_path,rname,plot_path,last,mspeed) # plot sav hight at last time step
