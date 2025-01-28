# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:49:58 2022

@author: Vero
"""

from netCDF4 import Dataset

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.tri as tri
import matplotlib as mpl
mpl.use('Agg')
import glob
import h5py

import os.path
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SchismUtils/')
from schism_utils import sort_files, read_data

#-----INPUT-----------------------------------------------------------------
#rname = ['sr020','sr059','sr060']
#labels=['sr020','increased wsed','increased critical shear stress']
#figname = "0xx_erodep"

#rname = ['srm001_2012','srm005_2012','srm008_2012']
#labels=['no seagrass','static seagrass','variable seagrass']
#figname = "srm1-5-8_2012"

#savref = 'srm008_2012'



#rname = ['srm_settling_006','srm_settling_007','srm_settling_009','srm_settling_011','srm_settling_012','srm_settling_013']
#labels=['settling 6','settling 7','settling 9','settling 11','settling 12','settling 13']
#figname = "srmsettling_all"


year = '2015'
runs=['srm020','srm026','srm024','srm035','srm036']
rname = [r+'_'+year for r in runs]
labels=['no sg','stat sg (ref)','var sg (ref)','stat sg (int)','var sg (int)']
figname = 'srm02x3x_'+year

savref = 'srm024_'+year

#rname = ['srm001_2015','srm002_2015','srm003_2015']
#labels=['no seagrass','static seagrass','variable seagrass']
#figname = "xx_2015"

#rname = ['sr320','sr355','sr351']
#labels=['no seagrass','static seagrass','variable seagrass']
#figname = "3xx_final"


#rname = ['sr058']
#labels=['sr058']
#figname = "sr058"

colors = ['tab:blue','midnightblue','gold','tab:orange','wheat','tan','peru','tab:green','lightgreen','darkseagreen','darkgreen','teal']
spat = "/work/gg0877/g260204/sim_data/SR5yr/"
savepat = "/work/gg0877/g260204/SR5yr/plots/plots/" + figname + '/'
#savref = 'srm007_2010'
hcanlim1 = 0.1
hcanlim2 = 0.02
mean_hw = 0.9 #m
mean_lw = -0.9 #m
#---------------------------------------------------------------------------

def moving_average(x,w):
    return np.convolve(x,np.ones(w),'valid')/w

if not os.path.exists(savepat):
    os.makedirs(savepat)

#count = 0
fig,axs  = plt.subplots(2,1,figsize=(14.90,13), gridspec_kw={'height_ratios': [1, 4]})
Tid_amp = mean_hw-mean_lw

#define area for sav -> needs to be constant for all runs to compare changes!
ncpat = spat + savref + '/outputs'
print(ncpat)
files_sorted = sort_files(ncpat)
ncdata=Dataset(files_sorted[0],mode='r')

hcan  = read_data('ICM_hcansav',files_sorted,ntime=range(0,1))
hcan_0 = np.mean(hcan,0)

sav_fac = np.zeros(np.size(hcan_0))
isav = np.where(hcan_0 > hcanlim1)
isav2 = np.where((hcan_0 <= hcanlim1)*(hcan_0 > hcanlim2))
inosav = np.where(hcan_0 <= hcanlim2)
sav_fac[isav] = 1


#area inside basin
hdf5pat = '/work/gg0877/g260204/data/pickle_files/mask_basin.hdf5'
f = h5py.File(hdf5pat,'r')
nin = f['nin'][:]

#calculate area and ini depth of element
x = ncdata.variables['SCHISM_hgrid_node_x'][:]
y = ncdata.variables['SCHISM_hgrid_node_y'][:]
tri = ncdata.variables['SCHISM_hgrid_face_nodes'][:, :3]-1
depth = ncdata.variables['depth'][:]

ii = np.where(np.sum(nin[tri],1)==3)
f.close()

#convert x,y from lat, lon to meters. use min(x),min(y) as reference x -> lon, y = lat
#approximation is enough: 1deg lat = 111.319 km; 1 deg lon = 111.319 km * cos(phi)
r_earth = 40075000 #m
x = (x-min(x))*r_earth/360*np.cos(np.mean(y)*np.pi/180)
y = (y-min(y))*r_earth/360

tri_x = x[tri]
tri_y = y[tri]
tri_y_c = np.mean(tri_y,1)
tri_d = -depth[tri]
A = 0.5*(np.multiply(tri_x[:, 0], (tri_y[:, 1]-tri_y[:, 2]))
         + np.multiply(tri_x[:, 1], (tri_y[:, 2]-tri_y[:, 0]))
         + np.multiply(tri_x[:, 2], (tri_y[:, 0]-tri_y[:, 1])))
d_el = np.mean(tri_d,1)
wat_vol = (Tid_amp-d_el)*A

#volume change only inside basin & subtidal area (depth < mean_lw)
#iit1 = np.where(d_el <mean_lw)
iit2 = np.where(d_el >= mean_lw)

d_el[ii] = 0
#d_el[iit1] = 0
d_el[iit2] = 0
A[ii] = 0
#A[iit1] = 0
A[iit2] = 0
wat_vol[ii] = 0
wat_vol_tot = np.sum(wat_vol)
A_sav   = A[isav]
A_sav2  = A[isav2]
A_nosav = A[inosav]

h5pypath= '/work/gg0877/g260204/data/pickle_files/' + figname + '_subtidal_' + str(hcanlim1) + '_' + str(hcanlim2) + '.hdf5'
fout = h5py.File(h5pypath,'w')

sav=False
print('A_sav',np.shape(A_sav))
for count in range(0,len(rname)):
    run = rname[count]
    ncpat = spat+run +'/outputs'
    files_sorted = sort_files(ncpat)
    
    ncdata=Dataset(files_sorted[0],mode='r')
    keys = ncdata.variables.keys()

    [depth_change,time] = read_data(['SED_depth_change','time'],files_sorted,ntime=range(0,1))
    if 'ICM_hcansav' in keys:
        sav=True
        hcansav      = read_data('ICM_hcansav',files_sorted,ntime=range(0,1))
        hcan_sav   = np.mean(np.squeeze(hcansav[:,isav]),1) 
        hcan_sav2  = np.mean(np.squeeze(hcansav[:,isav2]),1)
        hcan_nosav = np.mean(np.squeeze(hcansav[:,inosav]),1)
        ave_hcan = hcan_sav #moving_average(hcan_sav,1)
        ave_hcan2 = hcan_sav2#moving_average(hcan_sav2,1)
        ave_hcan_no = hcan_nosav #moving_average(hcan_nosav,1)


    d_change_el  = np.mean(depth_change[:,tri],2)
    d_change_el[:,ii]     = 0
    d_change_el[:,iit2]   = 0
#    d_change_el[:,iit1] = 0
    d_change_sav   = np.squeeze(d_change_el[:,isav])
    d_change_sav2  = np.squeeze(d_change_el[:,isav2])
    d_change_nosav = np.squeeze(d_change_el[:,inosav])

    Vol    = np.sum(d_change_sav*A_sav,1)
    Vol2   = np.sum(d_change_sav2*A_sav2,1)
    Vol_no = np.sum(d_change_nosav*A_nosav,1)

    norm_v = Vol#/wat_vol_tot 
    norm_v2 = Vol2#/wat_vol_tot
    norm_v_no = Vol_no#/wat_vol_tot
    ave_v = norm_v #moving_average(norm_v,1)
    ave_v2 = norm_v2 #moving_average(norm_v2,1)
    ave_v_no = norm_v_no #moving_average(norm_v_no,1)

    axs[1].plot(time, ave_v, linewidth=5,label = labels[count]+ ';                      canh > '+ str(hcanlim1)+' m',color=colors[count],linestyle='dotted')
    axs[1].plot(time, ave_v2, linewidth=5,label = labels[count]+ '; '+ str(hcanlim1)+ ' m     >= canh > ' + str(hcanlim2)+ ' m',color=colors[count],linestyle='dashed')
    axs[1].plot(time, ave_v_no,linewidth=5,label = labels[count] + '; '+str(hcanlim2) + ' m >= canh',color=colors[count])


#    axs[1].plot(time_con, vol_con, linewidth=5,label = labels[count]+ ';                      canh > '+ str(hcanlim1)+' m',color=colors[count],linestyle='dotted')
#    axs[1].plot(time_con, vol_con2, linewidth=5,label = labels[count]+ '; '+ str(hcanlim1)+ ' m     >= canh > ' + str(hcanlim2)+ ' m',color=colors[count],linestyle='dashed')
#    axs[1].plot(time_con, vol_con_no,linewidth=5,label = labels[count] + '; '+str(hcanlim2) + ' m >= canh',color=colors[count])
    print(norm_v[-1],np.sum(A_sav),labels[count],colors[count],run)
    print(norm_v2[-1],np.sum(A_sav2),labels[count],colors[count],run)
    print(norm_v_no[-1],np.sum(A_nosav),labels[count],colors[count],run)
    #count = count+1

    print(wat_vol_tot)
    fout[run+"_highcan"]=norm_v
    fout[run+"_midcan"]=norm_v2
    fout[run+"_nocan"]=norm_v_no
if sav:
    fout[run+'_hcan_highcan']= ave_hcan
    fout[run+'_hcan_midcan'] = ave_hcan2
    fout[run+'_hcan_nocan']=ave_hcan_no
fout.close()
axs[1].set_xlabel("time [years]", fontsize=34)
axs[1].set_ylabel("Net sediment volume change [m$^3$]", fontsize=34)
axs[1].yaxis.set_tick_params(labelsize=28)
#plt.ylim([-0.035,0])
axs[1].xaxis.set_tick_params(labelsize=28)

axs[1].legend(fontsize=26)

axs[1].yaxis.get_major_formatter().set_powerlimits((0, 1))
axs[1].yaxis.offsetText.set_fontsize(24)
axs[1].yaxis.get_major_formatter().set_useMathText('true')

#plt.savefig(savepat + "eroded_vol_intertidal_sav_" +str(hcanlim1) + '_two2_' +  figname +'.png')#,format='pdf' )
#plt.clf()

#print(mm_range)
#print(wat_vol_tot)        
        
#fig2 = plt.figure(2)
#plt.tripcolor(x,y,tri,d_el*sav_fac)
#plt.savefig(savepat + "eroded_vol_intertidal_sav_area_" + str(hcanlim2) +".png")

if sav:
    axs[0].plot(time, ave_hcan, linewidth=5,color='green',linestyle='dotted')
    axs[0].plot(time, ave_hcan2, linewidth=5,color='green',linestyle='dashed')
    axs[0].plot(time, ave_hcan_no,linewidth=5,color='green')
axs[0].set_yticks([0.05,0.2, 0.35])
axs[0].yaxis.set_tick_params(labelsize=28)
axs[0].set_ylabel("hcan [m]", fontsize=34)
axs[0].set_xticks([])
plt.tight_layout()
plt.savefig(savepat + "eroded_vol_subtidal_sav_hcan_subplot_"+ str(hcanlim1) +'_two_' + figname +'.pdf',format='pdf' )
        
