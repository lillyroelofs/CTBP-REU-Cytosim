# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:28:12 2022

Plotting the fiber confinement graphs for treadmilling/no treadmilling with error bars
"""
# Import libraries 
import pandas as pd 
import matplotlib.pyplot as plt

## Establish parameters
divide_by_num = 0 # 0 = do not divide by the total number of filaments, 1 = yes, divide by the total number of filaments 
legend = ['Treadmilling + Steric', 'Treadmilling + No Steric', 'No Treadmilling + Steric', 'No Treadmilling + No Steric']
colors = ['#225F99','#2E6917']



## Read in the CSV's we are interested in. For right now, this will be done manually 

# FOR FILE SYSTEM AT SCHOOL 
if divide_by_num == 1:
    treadmill_steric = pd.read_excel('~/cytosim/final_simulations/fil_tread/output_divided.xlsx')
    no_treadmill_steric = pd.read_excel('~/cytosim/final_simulations/fil/output_divided.xlsx')
    treadmill_no_steric = pd.read_excel('~/cytosim/final_simulations/fil_no_steric_tread/output_divided.xlsx')   
    no_treadmill_no_steric = pd.read_excel('~/cytosim/final_simulations/fil_no_steric/output_divided.xlsx')
else: 
    treadmill_steric = pd.read_excel('~/cytosim/final_simulations/fil_tread/output.xlsx')
    no_treadmill_steric = pd.read_excel('~/cytosim/final_simulations/fil/output.xlsx')
    treadmill_no_steric = pd.read_excel('~/cytosim/final_simulations/fil_no_steric_tread/output.xlsx')   
    no_treadmill_no_steric = pd.read_excel('~/cytosim/final_simulations/fil_no_steric/output.xlsx')



## Fixing the y axis and saved figure name (based on whether we are dividing by the number of filaments)
if divide_by_num == 1:
    y_label = 'Mean Confinement Pressure [pN] / Number\n of Actin Filaments'
    plt_title = 'tread_force_chart_divided'
else:
    y_label = 'Mean Confinement Pressure [pN/μm²]'
    plt_title = 'tread_force_chart'
graph_title = 'Actin Network Force on Boundary'
    
## Declare the error bars (in this case the confidence intervals) 
treadmill_steric_err = [treadmill_steric.iloc[:,3].to_list(), treadmill_steric.iloc[:,4].to_list()]
no_treadmill_steric_err = [no_treadmill_steric.iloc[:,3].to_list(), no_treadmill_steric.iloc[:,4].to_list()]
treadmill_no_steric_err = [treadmill_no_steric.iloc[:,3].to_list(), treadmill_no_steric.iloc[:,4].to_list()]
no_treadmill_no_steric_err = [no_treadmill_no_steric.iloc[:,3].to_list(), no_treadmill_no_steric.iloc[:,4].to_list()]

num_fibs = treadmill_steric.iloc[:,1].to_list()


## Function to plot the error bars 
def error_bar(error_set, color1):
    for e in range(len(error_set[0])):
        plt.vlines(x = num_fibs[e], ymin = error_set[0][e], ymax = error_set[1][e], color = color1)
    
    
## Make the plot 
final = plt.figure(figsize=(12,10))

plt.plot(treadmill_steric.iloc[:,1], treadmill_steric.iloc[:,2], '-o', alpha=0.75, color = colors[0]) # number of actin filaments, mean fiber confinement
plt.plot(treadmill_no_steric.iloc[:,1], treadmill_no_steric.iloc[:,2], '--o', alpha=0.75, color = colors[0])
plt.plot(no_treadmill_steric.iloc[:,1], no_treadmill_steric.iloc[:,2], '-o', alpha=0.75, color = colors[1]) 
plt.plot(no_treadmill_no_steric.iloc[:,1], no_treadmill_no_steric.iloc[:,2], '--o', alpha=0.75, color = colors[1]) # number of actin filaments, mean fiber confinement

error_bar(treadmill_steric_err, colors[0])
error_bar(treadmill_no_steric_err, colors[0])
error_bar(no_treadmill_steric_err, colors[1])
error_bar(no_treadmill_no_steric_err, colors[1])

plt.xlabel('Number of Actin Filaments', fontsize=28)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
    
plt.title(graph_title, fontsize=28, y=1.02)
plt.ylabel(y_label, fontsize=28)
plt.legend(legend, fontsize = 22)
final.savefig(plt_title, bbox_inches='tight')
