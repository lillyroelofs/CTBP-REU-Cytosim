## CTBP-REU-Cytosim - Lilly Roelofs - 08/5/2022

## Synopsis 
This repository contains Cytosim configurations files and python text parsing/data analysis scripts that I developed during my time in the FiS REU summer program. My project
was focused around building computational simulations of actin fibers and their associated binding proteins in an effort to study the mechanical/dynamic properites of 
actin networks. The motivation behind this work was to better characterize the expansion/collapsing of the cytoskeleton in dendritic spines, which is known to affect learning 
and memory processes. I used [Cytosim](https://gitlab.com/f-nedelec/cytosim/-/tree/14672a7532ea4f275114e94520df53758e84a259), a cytoskeleton based simulation platform, to conduct my experiments. I developed python scripts to parse Cytosim's output files, and 
conducted data analysis on the results. 

## Description of files/folders in CTBP-REU-Cytosim Repo:

### Python_Files Folder

**bash_scripts.py** - Creates a bash script per folder to run the Cytosim configuration file on a SLURM computer cluster. Automatically varies the time allocation by reading the configuration file and adding additional time based on the varied parameter value. 

**images2movie.py** - Turns a sequence of images into a movie and saves it to the specified folder. An option is provided to apply this to multiple folders in a directory.

**distance_segmentation.py** - Parses one of Cytosim's output files, fiber_point.txt, to extract the distance from the center for each point on each fiber in every frame. Uses this information to create a histogram representing the frequencies of the fiber point's distance. These frequencies are 4*pi*(r2^3 - r1^3) normalized, bar plotted, then exported to an excel sheet (histogram_curve.xlsx)

**circle_heatmap.py** - Creates a circular heatmap from the histogram of the filament density along the radius of the simulation space. The input of this function, histogram_curve.xlsx, is produced by *distance_segmentation.py*. This file normalizes the color bar across all plots, and it provides 2 simulation options: filament simulations, crosslinker simulations.
