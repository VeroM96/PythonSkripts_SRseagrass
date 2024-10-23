import netCDF4
from netCDF4 import Dataset
from datetime import datetime, timedelta
from pandas import DataFrame
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.tri as tri

import matplotlib as mpl
mpl.use('Agg')

import math
import glob
import h5py
import os.path

#https://github.com/PeterRochford/SkillMetrics
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SkillMetrics/')
import skill_metrics as sm

def plot_elev_multi(spat,rname_all,labels,plot_path, grid, obspath,shifts):
    #figures for plotting
    fig1 = plt.figure(figsize=(10,8))
    fig2 = plt.figure(figsize=(10,8))
    fig3 = plt.figure(figsize=(10,8))
    fig4 = plt.figure(figsize=(10,8))
    ax1=fig1.add_subplot(111)
    ax2=fig2.add_subplot(111)
    ax3=fig3.add_subplot(111)
    ax4=fig4.add_subplot(111)

    figtay = plt.figure(figsize=(10,8))
    axtay=figtay.add_subplot(111)
    cols = ['r','b','g','m','c','y']
    labeldict=dict()
    pegnames =  ['LIS','HAV','VIS','BAS']
    h5pypath = '/work/gg0877/g260204/data/pickle_files/'
    
    for i in range(0,len(rname_all)):
        #choose right points
        timeshift = shifts[i]
 

        match grid[i]:
            case 'sr100':
                points = [27906, 39222, 44444, 48718] #grid SyltRomo 100
            case 'sr50':
                points = [13563, 12914, 8840, 12671] #grid SyltRomo 50
            case 'sr200':
                points = [1749, 2752, 1305, 1379] #grid SyltRomo 200
            case _:
                print('Error: grid not in list')


        #define paths
        rname = rname_all[i]
        ncpat = spat + rname + '/outputs'
        h5name = h5pypath + 'taylor_' + rname + '_' + str(shifts[i]) + '.hdf5'
        print('read station files:',rname)
        #order in station files: time [LIS HAV VIS BAS]
        data = np.loadtxt(ncpat + '/staout_1')
        #initialize empty arrays
        tsecs = data[:,0]
        elev = data[:,1:]
        #for taylor
        stds_obs =[]
        stds =[]
        rmss = []
        cors = []
        label = []

        ncdata = Dataset(ncpat + '/schout_1.nc')


        sim_tu = ncdata.variables['time'].units
        sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')
        year = sim_basedate.year

        times = [sim_basedate + timedelta(hours=timeshift[0], minutes=timeshift[1]) + timedelta(seconds= s) for s in tsecs]
    
        sim = pd.DataFrame(data=elev,columns=pegnames,index=times)

        #print(sim)
    
        both = sim
        #load obs data
        for peg in pegnames:
            obsncf = obspath + peg +  '/wl_' + peg + '_' + str(year) + '.nc'
            #print(obsncf)
            obsdata = Dataset(obsncf,mode='r')
            obssecs = obsdata.variables['time'][:]
            obswl = obsdata.variables['wl'][:]/100
            obs_tu = obsdata.variables['time'].units
            obs_basedate = datetime.strptime(obs_tu.split()[2]+obs_tu.split()[3],'%Y-%m-%d%H:%M:%S')

            obs_times = [obs_basedate + timedelta(seconds=int(s)) for s in obssecs]

            obs = pd.DataFrame({'obs '+peg:obswl},index=obs_times)
            #print(obs)
            both = pd.merge(both,obs,left_index=True,right_index=True)
        #print(both)

        both =  both.dropna()
        taylor = pd.DataFrame(columns=["stds_obs","bias","rmse","stds","rmss","cors"],index=pegnames)
        for peg in pegnames:
            both['diff ' + peg] = both[peg] - both['obs ' + peg]
            taylor.at[peg,'bias']=both[peg].mean() - both['obs ' + peg].mean()
            taylor.at[peg,'rmse']=(both['diff ' + peg]**2).mean() **.5

            stats = sm.taylor_statistics(both[peg],both['obs ' + peg],'data')
            taylor.at[peg,'stds']=stats['sdev'][1]
            taylor.at[peg,'rmss']=stats['crmsd'][1]
            taylor.at[peg,'cors']=stats['ccoef'][1]
            taylor.at[peg,'stds_obs']= stats['sdev'][0]
    
        df2 = pd.DataFrame({'stds':stats['sdev'][0],'rmss':stats['crmsd'][0],'cors':stats['ccoef'][0]},index=['obs'])
        taylor= df2._append(taylor)
        #save to hdf5 file
        taylor.to_hdf(h5name,key='taylor',mode='w')
        both.to_hdf(h5name,key='both')

        print(both)
        print(taylor)
        
        #plotting
        ax1.plot(both[pegnames[0]],color=cols[i],label=labels[i])
        ax2.plot(both[pegnames[1]],color=cols[i],label=labels[i])
        ax3.plot(both[pegnames[2]],color=cols[i],label=labels[i])
        ax4.plot(both[pegnames[3]],color=cols[i],label=labels[i])
        if i == len(rname_all)-1:
            ax1.plot(both['obs ' + pegnames[0]],'--k',label='obs')
            ax2.plot(both['obs ' + pegnames[1]],'--k',label='obs')
            ax3.plot(both['obs ' + pegnames[2]],'--k',label='obs')
            ax4.plot(both['obs ' + pegnames[3]],'--k',label='obs')
        
        print(taylor['cors'].to_numpy(dtype=np.float32))
        print(np.arccos(taylor['cors'].to_numpy(dtype=np.float32)))
        plt.figure(figtay)
        if i == 0:
            sm.taylor_diagram(taylor['stds'].to_numpy(),
                    taylor['rmss'].to_numpy(),
                    taylor['cors'].to_numpy(dtype=np.float32),
                    markercolor=cols[i],markerLabel=list(taylor.index.values))
            labeldict.update({labels[i]:cols[i]})
            print(labeldict)
        elif i == len(rname_all)-1:
            labeldict.update({labels[i]:cols[i]})
            print(labeldict)
            sm.taylor_diagram(taylor['stds'].to_numpy(),
                    taylor['rmss'].to_numpy(),
                    taylor['cors'].to_numpy(dtype=np.float32),
                    markercolor=cols[i],overlay='on',markerLabel=labeldict)
        else:
            labeldict.update({labels[i]:cols[i]})
            sm.taylor_diagram(taylor['stds'].to_numpy(),
                    taylor['rmss'].to_numpy(),
                    taylor['cors'].to_numpy(dtype=np.float32)
                    ,markercolor=cols[i],overlay='on',markerLabel=list(taylor.index.values))
        
    name1 = plot_path + 'elev' + '_'+pegnames[0] 
    name2 = plot_path + 'elev' + '_'+pegnames[1]
    name3 = plot_path + 'elev' + '_'+pegnames[2] 
    name4 = plot_path + 'elev' + '_'+pegnames[3] 
    nametay = plot_path + 'taylor.png'

    dsta=datetime(2014,9,1)
    dend=datetime(2014,9,7)

    
    ax1.set_xlabel('time')
    ax1.set_ylabel('elevation [m]')
    ax1.set_title('wl at ' +pegnames[0]+ ' gauge station [m]')
    ax1.legend(loc='upper right')
    fig1.savefig(name1+'.png')
    ax1.set_xlim([dsta,dend])
    fig1.savefig(name1+'_7d.png')


    ax2.set_xlabel('time')
    ax2.set_ylabel('elevation [m]')
    ax2.set_title('wl at ' +pegnames[1]+ ' gauge station [m]')
    ax2.legend(loc='upper right')
    fig2.savefig(name2+'.png')
    ax2.set_xlim([dsta,dend])
    fig2.savefig(name2+'_7d.png')


    ax3.set_xlabel('time')
    ax3.set_ylabel('elevation [m]')
    ax3.set_title('wl at ' +pegnames[2]+ ' gauge station [m]')
    ax3.legend(loc='upper right')
    fig3.savefig(name3+'.png')
    ax3.set_xlim([dsta,dend])
    fig3.savefig(name3+'_7d.png')

    
    ax4.set_xlabel('time')
    ax4.set_ylabel('elevation [m]')
    ax4.set_title('wl at ' +pegnames[3]+ ' gauge station [m]')
    ax4.legend(loc='upper right')
    fig4.savefig(name4+'.png')
    ax4.set_xlim([dsta,dend])
    fig4.savefig(name4+'_7d.png')



    figtay.savefig(nametay)


