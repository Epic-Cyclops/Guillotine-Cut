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
        #print(cut_list[-1])
        (cut_list,cut_pieces) = remainder_cut(cut_list[0:-1], remainder, cut_pieces)
        
        #Recurse with remaining uncut pieces
        return cut_eva(EVA_width,cut_list,cut_pieces,EVA_consumption_length)
    
    else:
        return (cut_pieces, EVA_consumption_length)


"""OLD REMAINDER CUT FUNCTION
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
"""


''' This function takes in a piece size and a list of pieces to be cut from it to return an efficient layout of cut pieces'''
#The cut_list is assumed to be ordered smallest to largest piece by width
#The cut_list should be an array of 3 dimension arrays with width, length, area
#The remainder is two-dimensional tuple
def remainder_cut(cut_list,remainder, cut_pieces = []):
    #Create an empty array to track the pieces that can be cut from remainder
    potentials = []
    
    #Find which pieces fit into remainder
    for x in range(len(cut_list)):
        if (cut_list[x][1] <= remainder[1] and cut_list[x][0] <= remainder[0]) or (cut_list[x][0] <= remainder[1] and cut_list[x][1] <= remainder[0]):
            potentials.append([cut_list[x][0], cut_list[x][1], cut_list[x][2],x])
    
    #If no pieces can be cut from the remainder, return the input data except remainder
    if potentials == []:
        return (cut_list, cut_pieces)
    
    #If there are potential cuts:
    else:
        #Cut the largest piece from the remainder
        cut = max(potentials, key = lambda x: x[2])
        cut_pieces.append(cut[0:3])
        #print('CUT!' +str(cut[0:3]))
        cut_index = cut[3]
        del(cut_list[cut_index])
        
        #Set value of areas to -1 in case one option isn't ran
        area1 = -1
        area2 = -1
        
        new_cut_list_2 = [i for i in cut_list]
        new_cut_pieces_2 = [i for i in cut_pieces]

        
        #Determine possible orientations:
        if cut[0]<=remainder[0] and cut[1]<=remainder[1]:
            #print('ORIENTATION 1')
            #If orientation possible, determine which cut order results in larger remainder
            best_remainder_1 = best_cut_order((cut[0],cut[1]),(remainder[0],remainder[1]))
            #print('Orientation 1 remainder: ' + str(best_remainder_1))
            
            #get list of cuts from remainder
            new_cut_list_1, new_cut_pieces_1 = remainder_cut(cut_list,best_remainder_1,cut_pieces)
            
            #get area of cut cut pieces
            area1 = sum([i[2] for i in new_cut_pieces_1])
            #print(new_cut_pieces_1)
            #print('Already cut area 1 is: ' + str(area1))
            
        
        if cut[0]<=remainder[1] and cut[1]<=remainder[0]:
            #print('ORIENTATION 2')
            #If orientation possible, determine which cut order results in larger remainder
            best_remainder_2 = best_cut_order((cut[1],cut[0]),(remainder[0],remainder[1]))
            #print('Orientation 2 remainder: ' + str(best_remainder_2))
            #get list of cuts from remainder
            new_cut_list_2, new_cut_pieces_2 = remainder_cut(cut_list,best_remainder_2,cut_pieces)
            
            #get area of cut cut pieces
            area2 = sum([i[2] for i in new_cut_pieces_2])
            #print(new_cut_pieces_2)
            #print('Already cut area 2 is: ' + str(area2))
            
        
        #Get the max cut of orientation and return one with largest area
        if area1>area2:
            return (new_cut_list_1, new_cut_pieces_1)
        else:
            return (new_cut_list_2, new_cut_pieces_2)

       
'''This cut determines the best order to guillotine cut a piece from a remainder to result in the largest remaining piece'''
#This function assumes the inputs are ordered        
def best_cut_order(cut,remainder):
     #Calculate two potential remainder areas
     cut_area_1 = (remainder[1]-cut[1])*remainder[0]
     cut_area_2 = (remainder[0]-cut[0])*remainder[1]
     
     #return dimensions of largest remainder piece
     if cut_area_1>cut_area_2:
         return (remainder[1]-cut[1],remainder[0])
     else:
         return (remainder[0]-cut[0],remainder[1])

#Cut piece from remnant

#Remove piece from too-cut list

#Recurse remnants until no pieces fit

#Knowns: EVA width
EVA_width=59.0

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

#Double Check sizes of arrays to make sure the oversized pieces and glass_block_sizes arrays are same total length as before points are deleted
if len(glass_block_sizes) != len(glass_block_sizes_sorted)+len(oversized_piece_sizes):
    print('ERROR! Number of to-cut pieces and oversized pieces does not match total number of pieces!')
    
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
print(len(cut_pieces))
    
    
  
