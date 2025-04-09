#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
    Functions for basic utilities, such as path lookups and reading input files

"""

import tkinter as tk
from tkinter import filedialog
import src.modules.fsl as fsl

def askfordatalist(*args) -> str:
  """Asks user for data list file

  """
  root = tk.Tk()
  root.withdraw()
  datalist_filepath = filedialog.askopenfilename() #first row must say "input_file" and rest must be list of files
  return datalist_filepath


def compute_mean(nii_file: list[str],valid_files: list[str]) -> dict[str, float]:
    """Calls FSLstats for a single file, to be used with map
    
    This function calls FSLstats_mean for a single .nii file and
    returns the output as a dictionary which can be added to a list
    or combined with map().
    
    """
    # Call fslstats_Mean only if the file exists
    if nii_file in valid_files:
        return {'filename': nii_file, 'content': fsl.fslstats_Mean(nii_file)}
    else:
        print(f"File not found: {nii_file}")
        return None