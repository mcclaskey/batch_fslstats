#!/usr/bin/env python
# -*- coding : utf-8 -*-



'''

Scripts to mask the vista files with the warped output

To use, first put a 1 in the see_now (or run_now) column of the datalist and then save the file. This 
scripts reads the datalist and pulls out rows that have a 1, then loops over them.

'''
########################################################################
#Import modules, packages, and the datalist
########################################################################

import src.modules.utilities as utilities
import os
import pandas as pd
import datetime



# create list of data
list_of_data  = []

# ask for datalist (csv, first row must be "input_file")
datalist_filepath = utilities.askfordatalist()

###########################################################################################
# print info for user reference
###########################################################################################
timestamp_here = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
print(f"[{timestamp_here}] Starting FSL compilation for:\t {datalist_filepath}")

# Loop through the rows in the csv you specified
for ii, pprow in pd.read_csv(datalist_filepath).iterrows(): 
    ###########################################################################################
    # read from datalist to define things needed for this loop
    ###########################################################################################

    # read from datalist
    nii_file = pprow['input_file']
    text_file = nii_file.replace('.nii','_mean.txt')

    if os.path.exists(text_file):
        with open(text_file, 'r', encoding='utf-8') as file:
          content = file.read()
          list_of_data.append({'filename': text_file, 'content': content}) #text file must have only 1 line
    else:
        print(f"File not found: {text_file}")
    
# Create DataFrame from the list of dictionaries
combined_df = pd.DataFrame(list_of_data)

# Display the DataFrame
print(combined_df)

# save to file
timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.dirname(os.path.realpath(__file__))
output_csv_fullfile = os.path.join(output_dir,f"{timestamp_file}_dkifa_fslcalcs_compiled.csv")
combined_df.to_csv(output_csv_fullfile, index=False)
