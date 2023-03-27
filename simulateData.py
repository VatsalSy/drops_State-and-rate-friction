###############################################################################
# Written by Chloe W L
# Feb 8, 2022
#
# Simulates the width and contact angle of a
# drop removed at constant flow rate with a
# given static friction f_mu, equilibrium
# contact angle eq_CA, and drag coefficient
# beta (overdamped dynamics)
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
import scipy.optimize

# surface tension of water in air
gamma = 0.072

def simulateDrop(w_i,v_i,v_f,f_mu,beta,eq_CA,q,n_steps):
# in mm, L, .... , degrees, and L/s

    # convert to meters, radians, etc
    # and calculate needed parameters like total time of aspiration and dt
    width_list = [w_i/1000.0]
    volume_list = np.linspace(v_i,v_f,num=n_steps)
    t_total = (v_i-v_f)/q
    eq_CA = np.pi*eq_CA/180
    CA_list = [eq_CA]
    dt = t_total/n_steps

    # for each timestep, find the current force on the contact line assuming
    # young-like equation. Then modify width according to the corresponding
    # velocity and determine the new CA based on the new width and new volume
    # (decreased linearly in time)
    for ii in range(n_steps):
        width = width_list[ii]
        volume = volume_list[ii]
        def vol_func(CA):
            return volume - (np.pi/3.0) * ((width/(2*np.sin(CA)))**3) * \
            (2+np.cos(CA)) * ((1-np.cos(CA))**2)

        # for a given width and volume, calculate the new CA
        CA = scipy.optimize.fsolve(vol_func, CA_list[-1], xtol=1E-8)
        CA_list.append(CA[0])

        # if the CA has gone to zero, end the calculation
        if CA_list[-1] == 0:
            n_steps = 0

        # calculate the force on the contact line
        f = gamma*(np.cos(CA)-np.cos(eq_CA))

        # if the force is smaller than f_mu (usually set to 0), do nothing
        # this also prevents drop spreading
        if (f < f_mu and width_list[-1] == width_list[0] and ii < n_steps-1):
            width_list.append(width_list[-1])
        # otherwise, move the contact line (ie, decrease the drop width)
        elif ii < n_steps-1:
            width_list.append(width_list[-1]-dt*2*f/beta)

    # get rid of initial CA guess and convert things back to mm and degrees
    CA_list.pop(0)
    CA_list = np.array(CA_list)
    CA_list = 180*CA_list/np.pi
    width_list = np.array(width_list)
    width_list = 1000*width_list
    #np.savetxt(folder + 'f_mu_' + str(f_mu) + '_CA_' + str(180*eq_CA/np.pi) + '_beta_' + str(beta) + '.txt', \
    #np.transpose([CA_list,width_list]), fmt='%.6e', delimiter='\t')
    return np.array([CA_list,width_list])

'''
# EXAMPLE
data = simulateDrop(4.2, 16e-9, 3e-9, 0, 10, 75, 2E-9, 1000)
plt.plot(data[0,:], data[1,:], '.-')
plt.xlabel("contact angle")
plt.ylabel("width")
plt.show()
plt.clf()
'''
