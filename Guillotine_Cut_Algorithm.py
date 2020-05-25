# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:18:44 2020

@author: jampi
"""

import csv
import numpy as np

#Function to cut eva
def cut_eva(EVA_width, cut_list,cut_pieces = [],EVA_consumption_length = 0):
    if len(cut_list) > 0:
        #Track order to cut pieces in
        cut_pieces.append(cut_list[-1])
        
        #Calculate EVA consumption by adding to consumed length
        EVA_consumption_length+=cut_list[-1][0]
        
        #calculate remainder length after cut is made
        if cut_list[-1][0] < EVA_width-cut_list[-1][1]:
            remainder = (cut_list[-1][0], EVA_width-cut_list[-1][1])
        else:
            remainder = EVA_width-cut_list[-1][1], (cut_list[-1][0])
        
        #Cut from remainder using other function
        print(cut_list[-1])
        (cut_list,cut_pieces) = cut_remainder(remainder,cut_list[0:-1],cut_pieces)
        
        #Recurse with remaining uncut pieces
        return cut_eva(EVA_width,cut_list,cut_pieces,EVA_consumption_length)
    
    else:
        return (cut_pieces, EVA_consumption_length)

def cut_remainder(remainder, cut_list, cut_pieces):
    
    #Create empty set list for potentials
    potentials = []
    
    #iterate through uncut pieces and find which ones fit into the remainder
    for x in range(len(cut_list)):
        if cut_list[x][1] <= remainder[1] and cut_list[x][0] <= remainder[0]:
            potentials.append([cut_list[x][0], cut_list[x][1], cut_list[x][2], x])
    
    if len(potentials) >0:
        #decide which piece to cut by pulling the maximum area piece that fits
        cut = max(potentials, key = lambda x: x[2])
        
        #add the piece to the cut list and delete it from the uncut list
        cut_pieces.append(cut[0:-1])
        del cut_list[cut[-1]]            
 
        #calculate new remainder and recurse--not done yet
       
    return cut_list, cut_pieces


#Cut piece from remnant

#Remove piece from too-cut list

#Recurse remnants until no pieces fit

#Knowns: EVA width
EVA_width=87.0

#####Bring in CSV Data#######

#Save out raw glass data in qty, size, size format. Assumes file collumns are qty, size, size
with open('Glass Block Sizes.csv', newline = '') as glass_sizes_file:
    sizereader = csv.reader(glass_sizes_file ,dialect='excel',delimiter = ',', quotechar = '"')
    glass_data = []
    for x in sizereader:
        for y in range(len(x)):
            try:
                if y == 0:
                    x[y]=int(x[y])
                else:
                    x[y]=float(x[y])
            except:
                pass
        if type(x[1]) == float:
            glass_data.append(x)

#Make a list with one block size on each line aand remove qty column      
glass_block_sizes = []
k = 0
for x in glass_data:
    k+=x[0]
    for y in range(x[0]):
        glass_block_sizes.append(x[1:])

if k != len(glass_block_sizes):
    print('ERROR! Input count does not match output list length')

#sort glass sizes into short then long

glass_block_sizes_ordered = []

for x in glass_block_sizes:
    if x[0] < x[1]:
        glass_block_sizes_ordered.append(x)
    else:
        glass_block_sizes_ordered.append([x[1],x[0]])

#Order points by width
glass_block_sizes_sorted = sorted(glass_block_sizes_ordered, key=lambda x: x[0])

#Eliminate points with dimensions greater than EVA width
points_to_delete = []
oversized_piece_sizes = []
for x in range(len(glass_block_sizes_sorted)):
    if glass_block_sizes_sorted[x][1] > EVA_width:
        points_to_delete.append(x)
        oversized_piece_sizes.append(glass_block_sizes_sorted[x])

for x in reversed(points_to_delete):
    del glass_block_sizes_sorted[x]

#Print out eliminated points into other large cut csv

#Add area to points
for x in glass_block_sizes_sorted:
    x.append(x[0]*x[1]/144)

#Make new list and duplicate entries for 2 required layerss of EVA
EVA_cut_list = []
for x in glass_block_sizes_sorted:
    EVA_cut_list.append(x)
    EVA_cut_list.append(x)

#Calculate total area of remaining points
required_EVA_area = 0
for x in EVA_cut_list:
    required_EVA_area += x[-1]

#Duplicate list into a to-cut list
to_cut_list = []

for x in EVA_cut_list:
    to_cut_list.append(x)

    
#Recurse cutting using below function
(cut_pieces, EVA_consumption_length) = cut_eva(EVA_width,to_cut_list)

    
#Calculate theoretical yield
Yield = required_EVA_area/(EVA_consumption_length*EVA_width/144)    

print(Yield)
cut_pieces
    
    
    
