
import os.path
from plot_elev_obs_norm_multi import plot_elev_multi
from plot_temp_obs_multi import plot_temp_multi
import shutil
#from plot_hyps import plot_hyp
#from plot_morph import plot_morph
#from plot_hyps_dev import plot_hyps_dev
#from old_hcan.plot_hsav import plot_hsav

##main for defining paths and evironment vars
#plotname = "comp_h0", rname= ["sr007","sr011"],labels=["h0=0.01m","h0=0.1m"],grid = ["sr100","sr100"]
plotname = "srm024"
rname= ["srm024_2010","srm024_2011","srm024_2012","srm024_2013","srm024_2014","srm024_2015"]
labels=["2010","2011","2012","2013","2014","2015"]
grid = ["sr100","sr100","sr100","sr100","sr100","sr100"]
last = "365"
mspeed = 1;
obspath = '/work/gg0877/g260204/data/01_observations/wl/'
obspathtemp = '/work/gg0877/g260204/data/01_observations/t/'
#points = [27906, 39222, 44444, 48718] #grid SyltRomo 100
#points = [13563, 12914, 8840, 12671] #grid SyltRomo 50
#points = [1749, 2752, 1305, 1379] #grid SyltRomo 200
shift = [[+1,20],[+1,20],[+1,20],[1,20],[1,20],[+1,30]]

schout_path = "/work/gg0877/g260204/sim_data/SR5yr/"
plot_path = "/work/gg0877/g260204/sim_data/SR5yr/plots/plots/" + plotname +'/'

for r in rname:
    if not os.path.exists(schout_path + r):
        print('input folder does not exist')
if not os.path.exists(plot_path):
    os.makedirs(plot_path)

shutil.copy('multiplot_all.py',plot_path + 'multiplot_all.txt')

plot_elev_multi(schout_path,rname,labels,plot_path, grid, obspath,shift) #plot water elevationa
#plot_temp_multi(schout_path,rname,labels,plot_path, grid, obspathtemp) #plot water elevation.

#plot_hyp(schout_path,rname,plot_path, last,mspeed) #plot hypsometry at last time step
#plot_morph(schout_path,rname,plot_path,last,mspeed) #plot morphology at last time step
#plot_hyps_dev(schout_path,rname,plot_path,mspeed) #plot development of mean depth
#plot_hsav(schout_path,rname,plot_path,last,mspeed) # plot sav hight at last time step

