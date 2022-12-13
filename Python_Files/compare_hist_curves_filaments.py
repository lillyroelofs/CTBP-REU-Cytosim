# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 18:51:50 2022

Plotting all of the distribution curves on a single graph
"""

## Import libraries
import os
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd


## Setting any parameters ----------------------------------------------------
r = 1 # this is the radius of the sphere
bin_width = 0.05 # change the increment size according to how specific i want the bin size to be for the hist! 
bin_range = np.arange(0, r+bin_width, bin_width)
all_one = 0 # 0 = the data is coming from different folders, 1 = the data is coming from the same folder
colors = ['#225F99', '#225F99', '#2E6917', '#2E6917']

## Creating the x-axis (radial distances) ------------------------------------
# note: this should be automatically imported from the distance_segmentation.py file in the future        

# Find the midpoint per bin range, also create a list of strings of this for the bar plot  
bar_strings = []
mid_points = []
for b in range(len(bin_range)-1):
    # calculate the average of the bin and divide it by the radius to normalize it 
    middle = ((bin_range[b+1]+bin_range[b])/2) # calculates the averge of the bin 
    calc = '{}'.format(round(middle, 3))
    # b_string = '[{0:.2f} - {1:.2f}]'.format(bin_range[b], bin_range[b+1])
    mid_points.append(middle)
    bar_strings.append(calc)
        
    
if all_one == 1: 
    ########## this one does not have the new image formatting - need to update
    ## Importing the data --------------------------------------------------------
    os.chdir('../final_simulations/fil_no_steric_tread')
    curve_dict = {}
    fil_legend = []
    for x in sorted(os.listdir()):
        if x.startswith('run'): 
            run_num = int(x[-4:]) 
            if run_num%2 == 1:
                os.chdir(x)
                curve = pd.read_excel("histogram_curve.xlsx")
                curve_dict[curve.columns.values[1]] = curve.iloc[:,1]
                fil_legend.append(int(curve.columns.values[1][0:4]))
                os.chdir('..')
        
    ## Plot all of the curves against each other ---------------------------------
    final_counts = plt.figure(figsize=(9,9))
    for key in curve_dict:
        plt.plot(mid_points, curve_dict[key])
        ttl = key[16:]
    plt.title(ttl, fontsize = 25)
    plt.legend(fil_legend, title = 'Filament Count', fontsize = 18)
    plt.xlabel('R [μm]', fontsize=23)
    plt.ylabel('PDF of Actin Density', fontsize=23)
    plt.xticks(fontsize = 18, rotation = 90)
    plt.yticks(fontsize = 18)
    final_counts.savefig('curve_per_folder', bbox_inches='tight')


else:
    ## Set some parameters:
    folders = ['fil_tread', 'fil_no_steric_tread', 'fil_no_steric_incorrect_act_fil', 'fil_no_steric']
    num_filaments = 500
    to_folder = int((num_filaments-100) / 100) ################################# specific to these folders - change if applying to different data 
    
    ## Importing the data --------------------------------------------------------
    os.chdir('../final_simulations')
    curve_dict = {}
    fil_legend = []
    for x in sorted(os.listdir(), reverse=True):
        if x in folders: 
            os.chdir(x)
            print(x)
            for x in sorted(os.listdir()):
                if x.endswith(str(to_folder)): 
                    os.chdir(x)
                    print(x)
                    curve = pd.read_excel("histogram_curve.xlsx")
                    curve_dict[curve.columns.values[1]] = curve.iloc[:,1]
                    fil_legend.append(curve.columns.values[1][15:])
                    os.chdir('..')  
            os.chdir('..')
            
    ## Plot all of the curves against each other ---------------------------------
    final_counts, ax = plt.subplots(figsize=(10, 10))
    # final_counts = plt.figure(figsize=(9,9))
    counter = 0 
    for key in curve_dict:
        if counter % 2 == 1:
            ax.plot(mid_points, curve_dict[key], color = colors[counter], linestyle='dashed')
        else:
            ax.plot(mid_points, curve_dict[key], color = colors[counter])
        counter += 1
    ttl = '{} Actin Filaments'.format(num_filaments)
    # ax = final_counts.add_subplot(121)
    plt.title(ttl, fontsize = 28)
    ax.legend(fil_legend, fontsize = 22)
    plt.xlabel('R [μm]', fontsize=28)
    plt.ylabel('PDF of Actin Density', fontsize=28)
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    ax.set_ylim([0, 3.3])
    fig_name = 'curve_combined_{}'.format(num_filaments)
    final_counts.savefig(fig_name, bbox_inches='tight')


    

        

