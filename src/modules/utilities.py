#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
    Functions for basic utilities, such as path lookups and reading input files

"""

import os
import sys
import pandas as pd
import local_parameters
import getpass
import tkinter as tk
from tkinter import filedialog

def safetycheck(repo_dir,data_processed_dir = [],data_compiled_dir = []):
  """safety check in case we're overwriting the main data"""

  caaslrepo_dir = os.path.join(
        os.sep,
        "Volumes",
        "harris_lab",
        "Scripts",
        "ViSTa")  # path to repository

  caasldata_processed_dir = os.path.join(
        os.sep,
        "Volumes",
        "harris_lab",
        "Data_Processed")
  
  caasldata_compiled_dir = os.path.join(
        os.sep,
        "Volumes",
        "harris_lab",
        "Data_Compiled")

  list_of_secure_usernames = ['noone'] #AVSpeech
  current_username = getpass.getuser()


  if (not data_processed_dir == "") & (caaslrepo_dir != repo_dir) & (caasldata_processed_dir == data_processed_dir):
    if any(current_username in usernm for usernm in list_of_secure_usernames):
      print(f'WARNING! You are not using the main z-drive repo but are writing '
            'to the z-drive data_processed dir.\nThis is allowed only because you '
            f'are an approved user. Welcome {current_username}.\n')
      pass_safety_check = True
    else:
      pass_safety_check = False
  else:
    pass_safety_check = True
  

  if (not data_compiled_dir == "") & (caaslrepo_dir != repo_dir) & (caasldata_compiled_dir == data_compiled_dir):
    if any(current_username in usernm for usernm in list_of_secure_usernames):
      print(f'WARNING! You are not using the main z-drive repo but are writing '
            'to the z-drive data_compiled dir.\nThis is allowed only because you '
            f'are an approved user. Welcome {current_username}.\n')
      pass_safety_check = True
    else:
      pass_safety_check = False
  else:
    pass_safety_check = True
  
  return pass_safety_check


def pathlookup(type_here = "scripts",ppid = "*",dki_grantcode = "*",subfolder = ""):

  """Write paths for dki fa calcs
  
  These are determined by Z-drive structure
  """

  # first step: setup the basic z-drive path
  repo_dir = local_parameters.define_repo_dir() # path to repository

  data_processed_dir = local_parameters.define_data_processed_dir()
  if not safetycheck(repo_dir,data_processed_dir = data_processed_dir):
    raise Exception(
          "Oops, safety check failed"
          )

  data_compiled_dir = local_parameters.define_data_compiled_dir()
  if not safetycheck(repo_dir,data_compiled_dir = data_compiled_dir):
    raise Exception(
          "Oops, safety check failed"
          )

  # 2nd level: base folders, without writing any pp/grant information
  match type_here:
    case "scripts" | "datalist":
      pathpath = repo_dir
    case "documentation" | "instructions":
      pathpath = os.path.join(
        repo_dir,
        "documentation",
      )
    case "data_dki_root" | "data_dki":
      pathpath = os.path.join(
        data_processed_dir,
        "DKI",
        "BIDS",
        "derivatives",
        "raw",
      ) #more later
    case "compiled":
      pathpath = data_compiled_dir
    case _:
      pathpath = ""

  # 3rd level: pp levels
  match type_here:
    case "data_dki":
      pathpath = os.path.join(
        pathpath,
        "sub-"+ppid,
        "ses-"+dki_grantcode,
        "dwi_preprocessed",
      ) 
    case _:
      pathpath = pathpath

  # interlude: subfolder
  if not subfolder == "":
    pathpath = os.path.join(
      pathpath,
      subfolder,
      )

  # 3rd level: filenames
  match type_here:
    case "datalist" | "datalist_filenameonly":
      pathpath = os.path.join(
        pathpath,
        "ViSTa_datalist.xlsx",
      )
  return(pathpath)

  # ask for datalist
def askfordatalist(*args):
  """Asks user for data list file

  """
  root = tk.Tk()
  root.withdraw()
  datalist_filepath = filedialog.askopenfilename() #first row must say "input_file" and rest must be list of files
  return datalist_filepath


def loaddatalist(datalist_file=None):
    if datalist_file is None:
      datalist_file = pathlookup("datalist")

    datalist = pd.read_csv(datalist_file)
    return datalist



def compile_csvs(list_of_csv_inputs,output_csv_filename):
  dataframes = []
  for file_path in list_of_csv_inputs:
    df = pd.read_csv(file_path)
    dataframes.append(df)

  # Concatenate all DataFrames into a single DataFrame
  combined_df = pd.concat(dataframes)

  # save to file
  compiled_dir = pathlookup("compiled")
  output_csv_fullfile = os.path.join(compiled_dir,output_csv_filename)
  combined_df.to_csv(output_csv_fullfile, index=False)


if __name__ == "__main__":
    if len(sys.argv) < 6:
      subfolder = ""
    else:
      subfolder: str = sys.argv[5]

    if len(sys.argv) < 5:
      dki_grantcode = "*"
    else:
      dki_grantcode: str = sys.argv[4]

    if len(sys.argv) < 4:
      vista_grantcode = "*"
    else:
      vista_grantcode: str = sys.argv[3]

    if len(sys.argv) < 3:
      ppid = "*"
    else:
      ppid: str = sys.argv[2]
    
    if len(sys.argv) < 2:
      print('type_here argument required for pathlookup()')
    else:
      type_here: str = sys.argv[1]
      print(pathlookup(type_here,ppid,vista_grantcode,dki_grantcode,subfolder))
