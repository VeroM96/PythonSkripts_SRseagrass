import netCDF4
from netCDF4 import Dataset
from datetime import datetime, timedelta
from pandas import DataFrame
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.tri as tri

import os.path
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SchismUtils/')
from schism_utils import sort_files, read_data

import matplotlib as mpl
mpl.use('Agg')

import math
import glob


#https://github.com/PeterRochford/SkillMetrics
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SkillMetrics/')
import skill_metrics as sm


def plot_temp_multi(spat,rname_all,labels,plot_path, grid, obspath):
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
    pegnames =  ['HAV']
    h5pypath = '/work/gg0877/g260204/data/pickle_files/'

    for i in range(0,len(rname_all)):
        #choose right poinats

        match grid[i]:
            case 'sr100':
                points = [44444] #grid SyltRomo 100
            case 'sr50':
                points = [8840] #grid SyltRomo 50
            case 'sr200':
                points = [1305] #grid SyltRomo 200
            case _:
                print('Error: grid not in list')

        #define paths
        rname = rname_all[i]
        ncpat = spat + rname + '/outputs'
        h5name = h5pypath + 'taylor_temp_' + rname + '.hdf5'
        if os.path.isfile(h5name):
            print('read from file:', h5name)
            taylor = pd.read_hdf(h5name,'taylor')
            both = pd.read_hdf(h5name,'both')
        else:
            print('rad station files',rname)
            data =  np.loadtxt(ncpat + '/staout_5')
            #initialize empty arrays
            tsecs = data[:,0]
            temp = data[:,2]
            #for taylor
            stds =[]
            rmss = []
            cors = []
            label = []

            ncdata = Dataset(ncpat+'/schout_1.nc')

            sim_tu = ncdata.variables['time'].units
            sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')
            year = sim_basedate.year

            times = [sim_basedate + timedelta(hours=1, minutes=0) + timedelta(seconds= s) for s in tsecs]

            sim = pd.DataFrame(data=temp,columns=pegnames,index=times)

            #print(sim)

            both = sim
            #load obs data
            for peg in pegnames:
                obsncf = obspath + peg +  '/t_' + peg + '_' + str(year) + '.nc'
                #print(obsncf)
                obsdata = Dataset(obsncf,mode='r')
                obssecs = obsdata.variables['time'][:]
                obswl = obsdata.variables['t'][:]
                obs_tu = obsdata.variables['time'].units
                obs_basedate = datetime.strptime(obs_tu.split()[2]+obs_tu.split()[3],'%Y-%m-%d%H:%M:%S')

                obs_times = [obs_basedate + timedelta(seconds=int(s)) for s in obssecs]

                obs = pd.DataFrame({'obs '+peg:obswl},index=obs_times)
                #print(obs)
                both = pd.merge(both,obs,left_index=True,right_index=True)
            #print(both)

            both =  both.dropna()
            taylor = pd.DataFrame(columns=["bias","rmse","stds","rmss","cors"],index=pegnames)
            for peg in pegnames:
                both['diff ' + peg] = both[peg] - both['obs ' + peg]
                taylor.at[peg,'bias']=both[peg].mean() - both['obs ' + peg].mean()
                taylor.at[peg,'rmse']=(both['diff ' + peg]**2).mean() **.5

                stats = sm.taylor_statistics(both[peg],both['obs ' + peg],'data')
                taylor.at[peg,'stds']=stats['sdev'][1]
                taylor.at[peg,'rmss']=stats['crmsd'][1]
                taylor.at[peg,'cors']=stats['ccoef'][1]

            df2 = pd.DataFrame({'stds':stats['sdev'][0],'rmss':stats['crmsd'][0],'cors':stats['ccoef'][0]},index=['obs'])
            taylor= df2._append(taylor)
            #save to hdf5 file
            taylor.to_hdf(h5name,key='taylor',mode='w')
            both.to_hdf(h5name,key='both')

        print(both)
        print(taylor)

        #plotting
        ax1.plot(both[pegnames[0]],color=cols[i],label=labels[i])
        #ax2.plot(both[pegnames[1]],color=cols[i],label=labels[i])
        if i == len(rname_all)-1:
            ax1.plot(both['obs ' + pegnames[0]],'--k',label='obs')
           # ax2.plot(both['obs ' + pegnames[1]],'--k',label='obs')

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
            print(rname_all[i],i)
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

    name1 = plot_path + 'temp' + '_'+pegnames[0]
    #name2 = plot_path + 'temp' + '_'+pegnames[1]
    #name3 = plot_path + 'temp' + '_'+pegnames[2]
    #name4 = plot_path + 'temp' + '_'+pegnames[3]
    nametay = plot_path + 'taylor_temp.png'

    dsta=datetime(2014,9,1)
    dend=datetime(2014,9,7)


    ax1.set_xlabel('time')
    ax1.set_ylabel('temperature [°C]')
    ax1.set_title('T at ' +pegnames[0]+ ' gauge station [°C]')
    ax1.legend(loc='upper right')
    fig1.savefig(name1+'.png')
    ax1.set_xlim([dsta,dend])
    fig1.savefig(name1+'_7d.png')


    #ax2.set_xlabel('time')
    #ax2.set_ylabel('temperature [°C]')
    #ax2.set_title('T at ' +pegnames[1]+ ' gauge station [°C]')
    #ax2.legend(loc='upper right')
    #fig2.savefig(name2+'.png')
    #ax2.set_xlim([dsta,dend])
    #fig2.savefig(name2+'_7d.png')


    #ax3.set_xlabel('time')
    #ax3.set_ylabel('temperature [°C]')
    #ax3.set_title('T at ' +pegnames[2]+ ' gauge station [°C]')
    #ax3.legend(loc='upper right')
    #fig3.savefig(name3+'.png')
    #ax3.set_xlim([dsta,dend])
    #fig3.savefig(name3+'_7d.png')


    #ax4.set_xlabel('time')
    #ax4.set_ylabel('temperature [°C]')
    #ax4.set_title('T at ' +pegnames[3]+ ' gauge station [°C]')
    #ax4.legend(loc='upper right')
    #fig4.savefig(name4+'.png')
    #ax4.set_xlim([dsta,dend])
    #fig4.savefig(name4+'_7d.png')



    figtay.savefig(nametay)


