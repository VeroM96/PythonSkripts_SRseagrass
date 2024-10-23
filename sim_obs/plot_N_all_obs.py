
import netCDF4
from netCDF4 import Dataset
from datetime import datetime, timedelta
from pandas import DataFrame
import pandas as pd
import h5py
import h5py

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.tri as tri
from matplotlib import rcParams
rcParams['figure.dpi'] = 300

import matplotlib as mpl
mpl.use('Agg')

import math
import glob

import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SchismUtils/')
from schism_utils import sort_files, read_data

#https://github.com/PeterRochford/SkillMetrics
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SkillMetrics/')
import skill_metrics as sm


def plot_n(spat,rname_all,plot_path, points):
    #points = [27906, 39222, 44444, 48718]
    pegnames_sim = ["KT","KH","KP","MS","HD","RB","KB","HB"]
    pegnames_obs = ['KT_dicht','KT_duenn']
    obspath = '/work/gg0877/g260204/data/01_observations/sg/'

    rname = rname_all[0]
    ncpat = spat + rname + '/outputs'
    #read time & water elevation at 3 stations in basin
    tsecs   = []

    files_sorted = sort_files(ncpat)
    #base data
    ncdata      = Dataset(files_sorted[0], mode='r')
    sim_tu = ncdata.variables['time'].units
    sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')

    #load sim data
    tsecs = read_data('time',files_sorted)
    times = [sim_basedate + timedelta(seconds= s) for s in tsecs]
    months = [t.month for t in times]

    fig = plt.figure(figsize=(6,4))
    name     = plot_path + 'sgn_' + rname + '.png'

    nsav_month = np.zeros(12)
    #save monthly nsav
    hdf5file = '/work/gg0877/g260204/data/pickle_files/' +rname + 'nsav_month.hdf5'
    f = h5py.File(hdf5file,"w")
    
    nsav = read_data('ICM_nsav',files_sorted,face=points)
    for p in range(0,len(points)):
        tmp = nsav[:,p]
        for i in range(1,13):
            nsav_month[i-1] = np.mean(tmp[np.where(np.array(months)==i)])
        f.create_dataset("nsav_"+pegnames_sim[p],data=nsav_month,dtype='f')
        plt.plot(range(1,13),nsav_month,label=pegnames_sim[p])
    f.close()

    #load and plot observations
    #load observations
    fname=obspath+'2021-2023_Seegrassprosse_Sylt_Zusammenfassung_Veronika_Mohr.xlsx'
    data= pd.read_excel(fname)
    data['months']=pd.DatetimeIndex(data['Datum']).month
    data['density']=data['Station'].str.split(",",expand=True)[1].str.split(" ",expand=True)[1]

    months=range(1,13)
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

    #plot obs:
    plt.fill_between(months, obs_max[:,1], obs_min[:,1],alpha=0.2,color='cadetblue',zorder=0)
    plt.plot(months,obs_mean[:,1],color='cadetblue',zorder=1,linewidth=1,linestyle='--')
    plt.fill_between(months, obs_max[:,0], obs_min[:,0],alpha=0.2,color='darkseagreen',zorder=0)
    plt.plot(months,obs_mean[:,0],color='darkseagreen',zorder=1,linewidth=1,linestyle='--')


    plt.legend()
    plt.ylabel('density [shoots/m2]')
    plt.xlabel('month of the year')
    plt.legend(bbox_to_anchor=(1.07, 1))
    plt.tight_layout()
    plt.savefig(name)
    

#        #load sim data
#        for ncf in files_sorted:
#            ncdata      = Dataset(ncf, mode='r')
#            #print(ncf)
#            time    = ncdata.variables['time'][:]
#            tsecs    = np.concatenate([tsecs, time])
#            elev    = np.concatenate([elev, ncdata.variables['elev'][:,points[i]-1]]) #
#        sim_tu = ncdata.variables['time'].units
#        sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')
#        year = sim_basedate.year
#   times = [sim_basedate + timedelta(hours=timeshift, minutes=tsmins) + timedelta(seconds= s) for s in tsecs] 
#        times = [sim_basedate + timedelta(hours=timeshift, minutes=tsmins) + timedelta(seconds= s) for s in tsecs]
#        
#        sim = pd.DataFrame({'sim':elev},index=times)
#        #load obs data
#        obsncf = obspath + pegnames[i] +  '/wl_' + pegnames[i] + '_' + str(year) + '.nc'
#        print(obsncf)
#        obsdata = Dataset(obsncf,mode='r')
#        obssecs = obsdata.variables['time'][:]
#        obswl = obsdata.variables['wl'][:]/100
#        obs_tu = obsdata.variables['time'].units
#        obs_basedate = datetime.strptime(obs_tu.split()[2]+obs_tu.split()[3],'%Y-%m-%d%H:%M:%S')
#        
#        obs_times = [obs_basedate + timedelta(seconds=int(s)) for s in obssecs]
#        
#        obs = pd.DataFrame({'obs':obswl},index=obs_times)
#          #analysis
#        both = pd.merge(sim,obs,left_index=True,right_index=True)
#        both =  both.dropna()
#        diff = both.obs - both.sim
#        bias = both.obs.mean() - both.sim.mean()
#        rmse = ((both.obs - both.sim)**2).mean() ** .5
#           #plot
#        fig = plt.figure(figsize=(10,8))
#        ax=fig.add_subplot(111)
#        name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '.png'
#
#        #obs.plot(ax=ax, label='Observation',color='b')
#        #sim.plot(ax=ax, label='Simulation',color='r')
 #       plt.plot(times,elev,label='Simulation',color='r')
#        plt.plot(obs_times,obswl,label='Observation',color='b')
#        plt.plot(diff.index,diff.values,'--k',label='Difference')
#        ax.text(0.05, 0.95,'rmse = '+ str(round(rmse,5)) + ' m', transform=ax.transAxes)
#        ax.text(0.05, 0.90,'bias = '+ str(round(bias,5)) + ' m', transform=ax.transAxes)
#
#        ax.set_xlabel('time')
#        ax.set_ylabel('elevation [m]')
#        ax.set_title('wl at ' +obsdata.LongName+ ' gauge station [m]')
#        ax.legend(loc='upper right')
#
#        plt.savefig(name)
#        
#        dsta=datetime(2014,1,1)
#        dend=datetime(2014,2,1)
#        name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '_01.png'
#        plt.xlim([dsta,dend])
#        plt.savefig(name)
##

 #       dsta=datetime(2014,2,1) 
 #       dend=datetime(2014,3,1)
#        name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '_02.png'
#        plt.xlim([dsta,dend])
#        plt.savefig(name)

 #       dsta=datetime(2014,6,1)
 #       dend=datetime(2014,7,1)
 #       name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '_06.png'
 #       plt.xlim([dsta,dend])
 #       plt.savefig(name)
#
#        dsta=datetime(2014,12,1)
#        dend=datetime(2015,1,1)
#        name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '_12.png'
#        plt.xlim([dsta,dend])
#        plt.savefig(name)
#
#        plt.close()
#
#        #Taylor Diagramm
#        #https://github.com/PeterRochford/SkillMetrics
#        
#
#        stats = sm.taylor_statistics(both.sim,both.obs,'data')
#        if i ==0 :
#            stds.append(stats['sdev'][0])
#            rmss.append(stats['crmsd'][0])
 #           cors.append(stats['ccoef'][0])
#            label.append('obs')
#
#        stds.append(stats['sdev'][1])
#        rmss.append(stats['crmsd'][1])
#        cors.append(stats['ccoef'][1])
#        label.append(pegnames[i])
#
#
#
#        del time, tsecs, elev, sim_tu, times
#    
#    print(stds)
#    print(rmss)
#    print(cors)
#
#    #Taylor
#    name = plot_path + 'elev_' + rname + '_taylor.png'
#    fig = plt.figure(figsize=(10,8))
#    sm.taylor_diagram(np.array(stds),np.array(rmss),np.array(cors),markerLabel=label)
#
#    plt.savefig(name)


