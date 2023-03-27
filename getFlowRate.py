###############################################################################
# Written by Chloe W L
#
# Plots volumes vs time for a full set of experimental data for water on
# silanized glass (full sets of experiments saved together in one text file),
# then fits the slope of the volume vs time curve to get the correction to
# the flow rate (nominally 1 frame per .2 uL)
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

# exptType can be "wait_time", "q_0_min", or "q_3_min"
exptType = "wait_time"

# setNum can be 0, 1, or 2
setNum = 1

filename = "./water_data_silane/" + exptType + " (base bath " + str(setNum) + ")"

# for use with toluene data:
#calibrate = [0.516/65,0.516/65,0.516/53.3]
#calibrate = calibrate[0]

# takes width in mm and CA in degrees; returns volume in m^3
def vol_finder(width,CA):
        width = width/1000.0
        CA = np.pi*CA/180.0
        return (np.pi/3.0) * ((width/(2*np.sin(CA)))**3) * (2+np.cos(CA)) * ((1-np.cos(CA))**2)

def flowRate_finder(filename):
    CA_list = []
    width_list = []
    vol_list = []
    a = 0
    with open(filename + '.txt') as csvfile:
        plots = csv.reader(csvfile, delimiter='\t')
        for row in plots:
            a += 1
            if a > 0:
                if float(row[0]) < 90.0:
                    vol_list.append(vol_finder(float(row[1]),float(row[0])))
                    # for use with toluene data:
                    #vol_list.append(vol_finder(calibrate*(float(row[3]) - float(row[2])), \
                    #(float(row[0]) + float(row[1]))/2.0))

    # plot volume vs frame number for all experiments in file
    plt.plot(range(len(vol_list)), np.array(vol_list)*1000.0, 'o',  markersize = 5)
    plt.xlabel('time (frames)')
    plt.ylabel('volume (uL)')
    plt.show()

    # finds the frame numbers of the beginning of each experiment
    deriv_threshold = 0.4E-8
    vol_list = np.array(vol_list)
    deriv = vol_list[1:] - vol_list[:-1]
    sep_list = [0]
    for ii in range(len(deriv)):
        if deriv[ii] > deriv_threshold:
            sep_list.append(ii)
    sep_list.append(range(len(deriv))[-1])

    rate_list = []

    a = 25 # how many frames after beginning of experiment to start fitting
    b = 15 # how many frames before end of experiment to stop fitting
    for ii in range(len(sep_list)-1):
        fit = np.polyfit(range(len(vol_list))[sep_list[ii]+a:sep_list[ii+1]-b], \
        vol_list[sep_list[ii]+a:sep_list[ii+1]-b], 1)
        fit_fn = np.poly1d(fit)
        rate_list.append(fit[0]/-0.2E-9)
        # slope (fit[0]) is in m^3 / frame

        # plot volume vs time with fits
        plt.plot(range(len(vol_list))[sep_list[ii]+a:sep_list[ii+1]-b], \
        vol_list[sep_list[ii]+a:sep_list[ii+1]-b],'o')
        plt.plot(range(len(vol_list))[sep_list[ii]+a:sep_list[ii+1]-b], \
        fit_fn(range(len(vol_list))[sep_list[ii]+a:sep_list[ii+1]-b]))
    plt.show()
    plt.clf()

    return rate_list


flowRate_finder(filename)
