#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
Script to compile the text output of fslstats into a csv file with filenames. 
Intended to be used after running batch_fslstats.sh.

This function prompts the user for the csv file that contains input .nii files 
(which was used in the bash script), and then compiles the fslstats -M output 
into a csv file. 

For questions/comments/issues, see https://github.com/mcclaskey/batch_fslstats.

CMcC 4.9.2025
"""

###############################################################################
#Import modules, packages, and the datalist
###############################################################################

import src.modules.utilities as utilities
import os
import pandas as pd
import datetime

###############################################################################
# start with basic info: ask user for csv, initialize variables, report
###############################################################################

# create list of data
list_of_data  = []

# ask for datalist (csv, first row must be "input_file")
datalist_filepath = utilities.askfordatalist()

# print info for user reference
timestamp_here = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
print(f"[{timestamp_here}] Starting FSL compilation for:\t {datalist_filepath}")

###############################################################################
# Loop through the rows in the csv, load context of each file into list
###############################################################################
for ii, pprow in pd.read_csv(datalist_filepath).iterrows(): 
    # lookup text file from csv
    nii_file = pprow['input_file']
    text_file = nii_file.replace('.nii','_mean.txt')

    # read contents of the text file (each txt file assumed to have only 1 row)
    if os.path.exists(text_file):
        with open(text_file, 'r', encoding='utf-8') as file:
          content = file.read()
          list_of_data.append({'filename': text_file, 'content': content})
    else:
        print(f"File not found: {text_file}")
    
###############################################################################
# create dataframe, save to csv, end program
###############################################################################

# Create DataFrame from the list of dictionaries
combined_df = pd.DataFrame(list_of_data)

# Display the DataFrame
print(combined_df)

# save to file
timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.dirname(os.path.realpath(__file__))
output_csv_fullfile = os.path.join(output_dir,f"{timestamp_file}_dkifa_fslcalcs_compiled.csv")
combined_df.to_csv(output_csv_fullfile, index=False)
