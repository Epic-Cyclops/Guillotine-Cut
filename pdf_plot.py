# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:28:17 2020

@author: jampi
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def array_page_split(array, marks = True):
    split_arrays = []
    
    #Number of sections calulcator
    section_numbers = max([i[-1] for i in array])
    
    #fill out output array with empty arrays for appending
    for i in range(section_numbers+1):
        split_arrays.append([])
    print(len(split_arrays))
    
    #Sort data into its proper slot
    for i in array:
        if marks == True:
            split_arrays[i[-1]].append([i[0],i[1],i[3]])
        else:
            split_arrays[i[-1]].append(i[0:2])
    
    return split_arrays

def plot_array_generator(box_sizes):
    plot_points_x = []
    plot_points_y = []
    
    label_locations = []
    
    x_spacer = 0
    
    for i in box_sizes:
        plot_points_x.append((x_spacer,i[0]+x_spacer,i[0]+x_spacer,x_spacer,x_spacer))
        plot_points_y.append((0,0,i[1],i[1],0))
        label_locations.append((i[0]/2+x_spacer ,i[1]/2))
        x_spacer += i[0]+2
    
    return (plot_points_x, plot_points_y, label_locations)
        
def plot_boxes(x_points,y_points,label_locations, labels, title = 'Placeholder', fontsize = 10):
    fig = plt.figure(figsize=(11,8.5))
    plt.title(title, fontsize=fontsize)
    plt.axis('off')
    plt.axis('equal')
    for i in range(len(x_points)):
        plt.plot(x_points[i],y_points[i])
        text_x = label_locations[i][0]
        text_y = label_locations[i][1]
        label = labels[i]
        plt.text(text_x,text_y,label,horizontalalignment = 'center',verticalalignment = 'center',rotation = 90, fontsize=fontsize)
    
    return fig

def pdf_save(figure_array, filename = 'Test.pdf'):
    with PdfPages(filename) as pdf:
        for i in figure_array:
            pdf.savefig(i)
    return

def label_generator(box_sizes, marks = True):
    labels = []
    for i in box_sizes:
        labels.append([])
        for j in i:
            if marks == False:
                label_string = str(j[0]) + ' in. x ' + str(j[1]) + ' in.'
            else:
                label_string = j[2] + '\n' + str(j[0]) + ' in. x ' + str(j[1]) + ' in.'
            labels[-1].append(label_string)
    return labels

def plot_and_save(split_array, main_cuts, marks = True, filename = 'Test.pdf', fontsize=10):
    #Generate arrays for stoing data
    plot_arrays_x = []
    plot_arrays_y = []
    label_points = []
    
    #Split data from each major cut section into formats for plotting
    for i in split_array:
        x,y,label = plot_array_generator(i)
        plot_arrays_x.append(x)
        plot_arrays_y.append(y)
        label_points.append(label)
    
    #Generate plot labels
    plot_labels = label_generator(split_array, marks)
    
    #Create array for storing figures
    figures = []
    
    #Create and append all of the figures to the 
    for i in range(len(label_points)):
        figure_title = 'Ripper #' + str(i+1) + ': ' + str(main_cuts[i]) + ' in.'
        figures.append(plot_boxes(plot_arrays_x[i], plot_arrays_y[i], label_points[i], plot_labels[i], figure_title, fontsize))
    
    #save it all out as a pdf
    pdf_save(figures, filename)
        