## CTBP-REU-Cytosim - Lilly Roelofs - 08/5/2022

## Synopsis 
This repository contains Cytosim configurations files and python text parsing/data analysis scripts that I developed during my time in the FiS REU summer program. My project
was focused around building computational simulations of actin fibers and their associated binding proteins in an effort to study the mechanical/dynamic properites of 
actin networks. The motivation behind this work was to better characterize the expansion/collapsing of the cytoskeleton in dendritic spines, which is known to affect learning 
and memory processes. I used [Cytosim](https://gitlab.com/f-nedelec/cytosim/-/tree/14672a7532ea4f275114e94520df53758e84a259), a cytoskeleton based simulation platform, to conduct my experiments. I developed python scripts to parse Cytosim's output files, and 
conducted data analysis on the results. 

## Description of files/folders in CTBP-REU-Cytosim Repo:

**Final_Poster_Lilly_Roelofs_2.pdf** - This the poster I created for our end-of-the-program presentations. The scripts below directly created the figures and data analysis in this poster.

### Python_Files Folder

**bash_scripts.py** - Creates a bash script per folder to run the Cytosim configuration file on a SLURM computer cluster. Automatically varies the time allocation by reading the configuration file and adding additional time based on the varied parameter value. 

**images2movie.py** - Turns a sequence of images into a movie and saves it to the specified folder. An option is provided to apply this to multiple folders in a directory.

**distance_segmentation.py** - Parses one of Cytosim's output files, fiber_point.txt, to extract the distance from the center for each point on each fiber in every frame. Uses this information to create a histogram representing the frequencies of the fiber point's distance. These frequencies are 4*pi*(r2^3 - r1^3) normalized, bar plotted, then exported to an excel sheet (histogram_curve.xlsx)

**compare_hist_curves_filaments.py** - Plots the PDF of actin density against the radius (distance from center). Considers treadmilling vs no treadmilling and steric vs no steric interactions.  The input of this script, histogram_curve.xlsx, is produced by distance_segmentation.py.

**compare_hist_curves_cross.py** - Plots the PDF of actin density against the radius (distance from center). Considers varying numbers of crosslinkers [0, 250, 500, 750, 1000]. The input of this script, histogram_curve.xlsx, is produced by distance_segmentation.py.

**circle_heatmap.py** - Creates a circular heatmap from the histogram of the filament density along the radius of the simulation space. The input of this function, histogram_curve.xlsx, is produced by *distance_segmentation.py*. This file normalizes the color bar across all plots, and it provides 2 simulation options: filament simulations, crosslinker simulations.

 **read_fiber_confinement.py** - Parses the Cytosim output file fiber_confinement.txt to extract the cumulative force applied by the fibers against the simulation boundary per frame. Has an option to normalize the force by the number of actin filaments. Plots the fiber confinement force against time. Exports the total mean fiber confinement with the bootstrapped lower/upper confidence intervals as an excel sheet (output_divided.xlsx or output.xlsx). 
 
**compare_fiber_confinement_filaments_ALL.py** - Plots the mean fiber confinement pressure against the number of actin filaments including error bars. Considers treadmilling vs no treadmilling and steric interactions vs no steric. The input of this script, output.xlsx/output_divided.xlsx, is produced by read_fiber_confinement.py.

**compare_fiber_confinement_cross.py** - Plots the mean fiber confinement pressure against the number of crosslinkers including error bars. Considers varying numbers of actin filaments [250, 500, 750, 1000]. The input of this script, output.xlsx/output_divided.xlsx, is produced by read_fiber_confinement.py.

### Cytosim Configuration Files Folder

This folder contains examples of a few of the configuration files I created for my simulations. Further details can be found in the files, and documentation for these can be found on the Cytosim gitlab page linked above. 
