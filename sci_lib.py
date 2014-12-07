#!/usr/bin/python
#Author: Scott T. Salesky
#Created: 12.6.2014
#Purpose: Collection of useful Python classes,
#routines, and functions for scientific work
#----------------------------------------------

#Import all required packages
import numpy as np
from matplotlib.colors import Normalize

def read_f90_bin(path,nx,ny,nz,precision):
    
    """Reads Fortran binary direct access files into Numpy.
    
    path        => path to file to read
    (nx,ny,nz)  => grid dimensions
    precison    => (=4 single), (=8 double)
    Returns dat[nx,ny,nz] as numpy array.
    """    
    
    #Open file
    f=open(path,'rb')
    
    #Pass data to numpy array
    if (precision==4):
        dat=np.fromfile(f,dtype='float32',count=nx*ny*nz)
    elif (precision==8):
		dat=np.fromfile(f,dtype='float64',count=nx*ny*nz)
    else:
        raise ValueError('Precision must be 4 or 8')
    
    #Reshape array
    dat=np.reshape(dat,(nx,ny,nz),order='F')
    f.close()
    return dat
    
class MidPointNormalize(Normalize):
    """Defines the midpoint of diverging colormap.
    
    Usage: Allows one to adjust the colorbar, e.g. 
    using contouf to plot data in the range [-3,6] with
    a diverging colormap so that zero values are still white.
    Example usage:
        norm=MidPointNormalize(midpoint=0.0)
        f=plt.contourf(X,Y,dat,norm=norm,cmap=colormap)
     """
     
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
