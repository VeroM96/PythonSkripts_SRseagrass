#find highwater and lowwater in time series
#input:
#   elev: timeseries of water elevation
#   dt  : timestep of elev in minutes
#output:
#   df  : pandas dataset with entries 'data'(elevation time series), 'lw' (list of low water, 'hw' (list of high water)
#   fig : figure to check if hw,lw are found correctly  
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import pandas as pd
import numpy as np


def find_hwlw(elev,dt,figure=True): 
  #number of points to be checked before and after (~9h)
  n = int(560/dt) #input dt has to be in minutes

  df = pd.DataFrame(elev,columns=['data'])
  #find local peaks:
  df['lw'] = df.iloc[argrelextrema(df.data.values, np.less_equal,order=n)[0]]['data']
  df['hw'] = df.iloc[argrelextrema(df.data.values, np.greater_equal,order=n)[0]]['data']

  #plot results
  if figure:
      fig = plt.figure(figsize=(40,8))
      plt.scatter(df.index, df['lw'], c='r')
      plt.scatter(df.index, df['hw'], c='g')
      plt.plot(df.index, df['data'])
      return df, fig
  else:
      return df
