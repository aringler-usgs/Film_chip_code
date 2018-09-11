#!/usr/bin/env python
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
debug = True


import matplotlib as mpl
mpl.rc('font',family='serif')
mpl.rc('font',serif='Times') 
mpl.rc('text', usetex=True)
mpl.rc('font',size=18)

fig = plt.figure(1,figsize=(12,14))


# Here we get the stations and days of scans

chans = ['LPZ','SPN', 'LPN', 'SPN', 'LPE', 'SPE']
chans = ['LPZ']
for chidx, chan in enumerate(chans):
    f = open('scanned_chips','r')
    timesSC=[]
    staSC=[]

    for line in f:
        try:
            if chan in line:
                line=line.split(' ')
                curstr = line[2] + '-' + line[0] + '-' + line[1] + 'T' + \
                        line[3].replace('hr','') + ':' + line[4].replace('min','') + ':00.0'

                timesSC.append(UTCDateTime(curstr))
                staSC.append((line[6].replace(' ','')).rstrip())
        except:
            print(line)
    f.close()


    #timesSC= timesSC[:100]
    #staSC = staSC[:100]
    
    stalist = list(set(staSC))
    stalist.sort()
                                
    if debug:
        print(timesSC[:10])
        print(staSC[:10])

    print('HEre is the length of stalist:' + str(len(stalist)))
    stalistG = stalist
    for idxs in [1,2]:
        if idxs == 1:
            stalist = stalistG[:75]
        else:
            stalist = stalistG[75:]
        plt.subplot(1,2,idxs)
        
        #stalist = stalist[:75]
        
        for idx, sta in enumerate(stalist):
            currtimes = []
            for pair in zip(timesSC, staSC):
                if pair[1] == sta:
                    if pair[0].year < 1960.:
                        continue
                    else:
                        currtimes.append(pair[0].year + pair[0].julday/365.25)
            stidx = [idx]*len(currtimes)
            plt.plot( currtimes, stidx, '|',color='k')
        plt.ylim(-0.5, len(stalist)+0.5)
        plt.xlim(1962.,max(timesSC).year +1)
        plt.yticks(range(len(stalist)),stalist, fontsize=14)
        plt.xticks([1962, 1967, 1972, 1977])
fig.suptitle('WWSSN Film Chips Scanned for ' + chan)
plt.savefig('scansbyyear.jpg',format='JPEG',dpi=400)
plt.savefig('scansbyyear.pdf',format='PDF',dpi=400)
#plt.show()
