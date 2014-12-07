#!/usr/bin/python
#Author: Scott T. Salesky
#Email: scott.salesky@ubc.ca / stsalesky@gmail.com
#Created: 12.6.2014 / Updated: 12.6.2014
#Purpose: Collection of useful Python classes,
#routines, and functions for scientific work
#----------------------------------------------------------

#Import all required packages
import numpy as np                              #Numpy
from matplotlib.colors import Normalize         #Normalize class
import matplotlib.pyplot as plt                 #Matplotlib.pyplot
from matplotlib.ticker import MultipleLocator, \
     AutoLocator, AutoMinorLocator              #Tick locations
#from matplotlib import ticker                   #Ticker

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

def set_ticks(ax,xmaj=None,xmin=None,ymaj=None,ymin=None):
    """Sets major/minor axis tickmarks at specified increments.
    
    ax          => Axis handle (e.g. ax=plt.subplot(111))
    xmaj,ymaj   => Major tick frequency (optional)
    xmin,ymin   => Minor tick frequency (optional)
    """

    if xmaj is None:
        ax.xaxis.set_major_locator(AutoLocator())
    else:
        ax.xaxis.set_major_locator(MultipleLocator(xmaj))

    if ymaj is None:
        ax.yaxis.set_major_locator(AutoLocator())
    else:
        ax.yaxis.set_major_locator(MultipleLocator(ymaj))

    if xmin is None:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
    else:
        ax.xaxis.set_minor_locator(MultipleLocator(xmin))

    if ymin is None:
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    else:
        ax.yaxis.set_minor_locator(MultipleLocator(ymin))


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
        