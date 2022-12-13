#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:10:53 2022

@author: lmr15
"""

# Automating bash scripts in python for varying parameters of cytosim simulations

# load in libraries
import os

# move into correct path
os.chdir('../simulations/week8_nots')
config_filename = 'config.cym'
num_control_param = 2

# dictionary of param values and additional times associated with it 
# keys = param val, values = amount of time to add
param2time = {500: 1, 1000: 2}

# function to extract the varying parameter values  
def get_params():
    with open(config_filename, 'r') as c:
        con = c.readlines()
        add_time = 0
        for p in range(num_control_param):  
            param_val = float(con[p+1][2:6]) # works if the varied parameter is located in line 1 position 2...
            if param_val in param2time.keys():
                time2add = param2time.get(param_val)
                add_time += time2add
    return add_time


for x in sorted(os.listdir()):
    if x.startswith('run'):
        base_time = 3 # setting the minimum amount of time for the simulation to run
        os.chdir(x)
        additional = get_params()
        base_time += additional 
        with open ('parallel.sh', 'w') as rsh:
            rsh.write('''#! /bin/bash
#SBATCH --ntasks=1
#SBATCH --time={}:00:00
#SBATCH --partition=commons
#SBATCH --mail-user=lmr15@rice.edu
#SBATCH --mail-type=BEGIN

/home/lmr15/cytosim_nots/bin/sim config.cym
/home/lmr15/cytosim_nots/bin/report fiber:confinement > fiber_confinement.txt 
/home/lmr15/cytosim_nots/bin/report fiber:points > fiber_point.txt 
            '''.format(base_time))
        os.chdir('..')
