# -*- coding: utf-8 -*-
"""
Created on Mon May 25 18:06:52 2020

@author: jampi
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
        cut_index = cut[3]
        del(cut_list[cut_index])
        
        #Set value of areas to -1 in case one option isn't ran
        area1 = -1
        area2 = -1
        
        new_cut_list_2 = [i for i in cut_list]
        new_cut_pieces_2 = [i for i in cut_pieces]
        
        #Determine possible orientations:
        if cut[0]<remainder[0] and cut[1]<remainder[1]:
            #If orientation possible, determine which cut order results in larger remainder
            best_remainder_1 = best_cut_order((cut[0],cut[1]),(remainder[0],remainder[1]))
            
            #get list of cuts from remainder
            new_cut_list_1, new_cut_pieces_1 = remainder_cut(cut_list,best_remainder_1,cut_pieces)
            
            #get area of cut cut pieces
            area1 = sum([i[2] for i in new_cut_pieces_1])
            print(area1)
        
        if cut[0]<remainder[1] and cut[1]<remainder[0]:
            #If orientation possible, determine which cut order results in larger remainder
            best_remainder_2 = best_cut_order((cut[1],cut[0]),(remainder[0],remainder[1]))
            
            #get list of cuts from remainder
            new_cut_list_2, new_cut_pieces_2 = remainder_cut(cut_list,best_remainder_2,cut_pieces)
            
            #get area of cut cut pieces
            area2 = sum([i[2] for i in new_cut_pieces_2])
            print(area2)
        
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
     
if __name__ == '__main__':
    test_cut_list = [[1,1,1],[1,2,2],[2,3,6],[1,1,1],[5,4,20],[3,4,12]]
    test_piece_size = (6,7)
    output_1, output_2 = remainder_cut(test_cut_list,test_piece_size)
    print(output_1)
    print(output_2)
     