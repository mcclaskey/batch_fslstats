#!/usr/bin/env python
# -*- coding : utf-8 -*-

"""
    Functions for basic utilities, such as path lookups and reading input files

"""

import os
import sys
import getpass
import tkinter as tk
from tkinter import filedialog

def askfordatalist(*args):
  """Asks user for data list file

  """
  root = tk.Tk()
  root.withdraw()
  datalist_filepath = filedialog.askopenfilename() #first row must say "input_file" and rest must be list of files
  return datalist_filepath
