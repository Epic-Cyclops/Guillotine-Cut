# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 11:46:25 2020

@author: jampi
"""
import Guillotine_Cut_Algorithm as gc
import pdf_plot as pdf 


#Set file location and name
# filename = 'O:\Art_library\Flexi8network\Dallas Glass\Salem Police Handrail\EVA Cutting\EVA Sizes Phase 2.csv'

# pdf_filename = 'O:\Art_library\Flexi8network\Dallas Glass\Salem Police Handrail\EVA Cutting\EVA Cuts Phase 2.pdf'

filename = r'C:\Users\jampi\Desktop\EVA Cutting\Division Test Stop.csv'

pdf_filename = r'C:\Users\jampi\Desktop\EVA Cutting\Division Test Stop.pdf'

#Known variables
EVA_width = 87
marks = True
layer_count = 2

cut_pieces, EVA_consumption_length, main_cuts, EVA_cut_yield, oversized_pieces = gc.eva_cut_from_csv(filename, EVA_width, layer_count, marks)

split_cut_pieces = pdf.array_page_split(cut_pieces, marks)

pdf.plot_and_save(split_cut_pieces, main_cuts, marks, pdf_filename, fontsize=20)

#Calculate Yield
#EVA_cut_yield = gc.material_minimum(to_cut_list)/(EVA_consumption_length*EVA_width/144)
print('The yield is ' + str(round(EVA_cut_yield*100,2)) + '%.')

