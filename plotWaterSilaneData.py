###############################################################################
# Written by Chloe W L
#
# Plots a full set of experimental data for water on silanized glass
# (full sets of experiments saved together in one text file)
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

from scipy.optimize import curve_fit

matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)
plt.rcParams["figure.figsize"] = (5,3)

# exptType can be "wait_time", "q_0_min", or "q_3_min"
exptType = "wait_time"

# setNum can be 0, 1, or 2
setNum = 1

filename = "./water_data_silane/" + exptType + " (base bath " + str(setNum) + ")"

CA_list = []
width_list = []

CA = []
width = []
width.append(4.0)
CA.append(0.0)

with open(filename + '.txt') as csvfile:
    plots = csv.reader(csvfile, delimiter='\t')
    for row in plots:
        if float(row[0]) < 90.0:
        # removes spurrious points (where the software
        # interpreted the reflection as the drop)
            if np.abs(width[-1] - float(row[1])) < .75:
            # determines whether a new experiment has started
            # based on whether the width jumps up substantially
                CA.append(float(row[0]))
                width.append(float(row[1]))
            else:
                CA.pop(0)
                width.pop(0)
                CA_list.append(CA)
                CA = []
                CA.append(float(row[0]))
                CA.append(float(row[0]))
                width_list.append(width)
                width = []
                width.append(float(row[1]))
                width.append(float(row[1]))

CA.pop(0)
width.pop(0)
CA_list.append(CA)
width_list.append(width)


if "q_0_min" in filename or "q_3_min" in filename:

    if "(base bath 0)" in filename:
        order = [0,1,2]
    elif "(base bath 1)" in filename:
        order = [0,1,2]
    elif "(base bath 2)" in filename:
        order = [2,1,0]

    viridis = cm.get_cmap('viridis', 5)

    for ii in range(len(CA_list)):
        l = " "
        if ii == 0:
            l = '0.4 uL/s'
        if ii == 1:
            l = '2 uL/s'
        if ii == 2:
            l = '8 uL/s'

        plt.plot(CA_list[order[ii]], width_list[order[ii]], 'o', \
        color=viridis.colors[ii+1], markersize = 5, label = l)

else:

    if "(base bath 0)" in filename:
        order = [0,3,1,4,2]
    elif "(base bath 1)" in filename:
        order = [0,1,2,3,4,5]
    elif "(base bath 2)" in filename:
        order = [5,4,3,2,1,0]

    viridis = cm.get_cmap('plasma', 7)

    for ii in range(len(CA_list)):
        l = " "
        if ii == 0:
            l = '0 min'
        if ii == 1:
            l = '1 min'
        if ii == 2:
            l = '2 min'
        if ii == 3:
            l = '3 min'
        if ii == 4:
            l = '4 min'
        if ii == 5:
            l = '5 min'

        plt.plot(CA_list[order[ii]], width_list[order[ii]], 'o', \
        color=viridis.colors[ii], markersize = 5, label = l)
        #shift = [0, 4, 4, 4, 8, 12]
        #length = len(CA_list[order[ii]])
        #plt.plot(np.array(np.linspace(shift[ii], shift[ii] + length - 1, num=length))/10, \
        #np.array(width_list[order[ii]])/np.max(width_list[order[ii]]), 'o', \
        #color=viridis.colors[ii], markersize = 5, label = l)

axes = plt.gca()
#axes.set_ylim([1,5])
#axes.set_xlim([20,90])

axes.legend(loc="lower right")
for tick in axes.get_xticklabels():
    tick.set_fontname("Arial")
for tick in axes.get_yticklabels():
    tick.set_fontname("Arial")

plt.xlabel("contact angle (degrees)")
plt.ylabel("width (mm)")
plt.tight_layout()

plt.show()
plt.clf()
