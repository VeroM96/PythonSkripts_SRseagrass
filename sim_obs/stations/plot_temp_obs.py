
import netCDF4
from netCDF4 import Dataset
from datetime import datetime, timedelta
from pandas import DataFrame
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.tri as tri

import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SchismUtils/')
from schism_utils import sort_files, read_data

import matplotlib as mpl
mpl.use('Agg')

import math
import glob

from matplotlib import rcParams
rcParams['figure.dpi'] = 300

#https://github.com/PeterRochford/SkillMetrics
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SkillMetrics/')
import skill_metrics as sm


def plot_temp(spat,rname_all,plot_path, points):
    #points = [27906, 39222, 44444, 48718]
    pegnames = ['HAV']
    obspath = '/work/gg0877/g260204/data/01_observations/t/'
    timeshift = +0
    tsmins = +0 #!has to be 0 if outputsteps are 1h!

    rname = rname_all[0]
    ncpat = spat + rname + '/outputs'
    #read time & water elevation at 3 stations in basin
    tsecs    = []
    elev    = []
    elevin  = []
    elevbas = []
    
    #for taylor
    stds =[]
    rmss = []
    cors = []
    label = []


    for i in range(0,len(points)):
        print('read station temp files')
        data = np.loadtxt(ncpat+'/staout_5')
        tsecs    = data[:,0]
        temp    = data[:,2] # only HAV
        elevin  = []
        elevbas = []

        #load sim data
        ncdata = Dataset(ncpat + '/schout_1.nc')
        sim_tu = ncdata.variables['time'].units
        sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')
        year = sim_basedate.year
    
        times = [sim_basedate + timedelta(hours=timeshift, minutes=tsmins) + timedelta(seconds= s) for s in tsecs]
        
        sim = pd.DataFrame({'sim':temp},index=times)
        #load obs data
        obsncf = obspath + pegnames[i] +  '/t_' + pegnames[i] + '_' + str(year) + '.nc'
        print(obsncf)
        obsdata = Dataset(obsncf,mode='r')
        obssecs = obsdata.variables['time'][:]
        obst = obsdata.variables['t'][:]
        obs_tu = obsdata.variables['time'].units
        obs_basedate = datetime.strptime(obs_tu.split()[2]+obs_tu.split()[3],'%Y-%m-%d%H:%M:%S')
        
        obs_times = [obs_basedate + timedelta(seconds=int(s)) for s in obssecs]
        
        obs = pd.DataFrame({'obs':obst},index=obs_times)
          #analysis
        both = pd.merge(sim,obs,left_index=True,right_index=True)
        both =  both.dropna()
        diff = both.obs - both.sim
        bias = both.obs.mean() - both.sim.mean()
        rmse = ((both.obs - both.sim)**2).mean() ** .5
           #plot
        fig = plt.figure(figsize=(8,4))
        ax=fig.add_subplot(111)
        name     = plot_path + 'temp_' + rname + '_' + pegnames[i]+ '.png'

        #obs.plot(ax=ax, label='Observation',color='b')
        #sim.plot(ax=ax, label='Simulation',color='r')
        plt.plot(times,temp,label='Simulation',color='r')
        plt.plot(obs_times,obst,label='Observation',color='b')
        plt.plot(diff.index,diff.values,'--k',label='Difference')
        ax.text(0.05, 0.93,'rmse = '+ str(round(rmse,5)) + ' degree C', transform=ax.transAxes,fontsize=16)
        ax.text(0.05, 0.83,'bias = '+ str(round(bias,5)) + ' degree C', transform=ax.transAxes,fontsize=16)

        ax.set_xlabel('time',fontsize=16)
        ax.set_ylabel('water temperature [degree C]',fontsize=16)
        ax.set_title('t at ' +obsdata.LongName+ ' gauge station [m]',fontsize=16)
        ax.legend(loc='upper right',fontsize=16)
        ax.tick_params(axis='both',which='major',labelsize=15)
        fig.tight_layout()

        plt.savefig(name)
        
        dsta=datetime(year,1,1)
        dend=datetime(year,2,1)
        name     = plot_path + 'temp_' + rname + '_' + pegnames[i]+ '_01.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)


        dsta=datetime(year,2,1) 
        dend=datetime(year,3,1)
        name     = plot_path + 'temp_' + rname + '_' + pegnames[i]+ '_02.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,6,1)
        dend=datetime(year,7,1)
        name     = plot_path + 'temp_' + rname + '_' + pegnames[i]+ '_06.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,12,1)
        dend=datetime(year,1,1)
        name     = plot_path + 'temp_' + rname + '_' + pegnames[i]+ '_12.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        plt.close()

        #Taylor Diagramm
        #https://github.com/PeterRochford/SkillMetrics
        

        stats = sm.taylor_statistics(both.sim,both.obs,'data')
        if i ==0 :
            stds.append(stats['sdev'][0])
            rmss.append(stats['crmsd'][0])
            cors.append(stats['ccoef'][0])
            label.append('obs')

        stds.append(stats['sdev'][1])
        rmss.append(stats['crmsd'][1])
        cors.append(stats['ccoef'][1])
        label.append(pegnames[i])



        del tsecs, temp, sim_tu, times
    
    print(stds)
    print(rmss)
    print(cors)

    #Taylor
    name = plot_path + 'temp_' + rname + '_taylor.png'
    fig = plt.figure(figsize=(10,8))
    sm.taylor_diagram(np.array(stds),np.array(rmss),np.array(cors),markerLabel=label)

    plt.savefig(name)


