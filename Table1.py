#!/usr/bin/env python
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
debug = True


import matplotlib as mpl
mpl.rc('font',family='serif')
mpl.rc('font',serif='Times') 
mpl.rc('text', usetex=True)
mpl.rc('font',size=18)

fig = plt.figure(1,figsize=(8,14))


# Here we get the stations and days of scans



f = open('scanned_chips','r')
timesSC=[]
staSC=[]
chan=[]
bad =0
for line in f:
    try:

        line=line.split(' ')
        curstr = line[2] + '-' + line[0] + '-' + line[1] + 'T' + \
                line[3].replace('hr','') + ':' + line[4].replace('min','') + ':00.0'

        timesSC.append(UTCDateTime(curstr))
        staSC.append((line[6].replace(' ','')).rstrip())
        line[5] = line[5].strip()
        line[5] = line[5].replace('H','P')
        chan.append(line[5])
    except:
        print(line)
        bad +=1
f.close()

print('Here are the number of good scans: ' + str(len(chan)))
print('Here are the number of problematic scans: ' + str(bad))


stalist = list(set(staSC))
f2 = open('Results.csv','w')
f2.write('Station, LPZ, LPN, LPE, SPZ, SPN, SPE\n')
for sta in stalist:
    cnts={'LPN': 0, 'LPZ': 0, 'LPE': 0, 'SPZ': 0, 'SPN' : 0, 'SPE' :0}
    for pair in zip(staSC, chan):
        try:
            if pair[0] == sta:
                cnts[pair[1]] += 1
        except:
            pass
    f2.write(sta + ', ' + str(cnts['LPZ']) + ', ' + str(cnts['LPN']) + ', ' +
            str(cnts['LPE']) + ', ' + str(cnts['SPZ']) + ', ' + str(cnts['SPN']) + ', ' +
            str(cnts['SPE']) + '\n')

f2.close()
