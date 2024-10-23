
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


from matplotlib import rcParams
rcParams['figure.dpi'] = 300


#https://github.com/PeterRochford/SkillMetrics
import sys
sys.path.insert(0, '/home/g/g260204/tools/python_skripts/SkillMetrics/')
import skill_metrics as sm


def plot_elev(spat,rname_all,plot_path, points,shift):
    #points = [27906, 39222, 44444, 48718]
    pegnames = ['LIS','HAV','VIS','BAS']
    obspath = '/work/gg0877/g260204/data/01_observations/wl/'
    timeshift = shift[0]
    tsmins = shift[1] #!has to be 0 if outputsteps are 1h!
    ncpat = spat + rname_all[0] + '/outputs'

    #order in station files: time [LIS HAV VIS BAS]
    data = np.loadtxt(ncpat + '/staout_1')
    tsecs = data[:,0]
    rname = rname_all[0]
    #for taylor
    stds =[]
    rmss = []
    cors = []
    label = []

    for i in range(0,len(points)):
        elev = data[:,i+1]
        ncdata = Dataset(ncpat + '/schout_1.nc')

        sim_tu = ncdata.variables['time'].units
        sim_basedate = datetime.strptime(sim_tu.split()[2]+sim_tu.split()[3],'%Y-%m-%d%H:%M:%S')
        year = sim_basedate.year
    
        times = [sim_basedate + timedelta(hours=timeshift, minutes=tsmins) + timedelta(seconds= s) for s in tsecs]
        
        sim = pd.DataFrame({'sim':elev},index=times)
        #load obs data
        obsncf = obspath + pegnames[i] +  '/wl_' + pegnames[i] + '_' + str(year) + '.nc'
        print(obsncf)
        obsdata = Dataset(obsncf,mode='r')
        obssecs = obsdata.variables['time'][:]
        obswl = obsdata.variables['wl'][:]/100
        obs_tu = obsdata.variables['time'].units
        obs_basedate = datetime.strptime(obs_tu.split()[2]+obs_tu.split()[3],'%Y-%m-%d%H:%M:%S')
        
        obs_times = [obs_basedate + timedelta(seconds=int(s)) for s in obssecs]
        
        obs = pd.DataFrame({'obs':obswl},index=obs_times)
          #analysis
        both = pd.merge(sim,obs,left_index=True,right_index=True)
        both =both.dropna()
        #mask = (both.index >= datetime(year,4,1)) & (both.index <= datetime(year,11,1))
        #both = both.loc[mask]
        diff = both.obs - both.sim
        bias = both.obs.mean() - both.sim.mean()
        rmse = ((both.obs - both.sim)**2).mean() ** .5
           #plot
        fig = plt.figure(figsize=(8,4))
        ax=fig.add_subplot(111)
        name     = plot_path + 'elev_' + rname + '_' + pegnames[i]+ '.png'

        #obs.plot(ax=ax, label='Observation',color='b')
        #sim.plot(ax=ax, label='Simulation',color='r')
        plt.plot(times,elev,label='Simulation',color='r')
        plt.plot(obs_times,obswl,label='Observation',color='b')
        plt.plot(diff.index,diff.values,'--k',label='Difference')
        ax.text(0.05, 0.93,'rmse = '+ str(round(rmse,5)) + ' m', transform=ax.transAxes,fontsize=16)
        ax.text(0.05, 0.83,'bias = '+ str(round(bias,5)) + ' m', transform=ax.transAxes,fontsize=16)

        ax.set_xlabel('time',fontsize=16)
        ax.set_ylabel('elevation [m]',fontsize=16)
        ax.set_title('wl at ' +obsdata.LongName+ ' gauge station [m]',fontsize=16)
        ax.legend(loc='upper right',fontsize=16)
        ax.tick_params(axis='both',which='major',labelsize=15)
        plt.xlim([datetime(year,1,1),datetime(year+1,1,1)])
        fig.tight_layout()


        plt.savefig(name)
        strshift = str(shift[0])+':'+str(shift[1])
        
        dsta=datetime(year,1,1)
        dend=datetime(year,2,1)
        name     = plot_path + 'elev_' +strshift + '_'+ rname + '_' + pegnames[i]+ '_01.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,1,1)
        dend=datetime(year,4,1)
        name     = plot_path + 'elev_' +strshift + '_'+ rname + '_' + pegnames[i]+ '_1-3.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,2,1) 
        dend=datetime(year,3,1)
        name     = plot_path + 'elev_' +strshift + '_' + rname + '_' + pegnames[i]+ '_02.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,6,1)
        dend=datetime(year,7,1)
        name     = plot_path + 'elev_' +strshift + '_' + rname + '_' + pegnames[i]+ '_06.png'
        plt.xlim([dsta,dend])
        plt.savefig(name)

        dsta=datetime(year,12,1)
        dend=datetime(year+1,1,1)
        name     = plot_path + 'elev_'  +strshift + '_'+ rname + '_' + pegnames[i]+ '_12.png'
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

    print(stds)
    print(rmss)
    print(cors)

    #Taylor
    name = plot_path + 'elev_' + rname + '_taylor.png'
    fig = plt.figure(figsize=(8,5))
    sm.taylor_diagram(np.array(stds),np.array(rmss),np.array(cors),markerLabel=label)

    plt.savefig(name)


