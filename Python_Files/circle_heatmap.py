#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:07:28 2022

Heat diagram of spheres for the histogram curves!
Heatmap code adapted from: https://stackoverflow.com/questions/25236026/circular-interpolated-heat-map-plot-using-python (answer w/ highest score)
"""

## Import libraries 
import pandas as pd 
import matplotlib.pyplot as plt
import os
import numpy as np
# from mpl_toolkits.mplot3d import Axes3D

## Set some parameters:
r = 1 # this is the radius of the sphere
bin_width = 0.05 # change the increment size according to how specific i want the bin size to be for the hist! 
bin_range = np.arange(0, r+bin_width, bin_width)

WHICH_SIM = 0 # if 0, FILAMENT simulations, if 1, CROSSLINKER simulations

# Importing the LARGEST_CURVE data (which will normalize the color bar across all of the results)
# FOR FILAMENT SIMULATIONS:
if WHICH_SIM == 0:
    folders = ['fil', 'fil_no_steric', 'fil_no_steric_tread', 'fil_tread']
    num_filaments = 500
    to_folder = int((num_filaments-100) / 100) ################################# specific to these folders - change if applying to different data 
    
    ## Importing the data --------------------------------------------------------
    os.chdir('../final_simulations')
    curve_dict = {}
    fil_legend = []
    for x in os.listdir(): 
        if x in folders: 
            os.chdir(x)
            for x in sorted(os.listdir()):
                if x.endswith(str(to_folder)): 
                    os.chdir(x)
                    print(x)
                    curve = pd.read_excel("histogram_curve.xlsx")
                    curve_dict[curve.columns.values[1]] = curve.iloc[:,1]
                    fil_legend.append(curve.columns.values[1][15:])
                    os.chdir('..')  
            os.chdir('..')
       
    
    for key in curve_dict:
        print(key)
        fig = plt.figure(figsize=(10,9))
        # ax1 = Axes3D(fig)
        rad = np.linspace(0, 1, 20) # 0 -> 20 (because I have 20 points from the histogram values)
        azm = np.linspace(0, 2 * np.pi, 20) # 0 -> 20 (must match the size of rad, used to project this in polar)
        r, th = np.meshgrid(rad, azm) # function commonly used for heat maps -> projects the arrays into a square matrix
        prac = (curve_dict[key]) # get the data for this sample 
        z = np.tile(prac, (20, 1)) # project the data into a square matrix (same size as rad and azm)
        ax = plt.subplot(projection="polar") # create a polar graph
        cmap = plt.colormaps['winter_r'] # this is the color set I chose from matplotlib
        im = plt.pcolormesh(th, r, z, cmap=cmap,  vmin=0, vmax=3.2) # plot the colors using the histogram distribution
        ax.set_rticks([]) # getting rid of the ticks from the center to the end 
        # ax.set_rlabel_position(0)
        ax.set_xticks([]) # getting rid of the radial ticks 
        fig.colorbar(im, shrink=0.9) # include the colorbar with the values 
        # plt.plot(azm, r, color='k', ls='none') 
        # plt.grid()
        plt.title(key, y = 1.02, x = 0.6, size = 23) # centering the title 
        ttl = 'color_map_' + key 
        fig.savefig(ttl, bbox_inches = 'tight')
    
else:     
    
    # FOR CROSSLINKER SIMULATIONS:
    num_filaments = 500 # 250, 500, 750, 1000
    # num_sims = 9 # eventually automate this (number of run???? directories)
    dir_nums = list(range(9, 18))  # (0, 9), (9, 18), (18, 27), (27, 36)
    folders = []
    for i in dir_nums:
        if i < 10:
            folder_str = 'run000' + str(i)
            folders.append(folder_str)
        else:
            folder_str = 'run00' + str(i)
            folders.append(folder_str)
            
    ## Importing the data --------------------------------------------------------
    os.chdir('../final_simulations/cross')
    curve_dict = {}
    fil_legend = []
    for x in sorted(os.listdir()): 
        if x in folders: 
            os.chdir(x)
            print(x)
            curve = pd.read_excel("histogram_curve.xlsx")
            curve_dict[curve.columns.values[1]] = curve.iloc[:,1]
            fil_legend.append(curve.columns.values[1][15:])
            os.chdir('..')  
    
    for key in curve_dict:
        print(key)
        fig = plt.figure(figsize=(10,9))
        # ax1 = Axes3D(fig)
        rad = np.linspace(0, 1, 20) # 0 -> 20 (because I have 20 points from the histogram values)
        azm = np.linspace(0, 2 * np.pi, 20) # 0 -> 20 (must match the size of rad, used to project this in polar)
        r, th = np.meshgrid(rad, azm) # function commonly used for heat maps -> projects the arrays into a square matrix
        prac = (curve_dict[key]) # get the data for this sample 
        z = np.tile(prac, (20, 1)) # project the data into a square matrix (same size as rad and azm)
        ax = plt.subplot(projection="polar") # create a polar graph
        cmap = plt.colormaps['winter_r'] # this is the color set I chose from matplotlib
        im = plt.pcolormesh(th, r, z, cmap=cmap, vmin=0, vmax=3.2) # plot the colors using the histogram distribution
        ax.set_rticks([]) # getting rid of the ticks from the center to the end 
        # ax.set_rlabel_position(0)
        ax.set_xticks([]) # getting rid of the radial ticks 
        fig.colorbar(im, shrink=0.9) # include the colorbar with the values 
        # plt.plot(azm, r, color='k', ls='none') 
        # plt.grid()
        plt.title(key, y = 1.02, x = 0.6, size = 23) # centering the title 
        ttl = 'color_map_' + key 
        fig.savefig(ttl, bbox_inches = 'tight')
    