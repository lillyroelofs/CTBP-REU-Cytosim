#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lilly Roelofs  - 6/15/2022
Pulling data from text file concerning fiber force against it's confinement 

Every time I apply this to a new simulation, make sure all of the text spacing is correct. Try to base it off 
of the same configuration files/report set up to avoid extracting the wrong values from the text files. 
"""


## Import libraries -----------------------------------------------------------
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import bootstrap


## File Parcing---------------------------------------------------------------- 

# disclaimers: 
# - this file parsing depends on a constant number of rows in the text file between frames!!
# - need to make sure I check the file type I'm looking at (i.e. which order parameter)
#    as well as make sure all of the values are correct for it 
# - fiber_confinement.txt will need more checking because the forces can range from 1-100's places,
#    therefore the starting/ending points for the columns may be off... i think i fixed this issue
# - if one of the controlled parameter value has more than 4 place values, will need to
#   adjust the get_params() function accordingly 
# - since the first frame has a very large amount of force, it messes up with the column spacing
#   so I changed it to start at the second frame (works fine because we wanted to start at steady state anyways )

## Setting up -----------------------------------------------------------------
folder_name = 'fil_tread'
filename = 'fiber_confinement.txt' # options: 'fiber_confinement.txt'
config_filename = 'config.cym'
MULTIPLE = 2 # MULTIPLE = 0 (only want one plot), MULTIPLE = 1 (want multiple simulation - structured with run000), 
             # MULTIPLE = 2 (multiple simulations, but organized differently)
os.chdir('../final_simulations/' + folder_name) ################################################################################## change this when i go back to linux machine 
# os.chdir('../' + folder_name)
at_equil = 50 # set frame in which a pseudo-steady state is reached
avail_stats = [np.mean, np.std] # add more here if i want
rad = 1
divide_by_sa = 1 # if 0, do not divide by the surface area, if 1, divide by the surface area (changing it from force to pressure)

## FOR FIBER_CONFINEMENT.TXT -------------------------------------------------------
t1 = 8; # SECOND starting line for time (to avoid the very large forces in first frame)
e1 = 11; # SECOND starting line for confinement (to avoid the very large forces in first frame)
t1_col = 7 # the first col number that the time starts at 
t2_col = 16 # the last col number that the time finishes at % this will work for any time of length xxxx.xxxx
e1_col = 10 # the first col number that the confinement force starts at 
total_characters = 30 # this is the TOTAL number of characters (from start to very end) for the x, y, z data 
slicer = total_characters // 3 # this calculates the number of spaces between the x, y, z position text 


## Control parameters -------------------------------------------------------
divide_by_num = 0 # 0 = do not divide by the total number of filaments, 1 = yes, divide by the total number of filaments 

# FOR ANY SIMULATIONS WITH THE TITLE FOLDER STARTING WITH "FIL" - THESE ARE ONLY FILAMENTS AND INCLUDE 10 SIMS EACH TIME 
num_control_param = 1
control_params = ['Number of Actin Filaments'] # ['Number of Actin Filaments', 'Number of Motors']
num_sims = 10 # eventually automate this (number of run???? directories)

# fOR THE SIMULATIONS IN THE FOLDER CROSS -- change line 163 to include the second parameter in the dictionary
# num_control_param = 2  #1
# control_params = ['Number of Actin Filaments', 'Number of Crosslinkers'] # ['Number of Actin Filaments', 'Number of Motors']
# num_sims = 36 # eventually automate this (number of run???? directories)

## Surface area calculation --------------------------------------------------

if divide_by_sa == 1:
    sa = 4 * np.pi * rad**2
    
## FUNCTIONS ------------------------------------------------------------------

# Read in the information from a file - specifically FIBER_CONFINEMENT.TXT
def savedata():
        with open(filename, 'r') as f:
            op = f.readlines() 
            end = len(op)
            r1 = range(t1, end, 6) # (start, stop, increment) -- for time 
            r2 = range(e1, end, 6) # -- for confinement force 
            times = []
            confs = []
            confs_combined = []
            
            for j in r1: # extracting the time 
                ti = op[j][t1_col:t2_col] # exact column spacing 
                times.append(ti)
            tot_times_np = np.array([float(t) for t in times])
            
            for i in r2: # extracting the confinment info
                # print(i)
                con_full = op[i][e1_col:e1_col + total_characters]
                con_split = list(map(''.join, zip(*[iter(con_full)]*slicer)))  # don't know how this works,found here: https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts
                con_correct= np.array([abs(float(p)) for p in con_split]) # took the absolute value here!!!!!!!!!
                con_correct_comb = np.array(np.sum([abs(float(p)) for p in con_split])) # took the sum of the absolute value of all directions!!!
                if divide_by_sa == 1:
                    con_correct_comb = con_correct_comb / sa
                confs.append(con_correct)
                confs_combined.append(con_correct_comb)
            confs_np = np.array(confs)
            confs_combined_np = np.array(confs_combined)

        return tot_times_np, confs_np, confs_combined_np
   
def get_params():
    with open(config_filename, 'r') as c:
        con = c.readlines()
        params = []
        for p in range(num_control_param):  
            param_val = float(con[p+1][2:6]) # works if the varied parameter is located in line 1 position 2...
            params.append(param_val)
        params = np.array(params)
            # all_params = np.append(all_params, np.array(param_val), axis=0)
    return params
        
def find_boot(stat_name, data):   
    bootstrap_low = []
    bootstrap_high = []
    for i in range(len(data)):
        boot_mean = bootstrap(((data[i, :]),), avail_stats[stat_name], n_resamples = 1000, random_state = 304)
        # note, the confidence interval is 95% 
        bootstrap_low.append(boot_mean.confidence_interval[0])
        bootstrap_high.append(boot_mean.confidence_interval[1])
    return bootstrap_low, bootstrap_high
        
        
if MULTIPLE == 2:
    total_times = []
    total_confs = []  
    all_params = []
    for x in sorted(os.listdir()):
        if x.startswith('run'):
            os.chdir(x)
            time_seq, confs_seq, confs_sum_seq = savedata()
            total_times.append(time_seq[at_equil:])
            total_confs.append(confs_sum_seq[at_equil:])
            
            the_params = get_params()
            all_params.append(the_params)
            os.chdir('..')
    
    # Convert to numpy arrays 
    total_times_np = np.array(total_times)
    total_confs_np = np.array(total_confs) # x axis = number of frames, y axis = number of simulations
    test_total_confs_np = total_confs_np
    all_params_np = np.array(all_params)
    
    
    # DIVIDE BY THE NUMBER OF FIBERS TO NORMALIZE (IF WE ARE VARYING ONLY THE NUMBER OF FIBERS)
    if divide_by_num == 1:
        total_confs_np= np.divide(total_confs_np, all_params_np)
        dict_fix = 'Normalized Mean Fiber Confinement'
        dict_fix_std = 'Normalized STD of Force'
        data_name = 'output_divided.xlsx'
    else:
        dict_fix = 'Mean Fiber Confinement'  
        dict_fix_std = 'STD of Force'
        data_name = 'output.xlsx'
    
    # Take the mean and standard deviation 
    total_confs_mean = np.mean(total_confs_np, 1)
    bootstrap_mean_low, bootstrap_mean_high = find_boot(0, total_confs_np) # 0 = mean
    total_confs_std = np.std(total_confs_np, 1)
    bootstrap_std_low, bootstrap_std_high = find_boot(1, total_confs_np) # 1 = std 
    
    # Show the mean and param vals 
    # Export the data as a .csv 
    
    dictionary = {control_params[0]: all_params_np[:, 0], # control_params[1]: all_params_np[:, 1],
                  dict_fix : total_confs_mean, 'Bootstrap Mean: Lower CI': bootstrap_mean_low,
                  'Bootstrap Mean: Upper CI': bootstrap_mean_high, dict_fix_std: total_confs_std,
                  'Bootstrap STD: Lower CI': bootstrap_std_low, 'Bootstrap STD: Upper CI': bootstrap_std_high
                  }
    data = pd.DataFrame(dictionary)
    data.to_excel(data_name)    
    
    # Make the plot 
    final = plt.figure(figsize=(10,8))
    for i in range(len(total_times)):
        plt.plot(total_times_np[i], total_confs_np[i], alpha=0.75)
        
    if divide_by_num == 1:
        plt_title = 'confinement_graph_divided'
        graph_title = 'Normalized Confinement Force vs. Time'
        y_label = 'Confinement Force / Number of Actin Filaments [pN]'
    else: 
        plt_title = 'confinement_graph'
        graph_title = 'Net Confinement Force vs. Time'
        y_label = 'Net Fiber Force Against Confinement [pN]'
        
    plt.legend(all_params_np[:, 0], title = control_params[0], fontsize = 15, loc=2) # this is wrong for more than 1 parameter!!!!!!
    plt.title(graph_title, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.xlabel('Time [s]', fontsize=20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    final.savefig(plt_title, bbox_inches='tight')
    
    # Make the line chart (if number of changed parameters = 1)
    if num_control_param == 1:
        fig2 = plt.figure(figsize=(10,8))
        plt.plot(all_params_np, total_confs_mean)
        
        if divide_by_num == 1:
            plt_title2 = 'confine_chart_divided'
            graph_title2 = "Normalized Mean Fiber Confinement for Varying\n Numbers of Fibers"
            y_label2 = 'Mean Confinement Pressure [pN] / Number\n of Actin Filaments'
        else: 
            plt_title2 = 'confine_chart'
            graph_title2 = "Mean Fiber Confinement for Varying Numbers of Fibers"
            y_label2 = 'Mean Confinement Pressure [pN]'
        
        plt.ylabel(y_label2, fontsize=20)
        plt.xlabel(control_params[0], fontsize=20)
        plt.xticks(fontsize = 15)
        plt.yticks(fontsize = 15)
        plt.title(graph_title2, fontsize=20)
        fig2.savefig(plt_title2, bbox_inches='tight')
        



elif MULTIPLE == 1: # Collecting data from multiple folders -- used in parallel_simulation folder
    total_times = []
    total_confs = []
    total_params = []
    for x in sorted(os.listdir()):
        if x.startswith('run'):
            os.chdir(x)
            time_seq, confs_seq, confs_sum_seq = savedata()
            total_times.append(time_seq)
            total_confs.append(confs_sum_seq)
            with open(config_filename) as c:
                c_op = c.readlines()
                param_val = c_op[1][2]             ### works if the varied parameter is located in line 1 position 2...
            total_params.append(param_val)
            os.chdir('..')
    # Show the progression through time -- double check units
    final = plt.figure(figsize=(10,8))
    for i in range(len(total_times)):
        plt.plot(total_times[i], total_confs[i], alpha=0.75)
    plt.legend(total_params, title = "Changed Parameter", fontsize = 15)
    plt.ylabel('Net Fiber Force Against Confinement [pN]', fontsize=20)
    plt.xlabel('Time [s]', fontsize=20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    final.savefig('confinement_graph', bbox_inches='tight')
    
    
    
elif MULTIPLE == 0: # if I want to create movies from a single folder (which is the current directory specified on line 15)
    time_seq, confs_seq, confs_sum_seq = savedata()
    final = plt.figure(figsize=(10,8))
    plt.plot(time_seq[at_equil:], confs_sum_seq[at_equil:], alpha=0.75)
    plt.title("Fiber Force Against Confinement", fontsize=20)
    plt.ylabel('Net Fiber Force Against Confinement [pN]', fontsize=20)
    plt.xlabel('Time [s]', fontsize=20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    final.savefig('confinement_graph', bbox_inches='tight')

    
    
    
    
    
    
    
    
    
    
    