#read variable from multiple schout files and concat
#input: 
#   varname  : name of variable in schout file
#   ncf_all  : list of schout_files
# optional:
#   node     : index of node to read data from
#   vlayer   : index of layer to read data from
#   face     : index of face to read data from
#   ntime    : index of timestep to read data from, as range
#output:
#   vardata  : array of variable data
from netCDF4 import Dataset
import numpy as np

def read_data(varname, ncf_all,*,node="",vlayer="",face="",ntime=""):
    #get metadata info using first netcdf file
    ncf= ncf_all[0]
    nc = Dataset(ncf)
    dims = nc[varname].dimensions
    size = []
    #get size of dimensions
    for d in dims:
        size.append(nc.dimensions[d].size)
    #list of ranges to read from ncfile
    ids_list = [range(0,s) for s in size]

    #slicing
    if node:
        id_node = dims.index('nSCHISM_hgrid_node')
        if type(node)== int:
            size[id_node] = 1
        else:
            size[id_node] = len(node) # squeeze removes dimensions with size 1
        ids_list[id_node] = node
    if vlayer:
        id_layer = dims.index('nSCHISM_vgrid_layers')
        size[id_layer] = 1# squeeze removes dimentison with size 1 
        ids_list[id_layer] = vlayer
    if face:
        id_face=dims.index('nSCHISM_hgrid_face')
        if type(face) == int:
            size[id_face] = 1
        else:
            size[id_face] = len(face) # squeeze removes dimensions with size 1
        ids_list[id_face] = face
    if ntime:
        id_time= dims.index('time')
        ids_list[id_time] = ntime
    
    #create empty array without time dimension
    size[dims.index('time')] = 0
    vardata = np.empty(size).squeeze()

    #loop over files to get data
    i = 0
    for ncf in ncf_all:
        nc = Dataset(ncf,'r')
        vardata = np.concatenate([vardata,nc[varname][ids_list]],0)
        i+=1
        if i%50 == 0:
            print(ncf)
    return vardata

