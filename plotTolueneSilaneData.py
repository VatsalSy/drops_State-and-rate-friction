###############################################################################
# Written by Chloe W L
#
# Plots a full set of experimental data for toluene on silanized glass
# (each experiment saved in a separate txt file)
# Determine which set to plot by changing exptType and setNum below
#
###############################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import time
import sys
import os
import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)
plt.rcParams["figure.figsize"] = (5,3)

# setNum can be 0, 1, or 2
setNum = 0
# exptType can be "wait_time", "q_0_min", or "q_1_min"
exptType = "wait_time"

dirname = './toluene_data_silane/' + str(setNum) + '/'

# converts pixel to mm
calibrate = [0.516/65,0.516/65,0.516/53.3]
calibrate = calibrate[int(setNum)]

CA_list = []
width_list = []

CA = []
width = []

if exptType == "wait_time":
    times = ['00', 'p5', '01', '02']
else:
    times = ['p4', '01', '02', '04', '10']

for ii in range(len(times)):
    CA = []
    width = []
    if exptType == "wait_time":
        filename = dirname + exptType + "-" + str(times[ii]) + '_min-' + str(setNum) + '.txt'
    else:
        filename = dirname + exptType + "-" + str(times[ii]) + '_uL_s-' + str(setNum) + '.txt'
    with open(filename,'rU') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        linenum = 0
        for row in plots:
            linenum += 1
            if linenum > 1:
                CA.append((float(row[0])+float(row[1]))/2.0)
                width.append(float(row[3])-float(row[2]))
    CA_list.append(CA)
    width_list.append(width)

if exptType == "wait_time":
    viridis = cm.get_cmap('plasma', 6)
else:
    viridis = cm.get_cmap('viridis', 6)

for ii in range(len(CA_list)):
    l = " "
    if len(CA_list) == 4:
        if ii == 0:
            l = '0 min'
        if ii == 1:
            l = '.5 min'
        if ii == 2:
            l = '1 min'
        if ii == 3:
            l = '2 min'
    elif len(CA_list) == 5:
        if ii == 0:
            l = '.4 uL/s'
        if ii == 1:
            l = '1 uL/s'
        if ii == 2:
            l = '2 uL/s'
        if ii == 3:
            l = '4 uL/s'
        if ii == 4:
            l = '10 uL/s'

    plt.plot(CA_list[ii], calibrate*np.array(width_list[ii]), 'o', color=viridis.colors[ii], markersize = 5, label = l)

axes = plt.gca()
#axes.set_ylim([0,8])
#axes.set_xlim([10,25])

axes.legend(loc="lower left")
for tick in axes.get_xticklabels():
    tick.set_fontname("Arial")
for tick in axes.get_yticklabels():
    tick.set_fontname("Arial")

plt.xlabel("contact angle (degrees)")
plt.ylabel("drop width (mm)")
plt.tight_layout()

plt.show()
plt.clf()
