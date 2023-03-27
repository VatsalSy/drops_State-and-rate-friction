###############################################################################
# Written by Chloe W L
# Feb 10, 2022
#
# Compares simulated drop data made by simulateData.py
# with experimental data to find best fit for eq_CA,
# and damping coefficient beta
# Does this for entire data sets and saves the resulting
# parameters in a txt file
#
###############################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import time
import matplotlib.colors as mcolors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import simulateData as sd

n_steps = 1000
# 1000 steps seems to give good convergence
# if things fail, they will probably fail wildly.
# then you should increase n_steps

# for a single experiment, finds the best fit values of beta and
# the equilibrium contact angle
def simulateOneExperiment(data, q, saveFile):

    # gets the initial and final configurations of the drop
    CA_i = data[0,0]
    w_i = data[1,0]
    CA_f = data[0,-1]
    w_f = data[1,-1]

    # finds the initial and final volumes
    def vol_func(CA, width):
        CA = np.pi*CA/180.0
        width = width/1000.0
        return (np.pi/3.0) * ((width/(2*np.sin(CA)))**3) * (2+np.cos(CA)) * ((1-np.cos(CA))**2)
    vol_i = vol_func(CA_i,w_i)
    vol_f = vol_func(CA_f,w_f)

    # LOAD EXPERIMENTAL DATA TO BE FIT

    f_mu = 0
    # sets max static friction to zero

    eq_CA_list = np.linspace(65,85,num=21)
    # set which points in CA phase space will be tested

    # for a given list of beta values, returns the residuals
    # It's set up this way so that beta can be iterated over in
    # something like a bisection algorithm to find a local min
    # more quickly
    def simulateBeta(beta_list):

        residualsList = []
        simDataList = []
        paramList = []
        # for each combination of beta and eq CA tried, stores the sum over all
        # experimental data points of
        # ((simulated width - actual width)^2)/(actual width)
        for jj in range(len(beta_list)):
            beta = beta_list[jj]
            for kk in range(len(eq_CA_list)):
                eq_CA = eq_CA_list[kk]
                simData = sd.simulateDrop(w_i,vol_i,vol_f,f_mu,beta,eq_CA,q,n_steps)
                residuals = []
                for ll in range(len(data[0,:])):
                    CA = data[0,ll]
                    width = data[1,ll]
                    # finds the index for the closest simulated CA value
                    a = np.argmin(np.abs(CA*np.ones((len(simData[0,:])))-simData[0,:]))
                    # calculates a residual for the corresponding width
                    residuals.append(((simData[1,a]-width)**2.0)/width)
                residualsList.append(np.sqrt(np.sum(np.array(residuals))))
                simDataList.append(simData)
                paramList.append([f_mu,jj,kk])
        return paramList, residualsList

    # starts with a rough guess for beta and zooms in on best fit
    # at end, want to check that best fit wasn't endpoint; if it was,
    # use a larger starting range
    # note this isn't guaranteed to find global best fit
    beta_list = np.linspace(20,100,num=5)
    paramList, residualsList = simulateBeta(beta_list)
    beta_mid = beta_list[paramList[np.argmin(residualsList)][1]]
    beta_list = np.linspace(beta_mid-15, beta_mid+15, num=7)
    paramList, residualsList = simulateBeta(beta_list)

    '''
    # SAVE RESULTS OF BEST FIT
    f = open(saveFile, 'a')
    f.write(str(f_mu) + '\t' \
    + str(beta_list[paramList[np.argmin(residualsList)][1]]) + '\t' \
    + str(eq_CA_list[paramList[np.argmin(residualsList)][2]]) + '\n')
    f.close()
    '''

    # PLOT RESULTS OF BEST FIT WITH DATA
    f_mu = 0.0
    beta = beta_list[paramList[np.argmin(residualsList)][1]]
    eq_CA = eq_CA_list[paramList[np.argmin(residualsList)][2]]
    #simData = sd.simulateDrop(w_i,vol_i,vol_f,f_mu,beta,eq_CA,q,n_steps)

    print("beta = " + str(beta))
    print("theta = " + str(eq_CA))
    print("residual = " + str(np.min(residualsList)))
    '''
    plt.plot(data[0,:],data[1,:],'o',color='tab:blue',label='data')
    plt.plot(simData[0,:],simData[1,:],'.',color='tab:purple',label='simulation')
    axes = plt.gca()
    axes.legend()
    plt.ylabel('drop width (mm)')
    plt.xlabel('contact angle (degrees)')
    plt.show()
    plt.clf()
    '''


# SET EXPERIMENTS TO BE SIMULATED (water on silanized glass)

# uncomment one of these options
# note that each file contains several experiments, separated out below
# and run one at a time through the best fit function above
nameList = ['wait_time (base bath 0)']#, # order of experiments is 0, 2, 5, 1, 3 minutes
#'wait_time (base bath 1)', # order of experiments is 0, 1, 2, 3, 4, 5 minutes
#'wait_time (base bath 2)'] # order of experiments is 5, 4, 3, 2, 1, 0 minutes
#'q_0_min (base bath 0)', # order of experiments is 0.4, 2, 8 uL/s
#'q_0_min (base bath 1)', # order of experiments is 0.4, 2, 8 uL/s
#'q_0_min (base bath 2)'] # order of experiments is 8, 2, 0.4 uL/s
#'q_3_min (base bath 0)', # order of experiments is 0.4, 2, 8 uL/s
#'q_3_min (base bath 1)', # order of experiments is 0.4, 2, 8 uL/s
#'q_3_min (base bath 2)'] # order of experiments is 8, 2, 0.4 uL/s

# uncomment the corresponding flow rate list, multiplied here by the
# best fit corrections to the flow rate obtained from getFlowRate.py
qList = [[a*b for a,b in zip([2.0E-9,2.0E-9,2.0E-9,2.0E-9,2.0E-9],[1.03,1.03,1.00,1.09,1.01])]]#,
#[a*b for a,b in zip([2.0E-9,2.0E-9,2.0E-9,2.0E-9,2.0E-9,2.0E-9],[1.02,0.98,0.93,0.97,1.11,1.01])],
#[a*b for a,b in zip([2.0E-9,2.0E-9,2.0E-9,2.0E-9,2.0E-9,2.0E-9],[1.10,1.00,1.06,0.98,1.07,1.07])]]
#[a*b for a,b in zip([0.4E-9,2.0E-9,10.0E-9],[1.15,1.06,0.84])],
#[a*b for a,b in zip([0.4E-9,2.0E-9,10.0E-9],[1.08,0.99,0.80])],
#[a*b for a,b in zip([10.0E-9,2.0E-9,0.4E-9],[0.80,1.08,1.15])]]
#[a*b for a,b in zip([0.4E-9,2.0E-9,10.0E-9],[1.12,1.09,0.67])],
#[a*b for a,b in zip([0.4E-9,2.0E-9,10.0E-9],[1.00,0.97,0.67])],
#[a*b for a,b in zip([10.0E-9,2.0E-9,0.4E-9],[0.74,0.99,1.10])]]
# m^3/s

filename = nameList[0]
saveFile = "./best_fits-" + filename + ".txt"
#f = open(saveFile, 'a')
#f.write('f_mu' + '\t' + 'beta' + '\t' + 'eq_CA' + '\n')
#f.flush()
#f.close()

CA_list = []
width_list = []
CA = []
width = []

# put in initial guess for CA and width
width.append(4.0)
CA.append(0.0)

# separate out different experiments
with open('./water_data_silane/' + filename + '.txt') as csvfile:
    plots = csv.reader(csvfile, delimiter='\t')
    for row in plots:
        if float(row[0]) < 90.0:
            # determines whether a new experiment has started
            # based on whether the width jumps up substantially
            if np.abs(width[-1] - float(row[1])) < .75:
                CA.append(float(row[0]))
                width.append(float(row[1]))
            else:
                width.pop(0)
                CA.pop(0)
                CA_list.append(CA)
                CA = []
                CA.append(float(row[0]))
                CA.append(float(row[0]))
                width_list.append(width)
                width = []
                width.append(float(row[1]))
                width.append(float(row[1]))

# remove that initial guess for CA and width
width.pop(0)
CA.pop(0)
CA_list.append(CA)
width_list.append(width)

# repeats best fit procedure for each experiment in
# the file
for jj in range(len(CA_list)):
    data = np.array([CA_list[jj],width_list[jj]])
    q = qList[0][jj]
    simulateOneExperiment(data, q, saveFile)
