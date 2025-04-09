#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
Script to compile the text output of fslstats into a csv file with 
filenames. Intended to be used after running batch_fslstats.sh.

This function prompts the user for the csv file that contains input 
.nii files (which was used in the bash script), and then compiles the 
fslstats -M output into a csv file. 

For details & issues, see https://github.com/mcclaskey/batch_fslstats.

CMcC 4.9.2025
"""

##############################################################################
#Import modules, packages, and the datalist
##############################################################################

import src.modules.utilities as utilities
import src.modules.fsl as fsl
import os
import pandas as pd
import datetime

##############################################################################
# start with basic info: ask user for csv, report, check files
##############################################################################

# create list of data
list_of_data  = []

# ask for datalist (csv, first row must be "input_file")
datalist_filepath = utilities.askfordatalist()

# print info for user reference
timestamp_here = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
print(f"[{timestamp_here}] compile_fsl_data.py.\n\nCompiling .csv file with "
      f"fslstats -M values of .nii files listed in:\n{datalist_filepath}")

# read it and check for missing files
datalist = pd.read_csv(datalist_filepath)
valid_files = {f for f in datalist['input_file'] if os.path.exists(f)}

##############################################################################
# Loop through the rows in the csv, call fsl and add result to list
##############################################################################
for ii, pprow in datalist.iterrows(): 
	nii_file = pprow['input_file']
	output_dict = utilities.compute_mean(nii_file,valid_files)
	list_of_data.append(output_dict)
    
##############################################################################
# create dataframe, save to csv, end program
##############################################################################

# Create DataFrame from the list of dictionaries
combined_df = pd.DataFrame(list_of_data)

# Display the DataFrame
print(combined_df)

# save to file
timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.dirname(os.path.realpath(__file__))
output_csv_fullfile = os.path.join(output_dir,f"{timestamp_file}_dkifa_fslcalcs_compiled.csv")
combined_df.to_csv(output_csv_fullfile, index=False)
print(f"\nProgram complete. Output saved to file:\n{output_csv_fullfile}\n")