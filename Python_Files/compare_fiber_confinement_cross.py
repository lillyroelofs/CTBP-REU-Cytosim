# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:28:12 2022

Plotting the fiber confinement graphs for treadmilling/no treadmilling with error bars
THIS ONE HAS BEEN EDITED TO PLOT NUMBER OF CROSSLINKERS AND ACTIN FILAMENTS
"""
# Import libraries 
import pandas as pd 
import matplotlib.pyplot as plt

# Establish parameters
case = 3
for_cross = 1 # this is the column we index the treadmill variable for the x axis
divide_by_num = 0 # 0 = do not divide by the total number of filaments, 1 = yes, divide by the total number of filaments 
legend = ['250', '500', '750', '1000']
colors = ['#358299', '#BD9848', '#AD81DB', '#2D8F1E']

# Read in the CSV's we are interested in. For right now, this will be done manually 
# Make this whole script more efficient later!!
if divide_by_num == 1:
    fil_250 = pd.read_excel('../final_simulations/cross/output_divided_250_new.xlsx')
    fil_500 = pd.read_excel('../final_simulations/cross/output_divided_500_new.xlsx')
    fil_750 = pd.read_excel('../final_simulations/cross/output_divided_750_new.xlsx')
    fil_1000 = pd.read_excel('../final_simulations/cross/output_divided_1000_new.xlsx') 
else: 
    fil_250 = pd.read_excel('../final_simulations/cross/output_250_new.xlsx')
    fil_500 = pd.read_excel('../final_simulations/cross/output_500_new.xlsx')
    fil_750 = pd.read_excel('../final_simulations/cross/output_750_new.xlsx')
    fil_1000 = pd.read_excel('../final_simulations/cross/output_1000_new.xlsx')
    
if divide_by_num == 1: 
    graph_title = "Mean Fiber Confinement for \nVarying Numbers of Filaments"
    y_label = 'Mean Confinement Force [pN] / Number\n of Actin Filaments'
    plt_title = 'force_chart_divided'
else:
    graph_title = "Actin Network Force on Boundary"
    y_label = 'Mean Confinement Pressure [pN/μm²]'
    plt_title = 'force_chart'


# Declare the error bars (in this case the confidence intervals) 
fil_250_error = [fil_250.iloc[:,3].to_list(), fil_250.iloc[:,4].to_list()]
fil_500_error = [fil_500.iloc[:,3].to_list(), fil_500.iloc[:,4].to_list()]
fil_750_error = [fil_750.iloc[:,3].to_list(), fil_750.iloc[:,4].to_list()]
fil_1000_error = [fil_1000.iloc[:,3].to_list(), fil_1000.iloc[:,4].to_list()]
num_cross = fil_250.iloc[:,1].to_list()

# Function to plot the error bars 
def error_bar(error_set, color1):
    for e in range(len(error_set[0])):
        plt.vlines(x = num_cross[e], ymin = error_set[0][e], ymax = error_set[1][e], color = color1)
    
    
# Make the plot 
final = plt.figure(figsize=(12,10))

plt.plot(fil_250.iloc[:,for_cross], fil_250.iloc[:,for_cross+1], '-o', alpha=0.75, color = colors[0]) # number of actin filaments, mean fiber confinement
plt.plot(fil_500.iloc[:,for_cross], fil_500.iloc[:,for_cross+1], '-o', alpha=0.75, color = colors[1]) # number of actin filaments, mean fiber confinement
plt.plot(fil_750.iloc[:,for_cross], fil_750.iloc[:,for_cross+1], '-o', alpha=0.75, color = colors[2]) # number of actin filaments, mean fiber confinement
plt.plot(fil_1000.iloc[:,for_cross], fil_1000.iloc[:,for_cross+1], '-o', alpha=0.75, color = colors[3]) # number of actin filaments, mean fiber confinement

error_bar(fil_250_error, colors[0])
error_bar(fil_500_error, colors[1])
error_bar(fil_750_error, colors[2])
error_bar(fil_1000_error, colors[3])

plt.xlabel('Number of Crosslinkers', fontsize=28)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
    
plt.title(graph_title, fontsize=28, y=1.02)
plt.ylabel(y_label, fontsize=28)
plt.legend(legend, title = 'Filament Count', fontsize = 20, loc=3)
final.savefig(plt_title, bbox_inches='tight')

