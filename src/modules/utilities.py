#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
    Functions for basic utilities, such as path lookups and reading 
    input files

"""

import tkinter as tk
from tkinter import filedialog
import src.modules.fsl as fsl
import pandas as pd
import datetime
import os

def askfordatalist(*args) -> str:
  """Asks user for data list file

  first row must say "input_file" and rest must be list of files

  """
  root = tk.Tk()
  root.withdraw()
  datalist_filepath = filedialog.askopenfilename()
  return datalist_filepath


def compute_mean(nii_file: list[str],
                 valid_files: list[str]) -> dict[str, float]:
    
    """Calls FSLstats for a single file, to be used with map
    
    This function calls FSLstats_mean for a single .nii file and
    returns the output as a dictionary which can be added to a list
    or combined with map().
    
    """
    # Call fslstats_Mean only if the file exists
    if nii_file in valid_files:
        return {'filename': nii_file, 
                'content': fsl.fslstats_Mean(nii_file)}
    else:
        print(f"File not found: {nii_file}")
        return None
    

def save_output_csv(output_df: pd.DataFrame, 
                    datalist_filepath: str):
    
    """Saves data to csv file in same directory as input, with 
    timestamp
    
    """
    
    # get output dir
    output_dir = os.path.dirname(datalist_filepath)
    
	# get output filename
    timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    datalist_fname = os.path.basename(datalist_filepath)
    datalist_fname = datalist_fname.replace('.csv','_compiled.csv')
    output_fname = f"{timestamp_file}_{datalist_fname}"
    
	# save to file
    output_csv_fullfile = os.path.join(output_dir,output_fname)
    output_df.to_csv(output_csv_fullfile, index=False)
    print(f"\nOutput saved to file:\n{output_csv_fullfile}\n")