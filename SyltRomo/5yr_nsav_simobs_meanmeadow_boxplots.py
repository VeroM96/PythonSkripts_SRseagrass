#find points in meadows
from datetime import datetime, timedelta

from netCDF4 import Dataset
import numpy as  np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

import glob
import os.path
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SchismUtils/')
from schism_utils import read_data, sort_files

from matplotlib import rcParams
rcParams['figure.dpi'] = 500

#seagras meadows
import geopandas as gpd
sg_de_pat = '/work/gg0877/g260204/sim_data/SyltRomo/01_preprog/100m2014/seegrass_2014_DE.shp'
sg_dk_pat = '/work/gg0877/g260204/sim_data/SyltRomo/01_preprog/100m2014/seegrass_2014_DK.shp'
shp_pat =  '/work/gg0877/g260204/sim_data/SyltRomo/01_preprog/100m/syltromo_silhouette.shp'
sg_de = gpd.read_file(sg_de_pat)
sg_dk = gpd.read_file(sg_dk_pat)
sg_de = sg_de.to_crs("EPSG:4326")
sg_dk = sg_dk.to_crs("EPSG:4326")
sg_de = sg_de.cx[:,54.885:]
sg_dk = sg_dk.cx[:,:55.14]
#    sg_de.boundary.plot(ax=plt.gca(),color='red',linewidth=0.5)
#    sg_dk.boundary.plot(ax=plt.gca(),color='red',linewidth=0.5)

#### split danish seagrass into subsections
sg_havn = sg_dk[sg_dk['Område']=='Havneby Nord']
sg_havs = sg_dk[sg_dk['Område']=='Havneby Syd']
sg_kold = sg_dk[sg_dk['Område']=='Koldby']
sg_ball = sg_dk[sg_dk['Område']=='Ballum']
sg_jord = sg_dk[sg_dk['Område']=='Jordsand']

#split german seagrass into subsections
sg_rick = sg_de[3:9]
sg_hind = sg_de[9:13]
sg_mors = sg_de[13:15]
sg_keit = sg_de[15:24]
sg_kamp = sg_de.iloc[[2,24]]
sg_koen = sg_de.iloc[[0,1,25,26]]

in_path = "/work/gg0877/g260204/sim_data/SR5yr/"
rname = 'srm022'
run = rname + '_2010'
ncfilen = '365'

files_sorted = sort_files(in_path+run+'/outputs')

plotpath = in_path + 'plots/plots/' + rname +'/'


if not os.path.exists(plotpath):
    os.makedirs(plotpath)
#subsection Sylt-Romo
latd = 54.846448
latu = 55.163381
lonl = 8.190103
lonr = 8.73308

#read data
ncdata = Dataset(files_sorted[0], mode='r')
keys = ncdata.variables.keys()
#time independent
x       = ncdata.variables['SCHISM_hgrid_node_x'][:]
y       = ncdata.variables['SCHISM_hgrid_node_y'][:]
x_face  = ncdata.variables['SCHISM_hgrid_face_x'][:]
y_face  = ncdata.variables['SCHISM_hgrid_face_y'][:]
tri     = ncdata.variables['SCHISM_hgrid_face_nodes'][:,:3]-1
depth   = ncdata.variables['depth'][:]

#####################################################################
iin= []
from shapely.geometry import Point
#meadows = ['Havneby Nord','Havneby Syd','Koldby','Ballum','Jordsand','Rickelsbühl','Hindeburgdam','Morsum','Keitum','Kampen','Königshafen']
#shapes = [sg_havn,sg_havs,sg_kold,sg_ball,sg_jord,sg_rick,sg_hind,sg_mors,sg_keit,sg_kamp,sg_koen]

meadows = ['Hindeburgdam','Morsum','Keitum','Kampen','Königshafen']
shapes = [sg_hind,sg_mors,sg_keit,sg_kamp,sg_koen]


for meadow, shape in zip(meadows,shapes):
    iin = []
    for i in range(0,len(x_face)):
        if any(shape.contains(Point(x_face[i],y_face[i]))):
            iin.append(i)
#####################################################################
    for year in range(2010,2016):
        run = rname+'_'+ str(year)
        files_sorted = sort_files(in_path+run+'/outputs')
        if year==2010:
            [nsav,tmph,tsecs] = read_data(['ICM_nsav','ICM_hcansav','time'],files_sorted,face=iin)
            #tmph = read_data('ICM_hcansav',files_sorted,face=iin)
            nsav[:,np.max(tmph,0)==0]=np.nan
        else:
            [tmp,tmph,tmpt] = read_data(['ICM_nsav','ICM_hcansav','time'],files_sorted,face=iin)
            #tmph = read_data('ICM_hcansav',files_sorted,face=iin)
            tmp[:,np.max(tmph,0)==0]=np.nan
            nsav = np.append(nsav,tmp,0)
            tsecs = np.append(tsecs,tmpt)
    print(np.shape(nsav))

    #load sim data
#    for year in range(2010,2016):
#        run = rname+'_'+ str(year)
#        files_sorted = sort_files(in_path+run+'/outputs')
#        if year==2010:
#            tsecs = read_data('time',files_sorted)
#        else:
#            tmp = read_data('time',files_sorted)
#            tsecs = np.append(tsecs,tmp)
    
    sim_tu = ncdata.variables['time'].units
    sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')

    times = [sim_basedate + timedelta(seconds= s) for s in tsecs]
    months = [t.month for t in times]
    np.shape(months)

    month=range(1,13)
    nsav_all = []
    for m in month:
        nsav_m = nsav[np.array(months)==m,:]
        nsav_m = nsav_m.flatten()
        nsav_m = nsav_m[~np.isnan(nsav_m)]
        nsav_all.append(nsav_m)

    obspath = '/work/gg0877/g260204/data/01_observations/sg/'
    #load and plot observations
    #load observations
    fname=obspath+'2021-2023_Seegrassprosse_Sylt_Zusammenfassung_Veronika_Mohr.xlsx'
    data= pd.read_excel(fname)
    data['months']=pd.DatetimeIndex(data['Datum']).month
    data['density']=data['Station'].str.split(",",expand=True)[1].str.split(" ",expand=True)[1]

    dens = ['dichte','dünne']
    obs_mean = np.zeros([12,2])
    obs_min = np.zeros([12,2])
    obs_max = np.zeros([12,2])
    for m in months:
        tmp=data[data['months']==m]
        for d in range(0,2):
            tmpd = tmp[tmp['density']==dens[d]]
            obs_mean[m-1,d] = tmpd['Sprossdichte Zostera noltei pro m2'].mean()
            obs_min[m-1,d] = tmpd['Sprossdichte Zostera noltei pro m2'].min()
            obs_max[m-1,d] = tmpd['Sprossdichte Zostera noltei pro m2'].max()
    
    month=range(1,13)

    fig, ax = plt.subplots(figsize=(4,4))
    #plot sim:
    ax.boxplot(nsav_all,0,'') 

    #plot obs:
    ax.fill_between(month, obs_max[:,1], obs_min[:,1],alpha=0.2,color='cadetblue',zorder=0)
    ax.plot(month,obs_mean[:,1],color='cadetblue',zorder=1,linewidth=1,linestyle='--')
    ax.fill_between(month, obs_max[:,0], obs_min[:,0],alpha=0.2,color='darkseagreen',zorder=0)
    ax.plot(month,obs_mean[:,0],color='darkseagreen',zorder=1,linewidth=1,linestyle='--')

    ax.set_ylabel('density [shoots/m²]')
    ax.set_xlabel('month of the year')
    ax.set_title(meadow)
    ax.yaxis.get_major_formatter().set_useMathText('true')
    ax.yaxis.get_major_formatter().set_powerlimits((3,3))

    plt.tight_layout()
    plt.savefig(plotpath + 'nsav_simobs_'+meadow+'.png')
