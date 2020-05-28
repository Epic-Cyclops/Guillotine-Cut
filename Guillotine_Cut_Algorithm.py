# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:18:44 2020

@author: jampi
"""

import csv
import numpy as np

"""OLD #Function to cut eva
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
"""

#Function to cut eva
def cut_eva(EVA_width, cut_list,cut_pieces = [],EVA_consumption_length = 0):
    if len(cut_list) > 0:
        
        #Get total area cut so far:
        total_cut_area = sum(i[2] for i in cut_pieces)
        
        #print(str(len(cut_pieces)+len(cut_list)) + '  |  ' + str(len(cut_pieces)) + '  |  ' + str(len(cut_list)))
        #Track order to cut pieces in
        first_cut_piece = cut_list[-1]
        cut_pieces.append(first_cut_piece)
        del(cut_list[-1])
        
        #Set effficiencies to negative in case one isn't used
        efficiency_1 = -1
        efficiency_2 = -1
        
        #Try first orientation:
        if first_cut_piece[1] <= EVA_width:
            EVA_consumption_1 = first_cut_piece[0]
            
            #Calculate remainder:
            remainder_1 = (EVA_width-first_cut_piece[1],first_cut_piece[0])
            #print('Remainder 1 is: ' + str(remainder_1))
            #Cut apart remainder:
            (cut_list_1,cut_pieces_1) = remainder_cut(cut_list, remainder_1, cut_pieces)
            
            #Calculate efficiency of new cuts
            efficiency_1 = (sum(i[2] for i in cut_pieces_1)-total_cut_area)/(EVA_width*EVA_consumption_1/144)
            #print('eff 1: ' + str(round(efficiency_1,2)))
            
        #Try first orientation:
        if first_cut_piece[0] <= EVA_width:
            EVA_consumption_2 = first_cut_piece[1]
            
            #Calculate remainder:
            remainder_2 = (EVA_width-first_cut_piece[0],first_cut_piece[1])
            #print('Remainder 2 is: ' + str(remainder_2))
            
            #Cut apart remainder:
            (cut_list_2,cut_pieces_2) = remainder_cut(cut_list, remainder_2, cut_pieces)
            
            #Calculate efficiency of new cuts
            efficiency_2 = (sum(i[2] for i in cut_pieces_2)-total_cut_area)/(EVA_width*EVA_consumption_2/144)
            #print('eff 2: ' + str(round(efficiency_2,2)))
            
            
        #use most efficient cut
        if efficiency_1 > efficiency_2:
            #print('1!')
            #Calculate EVA consumption
            EVA_consumption_length+=EVA_consumption_1
            
            #Recurse with remaining uncut pieces using list 1
            return cut_eva(EVA_width,cut_list_1,cut_pieces_1,EVA_consumption_length)
        
        else:
            #print('2!')
            #Calculate EVA consumption
            EVA_consumption_length+=EVA_consumption_2

            #Recurse with remaining uncut pieces using list 1
            return cut_eva(EVA_width,cut_list_2,cut_pieces_2,EVA_consumption_length)
    
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
def remainder_cut(cut_list1,remainder, cut_pieces1 = []):
    #Create an empty array to track the pieces that can be cut from remainder
    potentials = []
    
    cut_list = [i for i in cut_list1]
    cut_pieces = [i for i in cut_pieces1]
    
    #Find which pieces fit into remainder
    for x in range(len(cut_list)):
        if (cut_list[x][1] <= remainder[1] and cut_list[x][0] <= remainder[0]) or (cut_list[x][0] <= remainder[1] and cut_list[x][1] <= remainder[0]):
            potentials.append([cut_list[x][0], cut_list[x][1], cut_list[x][2],x])
            #print('!')
    
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


"""This function grabs the data from the csv file"""
def get_data(filename = 'Glass Block Sizes.csv'):
    #Save out raw glass data in qty, size, size format. Assumes file collumns are qty, size, size
    with open(filename, newline = '') as glass_sizes_file:
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
    
    return glass_data


"""This function deletes the quantity data fom the raw csv data"""
def clear_quantity(glass_data):
    #Make a list with one block size on each line aand remove qty column      
    glass_block_sizes = []
    k = 0
    for x in glass_data:
        k+=x[0]
        for y in range(x[0]):
            glass_block_sizes.append(x[1:])
    
    if k != len(glass_block_sizes):
        print('ERROR! Input count does not match output list length')
    
    print(len(glass_block_sizes*2))
    #sort glass sizes into short then long
    
    return glass_block_sizes

"""This function takes in data, orders the points smaller dim., larger dim., then
sorts based on the smaller dimension"""
def order_and_sort(glass_block_sizes):
    glass_block_sizes_ordered = []

    for x in glass_block_sizes:
        if x[0] < x[1]:
            glass_block_sizes_ordered.append(x)
        else:
            glass_block_sizes_ordered.append([x[1],x[0]])
    
    
    #Order points by width
    glass_block_sizes_sorted = sorted(glass_block_sizes_ordered, key=lambda x: x[0])
    
    return glass_block_sizes_sorted

"""This function eliminates points that are too large to be cut from the material
and returns two arrays with the eliminated points and points to cut"""
def point_eliminate(glass_block_sizes_sorted, EVA_width):
    #Eliminate points with dimensions greater than EVA width
    points_to_delete = []
    oversized_piece_sizes = []
    for x in range(len(glass_block_sizes_sorted)):
        if glass_block_sizes_sorted[x][1] > EVA_width and glass_block_sizes_sorted[x][0] > EVA_width:
            points_to_delete.append(x)
            oversized_piece_sizes.append(glass_block_sizes_sorted[x])
    
    for x in reversed(points_to_delete):
        del glass_block_sizes_sorted[x]
    
    #Double Check sizes of arrays to make sure the oversized pieces and glass_block_sizes arrays are same total length as before points are deleted
    if len(glass_block_sizes) != len(glass_block_sizes_sorted)+len(oversized_piece_sizes):
        print('ERROR! Number of to-cut pieces and oversized pieces does not match total number of pieces!')
    
    return (glass_block_sizes_sorted,oversized_piece_sizes)

"""This function appends area to the size arrays
Assumes dims are in. and gives area in sq. ft."""
def append_area(glass_block_sizes_sorted):
    #Add area to points
    for x in glass_block_sizes_sorted:
        x.append(x[0]*x[1]/144)
        
    return glass_block_sizes_sorted

"""This function multiplies the number of gglass block size entries by the number
of layers required for each size"""
def layer_multiplier(glass_block_sizes_sorted, layer_count = 2):
    EVA_cut_list = []
    for x in glass_block_sizes_sorted:
        for y in range(layer_count):
            EVA_cut_list.append(x)
            
    return EVA_cut_list

"""This function calculates the theoretical minimum material requirement for the
cuts to be made, assuming areas are stored in the last array element """
def material_minimum(EVA_cut_list):
    return sum(i[-1] for i in EVA_cut_list)

if __name__ == '__main__':
    #Knowns: EVA width
    EVA_width=49
    layer_count = 2
    
    '''Bring in CSV Data'''
    
    glass_data = get_data('Glass Block Sizes.csv')
    
    glass_block_sizes = clear_quantity(glass_data)
    
    glass_block_sizes_sorted = order_and_sort(glass_block_sizes)
    
    glass_block_sizes_sorted, oversized_piece_sizes = point_eliminate(glass_block_sizes_sorted,EVA_width)
        
    #Print out eliminated points into other large cut csv
    
    glass_block_sizes_sorted = append_area(glass_block_sizes_sorted)
    
    #Make new list and duplicate entries for 2 required layerss of EVA
    EVA_cut_list = layer_multiplier(glass_block_sizes_sorted, layer_count)
    
    #Calculate total area of remaining points
    required_EVA_area = material_minimum(EVA_cut_list)
          
    #Recurse cutting using below function
    (cut_pieces, EVA_consumption_length) = cut_eva(EVA_width,EVA_cut_list)
    
    #Calculate theoretical yield
    Yield = required_EVA_area/(EVA_consumption_length*EVA_width/144)    
    
    print(Yield)
    print(len(cut_pieces))
    print(EVA_consumption_length/39.4)
    print(len(oversized_piece_sizes*2))
#    
    
  
#    #Knowns: EVA width
#    EVA_width=7
#    layer_count = 2
#    
#    '''Bring in CSV Data'''
#    
#    glass_data = get_data('Test.csv')
#    
#    glass_block_sizes = clear_quantity(glass_data)
#    
#    glass_block_sizes_sorted = order_and_sort(glass_block_sizes)
#    
#    glass_block_sizes_sorted, oversized_piece_sizes = point_eliminate(glass_block_sizes_sorted,EVA_width)
#        
#    #Print out eliminated points into other large cut csv
#    
#    glass_block_sizes_sorted = append_area(glass_block_sizes_sorted)
#    
#    #Make new list and duplicate entries for 2 required layerss of EVA
#    EVA_cut_list = layer_multiplier(glass_block_sizes_sorted, layer_count)
#    
#    #Calculate total area of remaining points
#    required_EVA_area = material_minimum(EVA_cut_list)
#          
#    #Recurse cutting using below function
#    (cut_pieces, EVA_consumption_length) = cut_eva(EVA_width,EVA_cut_list)
#    
#    #Calculate theoretical yield
#    Yield = required_EVA_area/(EVA_consumption_length*EVA_width/144)    
#    
#    print(Yield)
#    print(len(cut_pieces))
#    print(EVA_consumption_length/39.4)
#    print(len(oversized_piece_sizes*2))
    
    first_list = [[2,3,2*3/144] for i in range(6)]
    test_list = [[2,3,2*3/144] for i in range(6)]
    run1 = remainder_cut(test_list,(3.0,4.0))
    run2 = remainder_cut(test_list,(3.0,4.0))
    print(first_list == test_list)