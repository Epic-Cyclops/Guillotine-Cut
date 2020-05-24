# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:18:44 2020

@author: jampi
"""

import csv
import numpy as np

#Knowns: EVA width

#Bring in CSV Data

#Create dimension points

#sort dimension points into short then long

#Order points by width

#Eliminate points with dimensions greater than EVA width

#Print out eliminated points into other large cut csv

#Add area to points

#Calculate total area of remaining points

#Duplicate list into a to-cut list

#Create counter variable to track length of EVA used

#Start with widest element, cut it

#Add to tracker variable for length

#Calculate remaining piece of strip size

#Remove piece from to-cut list

#Find largets piece that will come out of it from remaining piece
    #search by length
    #If l<larger dimension, check width
    #if w<smaller dimension, add to potential list
    #Find largest piece in potential list, return

#Cut piece from remnant

#Remove piece from too-cut list

#Recurse remnants until no pieces fit

#Rinse and Repeat