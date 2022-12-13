#!/usr/bin/env python3

"""
Lilly Roelofs - 6/15/2022

Turning a sequence of images into a movie!
"""

from moviepy.editor import *
import os

# images -> movie function 
def im2mov(directory, folder_name):
    clips = []
    for filename in directory:
        # print(filename)
        if filename.endswith(".png") and filename.startswith('mov'):
            clips.append(ImageClip(filename).set_duration(0.15))
    # print(clips)
    video = concatenate(clips, method="compose")
    mov_name = folder_name + '.mp4'
    video.write_videofile(mov_name, fps=24)

# change current directory
name_of_directory = 'fil_tread' 
os.chdir('../final_simulations/' + name_of_directory)
# print(sorted(os.listdir()))

# if I want to create movies from a number of folders in a directory, MULTIPLE = 1 
MULTIPLE = 1

if MULTIPLE == 1: 
    # running through all of the simulations in a folder
    for x in sorted(os.listdir()):
        if x.startswith('run'):
            os.chdir(x)
            im2mov(sorted(os.listdir()), x)
            os.chdir('..')
else: # if I want to create movies from a single folder (which is the current directory specified on line 25)
    im2mov(sorted(os.listdir()), name_of_directory)


# Extra: 
    # listing the files/folders in this directory
    # print(sorted(os.listdir('.')))