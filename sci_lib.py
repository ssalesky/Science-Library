#!/usr/bin/python
#Author: Scott T. Salesky
#Email: scott.salesky@ubc.ca / stsalesky@gmail.com
#Created: 12.6.2014 / Updated: 12.6.2014
#Purpose: Collection of useful Python classes,
#routines, and functions for scientific work
#----------------------------------------------------------
#This is free software released into the public domain.
#Anyone is free to copy, modify, publish, use, compile, sell, or
#distribute this software, either in source code form or as a compiled
#binary, for any purpose, commercial or non-commercial, and by any
#means.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.
#----------------------------------------------------------

#Import all required packages
import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

#----------------------------------------------------------    
#Functions for reading/manipulating data
#----------------------------------------------------------

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
    
#----------------------------------------------------------    
#Classes and functions for generating plots with Matplotlib
#----------------------------------------------------------

def gen_colorlist(n,cmap):
    """Returns list of n colors evenly spaced from a given colormap.

    Useful for making a line plot with n lines with colors that are
    evenly spaced according to a given colormap.
        n       => number of colors to return
        cmap    => colormap (e.g. from pyplot.cm.colormapname)
        returns colorlist   => n tuples corresponding to colors
    
    Example Usage: 
        colorlist=gen_colorlist(ncolors,colormapname)
        for i in range(n):
            plt.plot(data[:,0],dat[:,i+1],color=colorlist[i],args*)    
    """
    
    colorlist=[]
    vals=np.linspace(1.0/n,1.0,n)
    for i in range(n):
        colorlist.append(cmap(vals[i]))
    return colorlist
    
    
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
        