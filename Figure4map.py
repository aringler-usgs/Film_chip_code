#!/usr/bin/env python
from obspy.clients.fdsn import Client
from obspy import read_inventory
from obspy.core import UTCDateTime 
from obspy.imaging.maps import plot_basemap
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.cm import get_cmap
import numpy as np
import sys


import matplotlib as mpl
mpl.rc('font',family='serif')
mpl.rc('font',serif='Times') 
mpl.rc('text', usetex=True)
mpl.rc('font',size=18)


codes = set([0,1])
cmap = get_cmap(name="Paired", lut=len(codes))

debug = True

lat =[]
lon=[]
depth=[]
mag =[]


# Here we get the stations lats and lons
f = open('newquakes.csv','r')
info = f.readline()
for line in f:
    print(line)
    line = line.split(',')
    lon.append(float(line[5]))
    lat.append(float(line[4]))
    depth.append(float(line[6]))
    mag.append(float(line[7]))
f.close()


min_size = 15.
max_size = 30.
min_size_ = min(mag) - 1
max_size_ = max(mag) + 1
frac = [(0.2 + (_i - min_size_)) / (max_size_ - min_size_) for _i in mag]
size_plot = [(_i * (max_size - min_size)) ** 2 for _i in frac]



fig =plt.figure(1, figsize=(12,8))

m = Basemap(projection='moll', resolution='c', lon_0 = 0.)
m.drawcoastlines()
m.fillcontinents(color='.9')
m.drawparallels(np.arange(-90., 120., 30.))
m.drawmeridians(np.arange(0., 420., 60.))
m.drawmapboundary()
ax = plt.gca()

mymap = plt.get_cmap('viridis')
mycolor = mymap(frac)

x,y = m(lon, lat)
sc = m.scatter(x,y, s=size_plot, c = mycolor, zorder=3, cmap='viridis') 


mags = [6, 7, 8, 9]
frac = [(0.2 + (_i - min_size_)) / (max_size_ - min_size_) for _i in mags]
size_plot = [(_i * (max_size - min_size)) ** 2 for _i in frac]
for sz, mag, cur in zip(size_plot,  mags, frac):
    sc2 = m.scatter([0.] ,[0.],s =[np.mean(sz)] ,c=[mymap(cur)],  cmap='viridis', zorder=3, label= 'M' + str(mag))

plt.title('Initial ' + str(len(lon)) + ' Scanned Earthquakes')

plt.legend(loc=9, ncol=5, bbox_to_anchor=(0.5,-0.01))
#plt.show()
plt.savefig('InitialEQ.jpg', dpi=400, format='JPEG')
plt.savefig('InitialEQ.pdf', dpi=400, format='PDF')
