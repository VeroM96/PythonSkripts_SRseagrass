#read multiple variables from multiple schout files and concat
#[vardata1,[vardata2,...]] = read_data([varname1,[varname2],...],ncf_all,[optional input])
#input: 
#   varname  : name of variable in schout file
#              can be multiple variables. variable has to be list.
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
from tqdm import tqdm

def read_data(varname, ncf_all,*,node="",vlayer="",face="",ntime=""):

    if type(varname)==str:
        varname = [varname]
    #get metadata info using first netcdf file
    ncf= ncf_all[0]
    nc = Dataset(ncf)
    ids_all = []
    size_all = []
    vardata = []
    for i in range(0,len(varname)):
        dims = nc[varname[i]].dimensions
        size = []
        #get size of dimensions
        for d in dims:
            size.append(nc.dimensions[d].size)
        #list of ranges to read from ncfile
        ids_list = [range(0,s) for s in size]

        #slicing
        if node:
            if 'nSCHISM_hgrid_node' in dims:
                id_node = dims.index('nSCHISM_hgrid_node')
                if type(node)== int:
                    size[id_node] = 1
                else:
                    size[id_node] = len(node) # squeeze removes dimensions with size 1
                ids_list[id_node] = node
        if vlayer:
            if 'nSCHISM_vgrid_layers' in dims:
                id_layer = dims.index('nSCHISM_vgrid_layers')
                size[id_layer] = 1# squeeze removes dimentison with size 1 
                ids_list[id_layer] = vlayer
        if face:
            if 'nSCHISM_hgrid_face' in dims:
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

        size_all.append([0])
        ids_all.append(ids_list)
        vardata.append(np.empty(size).squeeze())

    #loop over files to get data
    for ncf in tqdm(ncf_all,desc="Loading files ("+ncf_all[0].split('/')[-3]+", "+ varname[0]+")"):
        nc = Dataset(ncf,'r')
        for v in range(0,len(varname)):
            vardata[v] = np.concatenate([vardata[v],nc[varname[v]][ids_all[v]]],0)
    if len(varname)==1:
        vardata= vardata[0]

    return vardata

