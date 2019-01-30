import pandas as pd
import numpy as np
from copy import deepcopy
def chip_transfer(data,axis=0):
    d=np.nan_to_num(data)
    return np.mean(d,axis=axis)

def meth_transfer(data,axis=0):
    d = deepcopy(data)
    return np.nanmean(d,axis=axis)

def format_gz(filename,snum,mc_marker,hmc_marker,blocks):
    d = pd.read_csv(filename,sep="\t",skiprows=1)
    region_title = d.values[:,:6]
    data = d.values[:,6:].astype(float)
    if not mc_marker:
        m = chip_transfer(data)
    else:
        if hmc_marker:
            hmc = data[:,-1*blocks:]
            mc = data[:,-2*blocks:-1*blocks]
            inputdata = data[:,:-2*blocks]
#            print(hmc.shape,mc.shape,inputdata.shape)
#            print(data[:,-1*blocks:])
            m=[chip_transfer(inputdata),meth_transfer(mc),chip_transfer(hmc)]
            m = np.hstack(m)
        else:
            mc = data[:,-1*blocks:]
            inputdata = data[:,:-1*blocks]
#            print(mc.shape,inputdata.shape)
            m = [chip_transfer(inputdata),meth_transfer(mc)]
            m = np.hstack(m)
    region_mean = []
    for i in range(data.shape[1]//blocks):
        d = data[:,i*blocks:(i+1)*blocks]
        region_mean.append(chip_transfer(d,axis=1).flatten())
    region_mean = np.array(region_mean).T
    #print(region_mean.shape)
    return m.reshape(snum,blocks),region_mean,region_title

def bp_format(filename,snum,blocks):
    d = pd.read_csv(filename,sep="\t",skiprows=1)
    data = d.values[:,6:].astype(float)
    #data = np.nan_to_num(data)
    result=[]
    for i in range(blocks):
        temp=[]
        for j in range(snum):
            arr=[]
            for d in data[:,j*blocks+i]:
               if ~np.isnan(d):
                   arr.append(d)
               #else:
               #    print('nan')
            temp.append(arr)
        result.append(temp)
    #result = np.array(result).reshape(blocks,snum,-1)
    return result





if __name__=="__main__":
    import sys
    filename = sys.argv[1]
