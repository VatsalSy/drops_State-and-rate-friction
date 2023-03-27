###############################################################################
# Written by Chloe W L
#
# Plots a full set of experimental data for water on gold
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

matplotlib.rc('xtick', labelsize=8)
matplotlib.rc('ytick', labelsize=8)
plt.rcParams["figure.figsize"] = (5,3)

# exptType can be "wait_time", "q_0_min", or "q_5_min"
exptType = "q_5_min"

# setNum can be 0, 1, or "reverse"
setNum = 0

filename = "./water_data_gold/" + exptType + "-" + str(setNum)

CA_list = []
width_list = []

CA = []
width = []
width.append(5.0)
# initial guess for drop width

with open(filename + '.txt','rU') as csvfile:
    plots = csv.reader(csvfile, delimiter='\t')
    for row in plots:
        if float(row[0]) < 90.0:
        # excludes CA > 90, which tend to be bad fitting to the drop's reflection
            if np.abs(width[-1] - float(row[1])) < 1.5:
            # determines whether a new experiment has started
            # based on whether the width jumps up substantially
                CA.append(float(row[0]))
                width.append(float(row[1]))
            else:
                width.pop(0)
                CA_list.append(CA)
                CA = []
                width_list.append(width)
                width = []
                width.append(float(row[1]))
                width.append(float(row[1]))
                CA.append(float(row[0]))

# remove that initial guess for width
width.pop(0)
CA_list.append(CA)
width_list.append(width)


if exptType == "wait_time":
    if setNum == "reverse":
        order = [3,2,1,0]
    else:
        order = [0,1,2,3]
    viridis = cm.get_cmap('plasma', 7)

else:
    if setNum == "reverse":
        order = [4,3,2,1,0]
    else:
        order = [0,1,2,3,4]
    viridis = cm.get_cmap('viridis', 6)


for ii in range(len(CA_list)):
    if exptType == "wait_time":
        l = " "
        if ii == 0:
            l = '0 min'
        if ii == 1:
            l = '2 min'
        if ii == 2:
            l = '5 min'
        if ii == 3:
            l = '10 min'

        plt.plot(CA_list[order[ii]], width_list[order[ii]], 'o', color=viridis.colors[ii], markersize = 5, label = l)

    else:
        l = " "
        if ii == 0:
            l = '.4 uL/s'
        if ii == 1:
            l = '1 uL/s'
        if ii == 2:
            l = '2 uL/s'
        if ii == 3:
            l = '4 uL/s'
        if ii == 4:
            l = '8 uL/s'

        plt.plot(CA_list[order[ii]], width_list[order[ii]], 'o', color=viridis.colors[ii], markersize = 5, label = l)

axes = plt.gca()
#axes.set_ylim([1,5])
#axes.set_xlim([20,90])

axes.legend(loc="lower right")
for tick in axes.get_xticklabels():
    tick.set_fontname("Arial")
for tick in axes.get_yticklabels():
    tick.set_fontname("Arial")

plt.xlabel("contact angle")
plt.ylabel("drop width")
plt.tight_layout()

plt.show()
plt.clf()
