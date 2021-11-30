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
    section_numbers = max([i[4] for i in array])
    
    #fill out output array with empty arrays for appending
    for i in range(section_numbers+1):
        split_arrays.append([])
    print(len(split_arrays))
    
    #Sort data into its proper slot
    for i in array:
        if marks == True:
            split_arrays[i[4]].append([i[0],i[1],i[3],i[5]])
        else:
            split_arrays[i[4]].append([i[0],i[1],i[5]])
    
    return split_arrays

def plot_array_generator(box_sizes, EVA_width):
    plot_points_x = []
    plot_points_y = []
    
    label_locations = []
    
    x_spacer = 0
    y_spacer = 0
    
    #vars for tracking remainder area
    Area_1 = -1
    Area_2 = -1
    
    #vars for tracking remainder height and width
    rem_x = -1
    rem_y = -1
    
    k = 0
    
    for i in box_sizes:
        #The first one goes at 0,0 no matter what. No area considerations needed
        if k == 0:
            #set up for orientation 0
            if i[-1] == 0:
                plot_points_x.append((x_spacer,i[0]+x_spacer,i[0]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((0,0,i[1],i[1],0))
                label_locations.append((i[0]/2+x_spacer ,i[1]/2,0))
                
                #Calculate remainder size
                rem_x = EVA_width - i[0]
                rem_y = i[1]
                
                #calculate spacers
                x_spacer += i[0]+2
                
            #set up for orientation 1
            if i[-1] == 1:
                plot_points_x.append((x_spacer,i[1]+x_spacer,i[1]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((0,0,i[0],i[0],0))
                label_locations.append((i[1]/2+x_spacer ,i[0]/2,1))
                
                #Calculate remainder size
                rem_x = EVA_width - i[1]
                rem_y = i[0]
                
                #calculate spacers
                x_spacer += i[1]+2
            k+=1
        
        elif k == 1:
            if i[-1] == 0:
                plot_points_x.append((x_spacer,i[0]+x_spacer,i[0]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((0,0,i[1],i[1],0))
                label_locations.append((i[0]/2+x_spacer ,i[1]/2,0))
                
                #Calculate remainder size
                rem_x_1 = rem_x - i[0]
                rem_y_1 = rem_y - i[1]
                Area_1 = rem_x_1*rem_y
                Area_2 = rem_y_1*rem_x
                
                #calculate spacers
                if Area_1 < Area_2:
                    y_spacer += i[1] + 2
                else:
                    x_spacer += i[0]+2
                
            if i[-1] == 1:
                plot_points_x.append((x_spacer,i[1]+x_spacer,i[1]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((0,0,i[0],i[0],0))
                label_locations.append((i[1]/2+x_spacer ,i[0]/2,1))
                
                #Calculate remainder size
                rem_x_1 = rem_x - i[1]
                rem_y_1 = rem_y - i[0]
                Area_1 = rem_x_1*rem_y
                Area_2 = rem_y_1*rem_x
                
                #calculate spacers
                if Area_1 < Area_2:
                    y_spacer += i[0] + 2
                else:
                    x_spacer += i[1]+2
            k+=1
        
        else:
            if i[-1] == 0:
                plot_points_x.append((x_spacer,i[0]+x_spacer,i[0]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((y_spacer,y_spacer,y_spacer + i[1],y_spacer + i[1],y_spacer))
                label_locations.append((i[0]/2+x_spacer ,y_spacer + i[1]/2,0))
                
                #Calculate remainder size
                rem_x_1 = rem_x - i[0]
                rem_y_1 = rem_y - i[1]
                Area_1 = rem_x_1*rem_y
                Area_2 = rem_y_1*rem_x
                
                #calculate spacers
                if Area_1 < Area_2:
                    y_spacer += i[1] + 2
                else:
                    x_spacer += i[0]+2
                
            if i[-1] == 1:
                plot_points_x.append((x_spacer,i[1]+x_spacer,i[1]+x_spacer,x_spacer,x_spacer))
                plot_points_y.append((y_spacer,y_spacer,y_spacer + i[0],y_spacer + i[0],y_spacer))
                label_locations.append((i[1]/2+x_spacer ,y_spacer + i[0]/2,1))
                
                #Calculate remainder size
                rem_x_1 = rem_x - i[1]
                rem_y_1 = rem_y - i[0]
                Area_1 = rem_x_1*rem_y
                Area_2 = rem_y_1*rem_x
                
                #calculate spacers
                if Area_1 < Area_2:
                    y_spacer += i[0] + 2
                else:
                    x_spacer += i[1]+2
            k+=1
    
    
    """
    for i in box_sizes:
        plot_points_x.append((x_spacer,i[0]+x_spacer,i[0]+x_spacer,x_spacer,x_spacer))
        plot_points_y.append((0,0,i[1],i[1],0))
        label_locations.append((i[0]/2+x_spacer ,i[1]/2))
        x_spacer += i[0]+2
    """
    
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
        if label_locations[i][2] == 0:
            plt.text(text_x,text_y,label,horizontalalignment = 'center',verticalalignment = 'center',rotation = 90, fontsize=fontsize)
        elif label_locations[i][2] == 1:
            plt.text(text_x,text_y,label,horizontalalignment = 'center',verticalalignment = 'center',rotation = 0, fontsize=fontsize)
    
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

def plot_and_save(EVA_width, split_array, main_cuts, marks = True, filename = 'Test.pdf', fontsize=10):
    #Generate arrays for stoing data
    plot_arrays_x = []
    plot_arrays_y = []
    label_points = []
    
    #Split data from each major cut section into formats for plotting
    for i in split_array:
        x,y,label = plot_array_generator(i, EVA_width)
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


if __name__ == "__main__":
    
    "Plot and save function torn out and ran on its own"
    
    split_array = [[[28.0, 74.0, '', 0], [28.0, 74.0, '', 0], [28.0, 74.0, '', 0]],            
                  [[28.0, 74.0, '', 0], [28.0, 74.0, '', 0], [28.0, 74.0, '', 0]],
                  [[28.0, 74.0, '', 0], [28.0, 74.0, '', 0], [28.0, 74.0, '', 0]],
                  [[28.0, 74.0, '', 0], [28.0, 74.0, '', 0], [28.0, 74.0, '', 0]],
                  [[28.0, 74.0, '', 0], [28.0, 74.0, '', 0], [28.0, 74.0, '', 0]],
                  [[28.0, 74.0, '', 1]],
                  [[25.0, 56.0, '', 0], [25.0, 56.0, '', 1], [25.0, 56.0, '', 1]],
                  [[25.0, 56.0, '', 0], [25.0, 56.0, '', 1], [25.0, 56.0, '', 1]],
                  [[25.0, 56.0, '', 0], [25.0, 56.0, '', 1], [25.0, 56.0, '', 1]],
                  [[25.0, 56.0, '', 0], [25.0, 56.0, '', 1], [25.0, 56.0, '', 1]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 0], [25.0, 37.0, '', 0], [25.0, 37.0, '', 0]],
                  [[25.0, 37.0, '', 1]]]
    main_cuts = [74.0,
                 74.0,
                 74.0,
                 74.0,
                 74.0,
                 28.0,
                 56.0,
                 56.0,
                 56.0,
                 56.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 37.0,
                 25.0]
    marks = True
    filename = 'TM Test.pdf'
    fontsize = 18
    EVA_width = 86.6
    
    #Generate arrays for stoing data
    plot_arrays_x = []
    plot_arrays_y = []
    label_points = []
    
    #Split data from each major cut section into formats for plotting
    for i in split_array:
        x,y,label = plot_array_generator(i,EVA_width)
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    