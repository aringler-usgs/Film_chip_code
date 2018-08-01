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

latSta=[]
lonSta=[]
StaSta =[]
col =[]

# Here we get the stations lats and lons
f = open('wwssnlist.csv','r')
for line in f:
    line = line.split(',')
    lonSta.append(float(line[3]))
    latSta.append(float(line[2]))
    StaSta.append(line[1].replace(' ',''))
    if line[1].replace(' ','') in ['NAI', 'SPA', 'CHG', 'KIP', 'BUL', 'AFI', 'ANT', 'CTA', 'MUN', 'COL', 'SEO', 'SJG', 'ALQ', 'KON']:
        col.append('C0')
    else:
        col.append('C1')
f.close()


fig =plt.figure(1, figsize=(10,8))

m = Basemap(projection='moll', resolution='c', lon_0 = 0.)
m.drawcoastlines()
m.fillcontinents(color='.9')
m.drawparallels(np.arange(-90., 120., 30.))
m.drawmeridians(np.arange(0., 420., 60.))
m.drawmapboundary()
ax = plt.gca()

mymap = plt.get_cmap('viridis')
#mycolor = mymap(p100)
#if debug:
#    print(mycolor)
x,y = m(lonSta, latSta)
sc = m.scatter(x,y, s=50, c = col, zorder=3, cmap='viridis', marker="v") 

#days = np.asarray([0., 25., 50., 75., 100.])/100.
#size = np.asarray([0., 25., 50., 75., 100.])/100.
#frac = [(0.2 + (_i - min_size_)) / (max_size_ - min_size_) for _i in size]
#size_plot = [(_i * (max_size - min_size)) ** 2 for _i in frac]
#for pair in zip(days, size_plot):
    
sc2 = m.scatter([0.] ,[0.],s =50.,c='C0',  cmap='viridis', zorder=3, marker='v', label= 'Station')
sc2 = m.scatter([0.] ,[0.],s =50.,c='C1',  cmap='viridis', zorder=3, marker='v', label= 'Stations with over 1000 Scans')
#plt.title('From ' + str(min(timesM).year) + ' to  ' + str(max(timesM).year))
plt.title('WWSSN Station Map')
plt.legend(loc=9, ncol=1, bbox_to_anchor=(0.5,-0.01))
#plt.show()
plt.savefig('Figure1.jpg', dpi=400, format='JPEG')
