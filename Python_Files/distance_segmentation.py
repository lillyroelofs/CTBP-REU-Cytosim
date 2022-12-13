#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:09:39 2022

Lilly Roelofs - Closest Boundary Point Calculation - for fiber SEGMENT positions
"""

## Import libraries

import os
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns

## Set up environment - update this everytime I change folders/simulations
# os.chdir('../fil_no_steric_tread/run0002')
folder_name = 'cross/run0035'
os.chdir('../final_simulations/' + folder_name) ################################################################################## change this when i go back to linux machine 
number_of_segments = 26 # ( fiber length / segmentation ) + 1  !!!
r = 1 # this is the radius of the sphere - used to calculate the closest distance between the point and the boundary
total_characters = 30 # this is the TOTAL number of characters (from start to very end) for the x, y, z data 
slicer = total_characters // 3 # this calculates the number of spaces between the x, y, z position text 
center = np.array([0, 0, 0]) 
bin_width = 0.05 # change the increment size according to how specific i want the bin size to be for the hist! 
bin_range = np.arange(0, r+bin_width, bin_width) 
at_equil = 50 
cross = 1 # 0 = we are not running from the cross folder, 1 = we are running from the cross folder
if cross == 0: 
    treadmilling = 0 # 0 = no treadmilling, 1 = with treadmilling 
    steric = 1 # no steric, 1= with steric 
    ttl_str = ['No ', '']
if cross == 1: # there are a few simulations that use 0 crosslinkers, which throws off the file parsing of config.cym, therefore...
    bad_folder_nums = [0, 9, 18, 27]
    

#----------------------------------------------------------------------------------------------------------
### File Parcing 

# disclaimers: 
# - this file parsing depends on a constant number of rows in the text file between frames!!
# - if the number of fibers begins to change (between frames), will have to change the way I loop through the file
# - only works for radii < 10 micrometers (otherwise will need to edit the position columns so that they read double digits for radii instead of single digits)
   # - can develop a "checker" for this at one point by reading the configuration file 
# - for right now, this 

#----------------------------------------------------------------------------------------------------------
### FOR FIBER POSITION (center of fiber) - file called "fiber_pos.txt"
filename = 'fiber_point.txt'

# rows
t1 = 2 # the first row that time starts on
p1 = 6 # the first row that the positions start on
    
# columns
t1_col = 7 # the first col number that the time starts at 
t2_col = 16 # the last col number that the time finishes at # this will work for any time of length xxxx.xxxx

p1_col = 13  # the first col number that the positions starts at 
# the second col number where the positions end is p1_col + total_characters (AKA column 43) # this will work numbers of length x.xxxx

#------------------------------------------------------------------------------------------------------------
### Getting information from config.cym 
with open('config.cym', 'r') as c:
    cop = c.readlines()
    
    # do some further variable definitions
    number_of_fibers = int(cop[1][2:6]) # this is the number of fibers in the simulation
    if cross == 1:
        run_name = int(folder_name[-2:])
        print(run_name)
        if run_name in bad_folder_nums:
            number_of_cross = int(cop[2][2:4])  # this is the number of crosslinkers in the simulation
        else:
            number_of_cross = int(cop[2][2:6])  # this is the number of crosslinkers in the simulation
        
total_elements = number_of_fibers*number_of_segments
inc = ((number_of_segments + 1) * number_of_fibers) + 5 # the number of rows between the frames
    # 5 = arbitrary number of lines between frames 
        
#------------------------------------------------------------------------------------------------------------
### Opening the file, parsing it, and organizing the data!! 

#def parsefile()   
with open(filename, 'r') as f:
    
    op = f.readlines() 
    end = len(op)
    r_time = range(t1, end, inc) # (start, stop, increment) -- for time 
    r_pos = range(p1, end, inc) # -- for positions 
    tot_times = []
    tot_pos = []
    
    for j in r_time:
        time = op[j][t1_col:t2_col] # exact column spacing 
        tot_times.append(time)
    tot_times_np = np.array([float(t) for t in tot_times])
    
    for i in r_pos: # correlates to a frame 
        per_frame = []
        for extra in range(((number_of_segments + 1) * number_of_fibers)-1): # for each fiber segment in the frame...
            if not op[i+extra].startswith('%'): # if the row does NOT start with a "%"...
                pos_full = op[i+extra][p1_col:p1_col + total_characters]
                pos_split = list(map(''.join, zip(*[iter(pos_full)]*slicer)))  # don't know how this works,found here: https://stackoverflow.com/questions/22571259/split-a-string-into-n-equal-parts
                pos_correct= np.array([float(p) for p in pos_split])
                per_frame.append(pos_correct)
        per_frame_np = np.array(per_frame)
        tot_pos.append(per_frame_np)
    tot_pos_np = np.array(tot_pos)
  
        
# parsefile()

# Only want to consider points after equilibrium!!! 
tot_times_np = tot_times_np[at_equil:]
tot_pos_np = tot_pos_np[at_equil:, :, :]

# tot_times_np = list of times 
# tot_pos_np = array of all of the positions! 


#----------------------------------------------------------------------------------------------------------
### Figuring out the numbers to divide each frequency set by... 

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
    
    
to_div_by = []
for m in range(len(bin_range)-1):
    num = (bin_range[m+1])**3 - bin_range[m]**3
    to_div_by.append(num)

# Function to find the nearest radius to the sample distance and divide by 4*pi*(r^3 - r^3)
def division_calc(frequency_list):
    vals_divided = np.divide(frequency_list,  4/3 * np.pi * np.array(to_div_by))
    return vals_divided

#-----------------------------------------------------------------------------------------------------------
### Calculating the distances from the center, applying the histogram, dividing the frequency by 4*pi*r^2

# Function to produce histograms from the data 
def save_hist(data, image, range_bins): # image = 0 for not creating a histogram image
    fig, ax = plt.subplots(figsize=(8, 6))
    values, bins, patches = ax.hist(data, bins=range_bins, color='dodgerblue', edgecolor='white')
    plt.close(fig)
    if image == 1:
        ax.set_title('Distance Histogram')
        ax.set_xlabel('Distance from Boundary') # 0 = on boundary
        ax.set_ylabel('Frequency')
        #ax.set_xticks(minor=False)
        fig.tight_layout()
        #fig.savefig("test case {}/{} cluster/Histogram - {}.png".format(run, numclusters, filename), format='png')
        plt.show(fig)
    else:
        return values, bins


# Running through each frame, fiber, and segment to calculate the distance from the center 
# Also, running each FRAME through a histogram to get the frequency of the distances and dividing the frequency by 4*pi*r^2
total_distances = []
frame_hist_vals = []
frame_hist_divided = []
for frame in range(len(tot_pos_np)): # for each frame..
    frame_distance = []
    for each_segment in range(total_elements): # for each row of the frame (for each fiber POINT)...
        frame_pos = tot_pos_np[frame,each_segment,:]
        d = np.sqrt(np.sum(np.square(frame_pos - center))) # calculating the distance from the points and the center 
        frame_distance.append(d) # frame_distance = the distance per point to the center for each frame
    frame_distance_np = np.array(frame_distance)
    f_vals, f_bins = save_hist(frame_distance_np, 0, bin_range) # calculating the histogram frequencies per frame 
    
    # need to divide each frequency number by 4*pi*r^3 
    f_vals_divided = division_calc(f_vals)
    
    # f_vals_divided = np.divide(f_vals,  4 * np.pi * np.square(mid_points)) # dividing the frequencies by 4*pi*r^2
    frame_hist_vals.append(f_vals) # the frequency per bin for each frame 
    frame_hist_divided.append(f_vals_divided) # the divided frequency per bin for each frame 
    total_distances.append(frame_distance_np) # the distance per point for ALL frames
    
# Change the completed variables to numpy arrays 
total_distances_np = np.array(total_distances) # total_distances_np = the distance from the point to the center for all points in the simulation (each point for each fiber in each frame)
frame_hist_vals_np = np.array(frame_hist_vals) # frame_hist_vals_np = the bin frequencies per frame
frame_hist_divided_np = np.array(frame_hist_divided) #frame_hist_divided_np = the bin frequencies per frame divided by 4*pi*r^3-r^3   

#-----------------------------------------------------------------------------------------------------------
### Plotting the histogram - first for the data that is not 4*pi*r^2 normalized 

# Average the bin frequency for each bin across all frames (integrating out time) 
mean_bins = np.mean(frame_hist_vals_np, 0)
# Take the area under the curve 
aoc = np.sum(mean_bins*bin_width) # multiply each mean frequency by the bin width and sum them all together
# Take the mean bin frequency and divide it by the total area under the curve
norm_mean_bin = mean_bins / aoc

final_counts = plt.figure(figsize=(13,11))
plt.bar(bar_strings, norm_mean_bin)
plt.title("WRONG GRAPH", fontsize=23, y =  1.015)
plt.xlabel('R [μm]', fontsize=23)
plt.ylabel('PDF of Actin Density', fontsize=23)
plt.xticks(fontsize = 18, rotation = 90)
plt.yticks(fontsize = 18)
# os.chdir('..')
# final_counts.savefig('mean_histograms', bbox_inches='tight')
        
        
#-----------------------------------------------------------------------------------------------------------
### Plotting the histogram - now for the frequencies that are 4*pi*r^2 normalized

# Average the bin frequency for each bin across all frames (integrating out time) 
mean_bins_div = np.mean(frame_hist_divided_np, 0)
# Take the area under the curve 
aoc_div = np.sum(mean_bins_div*bin_width) # multiply each mean frequency by the bin width and sum them all together
# Take the mean bin frequency and divide it by the total area under the curve
norm_mean_bin_div = mean_bins_div / aoc_div

final_counts_div = plt.figure(figsize=(13,11))
plt.bar(bar_strings, norm_mean_bin_div)
# plt.plot(bar_strings, norm_mean_bin_div, color='black')
if cross == 0:
    ttl_name = '{} Filaments, {}Treadmilling, {}Steric'.format(number_of_fibers, ttl_str[treadmilling], ttl_str[steric])
else:
    ttl_name = '{} Filaments, {} Crosslinkers'.format(number_of_fibers, number_of_cross)
plt.title(ttl_name, fontsize=25, y = 1.015)
plt.xlabel('R [μm]', fontsize=25)
plt.ylabel('PDF of Actin Density', fontsize=25)
plt.xticks(fontsize = 18, rotation = 90)
plt.yticks(fontsize = 18)
# os.chdir('..')
final_counts_div.savefig('mean_histograms_div', bbox_inches='tight')


# Code I am using for the histogram: (https://stackoverflow.com/questions/66837184/is-there-a-way-to-save-the-bins-from-a-histogram-in-python#:~:text=You%20can%20save%20the%20information,than%20the%20number%20of%20bars).)


#-----------------------------------------------------------------------------------------------------------
### Export a line of all of the top points on the histogram
writer = pd.ExcelWriter('histogram_curve.xlsx')
dictionary = {ttl_name: norm_mean_bin_div}
data = pd.DataFrame(dictionary)
data.to_excel(writer, sheet_name='Sheet1', startrow=0)

# data.to_excel('curves.xlsx') 
writer.save()
#-----------------------------------------------------------------------------------------------------------
### Save the "most probable" radius (r/R) value to a variable 

# ## Save the results to a file 
# kfile = open('distance_results', "w") 

# ## Most probable (mode)
# # I am defining the most probable radius as the bin with the greatest mean frequency value.
# # Also, I am using the 'normalized' (4*pi*r^2) values to do this 
# result = np.where(norm_mean_bin_div == np.amax(norm_mean_bin_div))[0][0]  # Find the position of the max frequency 
# most_probable = mid_points[result] # Get the bin value for the max frequency
# mode_str = 'The most probable r/R distance is: {}'.format(most_probable)
# print(mode_str)
# kfile.write(mode_str)

# ## Mean 
# # mean1 = np.mean(tot_pos_np, axis = 1) # Find the position of the max frequency 
# # mean_str = 'The average r/R distance is: {}'.format(most_probable)
# # (mode_str)
# # kfile.write(mode_str)

# kfile.close()

#-----------------------------------------------------------------------------------------------------------
### Create a boxplot with the data 

# bplot=sns.boxplot(y='lifeExp', x='continent', data=norm_mean_bin_div, width=0.5, palette="colorblind")

# need to fix this calculation to divide the 




